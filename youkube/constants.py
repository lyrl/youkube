#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-26 11:04:34


VIDEO_STATUS_NEW = 0  # 新视频
VIDEO_STATUS_DOWNLOADING = 1  # 下载中
VIDEO_STATUS_DOWNLOAD_FAIL = 2  # 下载完成
VIDEO_STATUS_DOWNLOADED = 3  # 上传中
VIDEO_STATUS_UPLOADING = 4  # 上传失败
VIDEO_STATUS_UPLOADING_FAIL = 5  # 上传完成
VIDEO_STATUS_UPLOADED = 6  # 上传成功



YOUTUBE_USER_BASE_URL = "https://www.youtube.com/user/%s/videos"
YOUTUBE_VIDEO_LINK_REGEX = '/watch\?v=\w+$'
YOUTUBE_BASE_URL = "https://www.youtube.com"

YOUKU_CLIENT_ID = '97c24e4be2c1383a'
YOUKU_ACCESS_TOKEN = 'a1a718a2d25943a12002802877622961'

