#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

class config_path:
    def __init__(self):
        self.tmpl_name = "target.jpg"
        self.top_dir  = "./"
        self.raw_dir = "raw"
        self.hsd_dir = "hsd"

class config_param:
    def __init__(self):
        self.file_num = 100

class config_const:
    def __init__(self):
        self.H_LABEL = 0
        self.E_LABEL = 1
        self.B_LABEL = 2


def init():
    path = config_path()
    raw_dir_path = os.path.join(path.raw_dir)
    if os.path.exists(raw_dir_path):
        print("%s is exist!" %(raw_dir_path))
    else:
        print("error")
        return 1

    hsd_dir_path = os.path.join(path.raw_dir)
    if os.path.exists(hsd_dir_path):
        print("%s is exist!" %(hsd_dir_path))
    else:
        os.makedirs(hsd_dir_path)
        print("creat the hsd dir")
    return 0