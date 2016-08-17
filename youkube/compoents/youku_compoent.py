#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016年8月9日13:16:54
import youku


class Youku(object):

    def __init__(self, client_id, access_token):
        self.client_id = client_id
        self.access_token = access_token


    def upload(self, file_path, title, tags, description):
        """
        上传

        """
        file_info = {
            'title': title,
            'tags': tags,
            'description': description
        }

        youku_upload = youku.YoukuUpload(self.client_id, self.access_token, file_path)
        youku_upload.upload(file_info)

