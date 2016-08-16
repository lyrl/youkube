#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-26 11:04:34
import sys
import os
path = os.getcwd()
if path not in sys.path:
    sys.path.append(path)

import youtube_dl

class MyLogger(object):
    def debug(self, msg):
        print msg
        pass

    def warning(self, msg):
        # print msg
        pass

    def error(self, msg):
        print(msg)


if __name__ == '__main__':


    def my_hook(d):
        print d
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')


    ydl_opts = {
        # 'format': 'best/best',
        # 'logger': MyLogger(),
        # 'progress_hooks': [my_hook],
        'proxy': 'socks5://127.0.0.1:1080/',
        'forcejson': True,
        'simulate': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=XUY0-doBx1U'])
