#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-26 11:04:34
import json
import unittest
import youkube.util as util


class YoukubeTestCase(unittest.TestCase):

    def test_youkube(self):
        print util.md5encode('hello')

if __name__ == '__main__':
    unittest.main()