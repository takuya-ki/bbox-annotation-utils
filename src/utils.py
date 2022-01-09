#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import glob
import os.path as osp


def get_file_paths(file_dir, file_ext, is_show=False):
    path = osp.join(file_dir, '*.'+file_ext)
    file_paths = glob.glob(path)
    file_names = [osp.splitext(osp.basename(r))[0] for r in file_paths]
    if is_show:
        print(file_names)
        print(file_paths)
    return file_paths, file_names


def scale_to_width(img, width):
    scale = width / img.shape[1]
    return cv2.resize(img, dsize=None, fx=scale, fy=scale)
