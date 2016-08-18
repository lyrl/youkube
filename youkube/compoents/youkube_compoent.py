#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016年8月9日13:16:54
import datetime
import json
import os

import youkube.compoents.model as model
import youkube.compoents.youtube_compoent as youtube
import youkube.util as util
import time
import youkube.constants as constants
import youkube.compoents.youku_compoent as youkucom

logger = util.get_logger('Youkube')


"""
配置文件示例

user youtube要订阅的用户
video_dir 视频文件保存路径
thumbnail_dir 视频缩略图/封面图保存路径
sqlite3_file sqlite3数据库文件路
youku_client_id  优酷client id
youku_access_token  优酷access_token


{
  "users": [
        {"user":"greatscottlab", "channel_name": "GreateScoot", "youku_prefix": "GreateScoot - ", "desc": "模拟电路数字电路", "category": "科技"},
        {"user":"DarduinMyMenlon", "channel_name": "Dota2 WTF", "youku_prefix" : "", "desc" : "Dota2 Wtf", "category": "游戏"}


                {"user":"Larva2011ani", "channel_name": "Larva ", "youku_prefix" : "Larva - ", "desc" : "红虫黄虫", "category": "搞笑"}
    ],
  "video_dir": "/root/video",
  "thumbnail_dir": "/root/thumbnail",
  "sqlite3_file": "/root/sqlite3.db",
  "youku_client_id": "97c24e4be2c1383a",
  "youku_access_token": "a1a718a2d25943a12002802877622961"
}
"""


class Youkube(object):

    def __init__(self, config_file_path):
        with open(config_file_path) as file:
            self.config = json.loads(file.read())

        if not self.config:
            raise YoukubeException("配置文件读取失败!")

        self.repo = YoukubeRepo(self.config['sqlite3_file'])
        self.youtube = youtube.YoutubeCompoentImpl()
        self.youku = youkucom.Youku(self.config['youku_client_id'], self.config['youku_access_token'])

    def run(self):

        while True:
            logger.info("[Youkube] - 检查并准备删除已上传成功的视频文件...")
            self.del_uploaded_video_file()

            logger.info("[Youkube] - 检查未完成上传的视频...")
            self.retry_upload_task()

            logger.info("[Youkube] - 抓取最新视频...")
            self.fetch_new_videos()

            logger.info(u"[Youkube] - 所有视频处理完成，等待1分钟重新获取新视频!")
            time.sleep(60)

    def fetch_new_videos(self):
        for i in self.config['users']:
            links = self.youtube.fetch_user_page_video_links(i['user'])

            self.fetch_new_video(self.rm_dup_link(links),i)

    def rm_dup_link(self, links):
        uniquelist = []
        for i in links:
            if (i not in uniquelist ) and (not self.repo.find_by_url(i)):
                uniquelist.append(i)

        return uniquelist

    def fetch_new_video(self,  uniquelist, use_info):
        """
         {
         "user":"greatscottlab",
          "channel_name": "GreateScoot",
          "youku_prefix": "GreateScoot - ",
          "desc": "模拟电路数字电路",
          "category": "科技"
        }

        """

        for link in uniquelist:
            # 视频基本信息的字典数据，信息由youtube-dl 提供
            info_dict = self.youtube.fetch_video_base_info(link)
            # 将视频保存到数据库
            video_entity = self.__save_new_video_info_to_db__(info_dict, use_info)
            logger.debug(u"发现新视频 %s 时长 %s " % (video_entity.title, video_entity.duration))

            logger.info(u"视频 %s 下载任务创建成功，正在下载！" % video_entity.title)
            self.repo.chg_status(video_entity, constants.VIDEO_STATUS_DOWNLOADING)

            self.youtube.download(link, self.config['video_dir'], video_entity.ext, info_dict['url'])
            logger.info(u"视频 %s 下载成功，准备上传！" % video_entity.title)

            video_entity.filesize = os.path.getsize(
                "%s%s.%s" % (self.config['video_dir'], util.md5encode(video_entity.url), video_entity.ext))
            self.repo.save(video_entity)
            self.repo.chg_status(video_entity, constants.VIDEO_STATUS_DOWNLOADED)

            self.retry_upload_task()
            self.del_uploaded_video_file()


    def retry_upload_task(self):
        need_upload_video = self.repo.find_need_upload_video()

        for n in need_upload_video:
            n.filesize = os.path.getsize(
                "%s%s.%s" % (self.config['video_dir'], util.md5encode(n.url), n.ext))
            self.repo.save(n)

            logger.info(u"[Youkube] - 视频 %s 开始上传！" % n.title)
            self.repo.chg_status(n, constants.VIDEO_STATUS_UPLOADING)

            try:
                self.youku.upload(
                    "%s%s.%s" % (self.config['video_dir'], util.md5encode(n.url), n.ext),
                    n.youku_prefix + n.title, "", n.desc, n.category)
            except Exception as e:
                logger.warn(u"[Youkube] - 视频上传失败!" + e.message)
                raise e
                # continue

            logger.info(u"[Youkube] - 视频 %s 上传完成！" % n.title)
            self.repo.chg_status(n, constants.VIDEO_STATUS_UPLOADED)
            self.del_uploaded_video_file()

    def del_uploaded_video_file(self):
        uploaded_videps = self.repo.find_uploaded_video()

        for v in uploaded_videps:
            file_paht = self.config['video_dir'] + '/' + v.url_hash + '.' + v.ext
            is_exist = os.path.exists(file_paht)

            if is_exist:
                logger.info(u"[Youkube] - 视频 %s 已上传成功 ! 视频文件 %s 准备删除!", (v.title, file_paht))
                os.remove(file_paht)
                logger.info(u"[Youkube] - 视频 %s  视频文件 %s 删除成功!", (v.title, file_paht))


    def __save_new_video_info_to_db__(self, info_dict, user_info):

        """
         {
         "user":"greatscottlab",
          "channel_name": "GreateScoot",
          "youku_prefix": "GreateScoot - ",
          "desc": "模拟电路数字电路"},

        """

        date_time_format = '%Y%m%d'
        video = model.Video()

        video.url = info_dict['webpage_url']
        video.url_hash = util.md5encode(video.url)
        video.uploader = info_dict['uploader']
        video.title = info_dict['title']
        video.like_count = info_dict['like_count']
        video.dislike_count = info_dict['dislike_count']
        video.duration = info_dict['duration']
        video.format_note = info_dict['format_note']
        video.height = info_dict['height']
        video.width = info_dict['width']
        video.resolution = info_dict['resolution']
        video.view_count = info_dict['view_count']
        video.video_id = info_dict['id']
        video.format = info_dict['format']
        video.filesize = 0 # info_dict['filesize']
        video.ext = info_dict['ext']
        video.thumbnail = info_dict['thumbnail']
        try:
            video.upload_date = datetime.datetime.strptime(info_dict['upload_date'], date_time_format)
        except Exception:
            video.upload_date = datetime.datetime.now()


        video.create_time = datetime.datetime.now()
        video.update_time = datetime.datetime.now()

        video.user = user_info['user']
        video.channel_name = user_info['channel_name']
        video.youku_prefix = user_info['youku_prefix']
        video.desc = user_info['desc']
        video.category = user_info['category']

        self.repo.save(video)

        return video



class YoukubeRepo(object):
    """数据库访问类

    包括了视频信息，任务信息等等

    Attributes:
        sqlite3_file (str): 数据库文件位置
    """
    def __init__(self, sqlite3_file):
        if not sqlite3_file:
            raise YoukubeRepoException("参数 sqlite3_file 不能为空!")

        model.deferred_db.init(sqlite3_file)

        try:
            model.deferred_db.connect()
        except Exception as e:
            raise YoukubeRepoException("数据库连接失败: " + e.message)

        if not model.Video.table_exists():
            model.Video.create_table()

    def save(self, video):
        """将新发布的视频信息保存到数据库

        Args:
            video (model.Video): 视频实体
        """
        video.save()

    def update(self, video):
        """将新发布的视频信息保存到数据库

        Args:
            video (model.Video): 视频实体
        """
        video.update()

    def find_by_url_hash(self, url_hash):
        try:
            model.Video.get(model.Video.url_hash == url_hash)
        except:
            return None

    def find_by_url(self, url):
        try:
            return model.Video.get(model.Video.url == url)
        except:
            return None

    def chg_status(self, video_entity, status):
        video_entity.status = status
        video_entity.update_time = datetime.datetime.now()
        video_entity.save()

    def find_need_upload_video(self):
        return model.Video.select().where(model.Video.status >= 3 and model.Video.status <= 5)

    def find_uploaded_video(self):
        return model.Video.select().where(model.Video.status == 6)


class YoukubeRepoException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message

class YoukubeException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message