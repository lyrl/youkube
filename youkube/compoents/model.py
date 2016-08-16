#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-26 11:04:34
import peewee
import youkube.constants as constants

deferred_db = peewee.SqliteDatabase(None)


class BaseModel(peewee.Model):
    class Meta:
        database = deferred_db


class Video(BaseModel):
    url_hash = peewee.CharField(unique=True, index=True)            # 地址hash
    url = peewee.CharField(unique=True)                 # url
    uploader = peewee.CharField()            # 作者
    title = peewee.CharField()               # 标题
    like_count = peewee.IntegerField()       # 喜欢数
    dislike_count = peewee.IntegerField()    # 不喜欢数
    duration = peewee.IntegerField()         # 时长
    format_note = peewee.CharField()         # 格式描述
    height = peewee.IntegerField()           # 高度
    width = peewee.IntegerField()            # 宽度
    resolution = peewee.CharField()          # 分辨率
    view_count = peewee.IntegerField()       # 播放次数
    filesize = peewee.IntegerField()       # 文件大小
    video_id = peewee.CharField(unique=True,index=True)            # 视频id
    format = peewee.CharField()              # 描述
    ext = peewee.CharField()                 # 视频拓展名/后缀
    upload_date = peewee.DateTimeField()     # 上传时间

    create_time = peewee.DateTimeField()
    update_time = peewee.DateTimeField()

    # 视频状态 默认：新视频

    status = peewee.IntegerField(default=constants.VIDEO_STATUS_NEW)


