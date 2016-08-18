#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016年8月9日13:16:54
import json

import youku
import youkube.util as util

logger = util.get_logger("YOUKU")


categorys = {
    "游戏": {
        "term": "Games",
        "label": "游戏",
        "lang": "zh_CN"
    },
    "科技": {
        "term": "Tech",
        "label": "科技",
        "lang": "zh_CN"
    },
    "搞笑": {
        "term": "Humor",
        "label": "搞笑",
        "lang": "zh_CN",

    }
}

class Youku(object):

    def __init__(self, client_id, access_token):
        self.client_id = client_id
        self.access_token = access_token


    def upload(self, file_path, title, tags, description, category):
        """
        上传

        """
        try:
            text_category = json.dumps(categorys[category])
        except Exception:
            text_category = ''

        file_info = {
            'title': title,
            'tags': tags,
            'description': description,
            'category': text_category
        }

        logger.debug("YOUKU - file_path %s title %s tags %s description %s" % (file_path, title, tags, description))

        youku_upload = youku.YoukuUpload(self.client_id, self.access_token, file_path)
        youku_upload.upload(file_info)

