#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-26 11:04:34
import os
import sys

path = os.getcwd()
if path not in sys.path:
    sys.path.append(path)

import youkube.compoents.youkube_compoent as youkube



if __name__ == '__main__':
    ykb = youkube.Youkube('./config.json')
    ykb.run()