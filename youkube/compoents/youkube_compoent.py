#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016年8月9日13:16:54
import datetime
import json

import youkube.compoents.model as model
import youkube.compoents.youtube_compoent as youtube
import youkube.util as util
import time
import youkube.constants as constants

logger = util.get_logger('Youkube')


"""
配置文件示例

user youtube要订阅的用户
video_dir 视频文件保存路径
thumbnail_dir 视频缩略图/封面图保存路径
sqlite3_file sqlite3数据库文件路

{
  "user": "greateScoot",
  "video_dir": "/root/video",
  "thumbnail_dir": "/root/thumbnail",
  "sqlite3_file": "/root/sqlite3.db"
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

    def run(self):

        while True:
            links = self.youtube.fetch_user_page_video_links(self.config['user'])
            # 未下载的视频,添加到任务列表
            schedule_links = [i for i in links if not self.repo.find_by_url(i)]

            for link in schedule_links:

                if self.repo.find_by_url(link):
                    continue

                # 视频基本信息的字典数据，信息由youtube-dl 提供
                info_dict = self.youtube.fetch_video_base_info(link)
                # 将视频保存到数据库
                video_entity = self.__save_new_video_info_to_db__(info_dict)
                logger.debug(u"发现新视频 %s 时长 % 大小 %s " % (video_entity.title, video_entity.duration, video_entity.filesize))

                logger.info(u"视频 %s 下载任务创建成功，正在下载！" % video_entity.title)
                self.repo.chg_status(video_entity, constants.VIDEO_STATUS_DOWNLOADING)

                self.youtube.download(link, self.config['video_dir'], video_entity.ext, info_dict['url'])
                logger.info(u"视频 %s 下载成功，准备上传！" % video_entity.title)


            logger.info(u"所有视频处理完成，等待10秒重新获取新视频!")
            time.sleep(10)







































    def __save_new_video_info_to_db__(self, info_dict):
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
        video.filesize = 999999999 # info_dict['filesize']
        video.ext = info_dict['ext']
        video.thumbnail = info_dict['thumbnail']
        video.upload_date = datetime.datetime.strptime(info_dict['upload_date'], date_time_format)
        video.create_time = datetime.datetime.now()
        video.update_time = datetime.datetime.now()

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
        video_entity.update()


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