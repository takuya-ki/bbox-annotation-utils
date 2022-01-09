#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import os.path as osp

from utils import get_file_paths, scale_to_width


def draw_txt_annotation(imgpath, txtpath, classes, colors, is_save=True):
    img = cv2.imread(imgpath, cv2.IMREAD_COLOR)
    height, width = img.shape[:2]
    with open(txtpath, mode='r') as f:
        for row in f:
            splitrow = row.strip().split(' ')
            if len(splitrow[0]) != 0:
                # (x+w/2.00)/width (y+h/2.00)/height w/width h/height
                lab = classes[int(splitrow[0])]
                if not colors:
                    color = np.uint8(np.random.uniform(0, 255, 3))
                    c = tuple(map(int, color))
                else:
                    c = colors[lab]

                w = int(float(splitrow[3])*float(width))
                h = int(float(splitrow[4])*float(height))
                x = int(float(splitrow[1])*float(width)-w/2.00)
                y = int(float(splitrow[2])*float(height)-h/2.00)
                txtpos = (x, y-5)
                cv2.putText(
                    img, lab, txtpos, cv2.FONT_HERSHEY_PLAIN, 3.5, c, 5)
                cv2.rectangle(img, (x, y), (x+w, y+h), c, 1)
                cv2.circle(img, (x, y), 10, c, -1)
                cv2.circle(img, (x+w, y), 10, c, -1)
                cv2.circle(img, (x+w, y+h), 10, c, -1)
                cv2.circle(img, (x, y+h), 10, c, -1)

    cv2.imshow("drawed", scale_to_width(img, 1000))
    if is_save:
        dirpath, imgname = osp.split(imgpath)
        outdirpath = osp.join(dirpath, 'result_from_txt')
        os.makedirs(outdirpath, exist_ok=True)  # generate output directory
        cv2.imwrite(osp.join(outdirpath, imgname), img)
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()


if __name__ == '__main__':

    datasetpath = osp.join(
        osp.dirname(__file__), "..", "dataset")
    classes = dict()
    classes_txt_path = osp.join(
        datasetpath, "class_color_list.txt")
    if not osp.isfile(classes_txt_path):
        print("Check class list file: {}".format(classes_txt_path))
        exit()
    with open(classes_txt_path, "r") as f:
        clist = f.read().strip().split()
        classes = {k: str(v).split(',')[0] for (k, v) in enumerate(clist)}
        colors = None
        if len(clist[0].split(',')) > 1:
            colors = {
                str(v).split(',')[0]:
                tuple((int(str(v).split(',')[1]),
                       int(str(v).split(',')[2]),
                       int(str(v).split(',')[3])))
                for (k, v) in enumerate(clist)}

    imgext = 'jpg'
    imgdirpath = osp.join(
        datasetpath, imgext)
    txtdirpath = osp.join(
        datasetpath, "txt")

    imgpaths, imgnames = get_file_paths(imgdirpath, imgext)
    for imgpath, imgname in zip(imgpaths, imgnames):
        txtpath = osp.join(txtdirpath, imgname+'.txt')
        if os.stat(txtpath).st_size > 0:  # not empty txt
            draw_txt_annotation(imgpath, txtpath, classes, colors)
        else:
            print("Skipping file (empty txt file): {}".format(txtpath))
