#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016年8月9日13:16:54
import json
import re
import urllib
import urllib2

import requests
import time

import sys
import youtube_dl
from BeautifulSoup import BeautifulSoup
import youkube.constants as constans
import youkube.util as util

logger = util.get_logger("YoutubeCompoent")


class YoutubeCompoentImpl(object):

    def fetch_video_base_info(self, url):
        return YoutubeDl.fetch_video_base_info(url)

    def fetch_user_page_video_links(self, user):
        return YoutubeDl.fetch_user_page_video_links(user)

    def download(self, url, video_dir, ext, download_url):
        return YoutubeDl.download(url, video_dir, ext, download_url)


class YoutubeDl(object):

    @staticmethod
    def fetch_video_base_info(url):
        params = {  'format': 'best/best', # 最高画质
                    'forcejson': True, # 返回json数据
                    'simulate': True}  # 不进行下载操作

        dl = youtube_dl.YoutubeDL(params)

        return json.loads(dl.download(url))

    @staticmethod
    def fetch_user_page_video_links(user):
        logger.debug("[fetch_user_page_video_links] urlopen url: %s" % (constans.YOUTUBE_USER_BASE_URL % user))

        body = urllib2.urlopen(constans.YOUTUBE_USER_BASE_URL % user).read()

        soup = BeautifulSoup(body)

        links = soup.findAll('a', attrs={'href': re.compile(constans.YOUTUBE_VIDEO_LINK_REGEX)})

        return links

    @staticmethod
    def download(url, video_dir, ext, video_url):

        file_name = "%s/%s\.%s" % (video_dir, util.md5encode(url), ext)

        with open(file_name, "wb") as f:
            logger.debug("Downloading %s" % file_name)
            response = None
            try:
                response = requests.get(video_url, stream=True)
            except Exception as e:
                logger.debug(e.message)
                return

            total_length = response.headers.get('content-length')

            logger.debug("File length %s bytes" % total_length)

            start_time = time.time()

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(1024):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)

                    kbs = formatDownloadSpeed(dl, start_time)

                    sys.stdout.write("\r[%s%s] %s %% %s" % (
                    '=' * done, ' ' * (50 - done), "{:0.2f}".format(dl / float(total_length) * 100), kbs))
                    sys.stdout.flush()

                logger.debug("Download Complete Elapsed %sM%sS" % (
                (time.time() - start_time) / 60, (time.time() - start_time) % 60))


        # params = {'format': 'best/best',  # 最高画质
        #           'progress_hooks': [download_progress_hook],
        #           'logger': DownloaderLogger(),
        #           'outtmpl': video_dir + '/' + util.md5encode(util) + '.' + ext
        #           }
        #
        # dl = youtube_dl.YoutubeDL(params)

        # dl.download(url)


def formatDownloadSpeed(dl, start_time):
    now = time.time()
    consum_seconds = now - start_time
    dl_per_second = dl / consum_seconds

    k = dl_per_second / 1024.00
    b = dl_per_second % 1024.00
    b = b / 1024.00

    kbs = k + b
    return "{:0.2f}".format(kbs) + 'KBS'

def download_progress_hook(data):
    print data

    if data['status'] == 'finished':
        print('Done downloading, now converting ...')


class DownloaderLogger(object):
    def debug(self, msg):
        logger.debug(msg)

    def warning(self, msg):
        logger.debug(msg)

    def error(self, msg):
        logger.debug(msg)


class YoutubeException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


class YoutubeDlException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message
