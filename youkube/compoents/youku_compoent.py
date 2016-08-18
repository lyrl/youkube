#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016年8月9日13:16:54
import json

import youku
import youkube.util as util

logger = util.get_logger("YOUKU")


categorys = [
     {
        "id": 99,
        "term": "Games",
        "label": "游戏",
        "lang": "zh_CN"
    },
    {
        "id": 105,
        "term": "Tech",
        "label": "科技",
        "lang": "zh_CN"
    },
    {
        "id": 94,
        "term": "Humor",
        "label": "搞笑",
        "lang": "zh_CN"
    }
]

def find_category(desc):
    for i in categorys:
        if i['label'] == desc:
            return i['id']
    return ''

class Youku(object):

    def __init__(self, client_id, access_token):
        self.client_id = client_id
        self.access_token = access_token

    def upload(self, file_path, title, tags, description, category):
        """
        上传

        """

        logger.info("category %s  category id : %s" % (category,find_category(category)))

        file_info = {
            'title': title,
            'tags': tags,
            'description': description,
            'category': find_category(category)
        }

        logger.debug("YOUKU - file_path %s title %s tags %s description %s" % (file_path, title, tags, description))

        youku_upload = youku.YoukuUpload(self.client_id, self.access_token, file_path)
        youku_upload.upload(file_info)

