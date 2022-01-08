#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import cv2
import os.path as osp
from glob import glob
from lxml import etree
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement


class PascalVocReader:
    def __init__(self, filepath):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color, difficult]
        self.shapes = []
        self.filepath = filepath
        self.verified = False
        self.parseXML()

    def getShapes(self):
        return self.shapes

    def addShape(self, label, bndbox, filename, difficult):
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        self.shapes.append((label, points, filename, difficult))

    def parseXML(self):
        assert self.filepath.endswith('.xml'), "Unsupport file format"
        parser = etree.XMLParser(encoding='utf-8')
        xmltree = ElementTree.parse(self.filepath, parser=parser).getroot()
        filename = xmltree.find('filename').text
        try:
            verified = xmltree.attrib['verified']
            if verified == 'yes':
                self.verified = True
        except KeyError:
            self.verified = False

        for object_iter in xmltree.findall('object'):
            bndbox = object_iter.find("bndbox")
            label = object_iter.find('name').text

            difficult = False
            if object_iter.find('difficult') is not None:
                difficult = bool(int(object_iter.find('difficult').text))
            self.addShape(label, bndbox, filename, difficult)
        return True


if __name__ == '__main__':

    classes = dict()
    num_classes = 0

    imgext = 'jpg'
    datasetpath = osp.join(
        osp.dirname(__file__), "..", "dataset")
    xmlpath = osp.join(
        datasetpath, "xml")
    imgdirpath = osp.join(
        datasetpath, imgext)
    txtdirpath = osp.join(
        datasetpath, "txt")
    classes_txt_path = osp.join(
        datasetpath, "class_list.txt")

    if osp.isfile(classes_txt_path):
        with open(classes_txt_path, "r") as f:
            class_list = f.read().strip().split()
            classes = {k : v for (v, k) in enumerate(class_list)}
    os.makedirs(txtdirpath, exist_ok=True)

    xmlPaths = glob(xmlpath + "/*.xml")
    for xmlPath in xmlPaths:
        tVocParseReader = PascalVocReader(xmlPath)
        shapes = tVocParseReader.getShapes()
        txtpath = osp.join(txtdirpath, osp.basename(xmlPath)[:-4] + ".txt")
        with open(txtpath, "w") as f:
            for shape in shapes:
                class_name = shape[0]
                box = shape[1]
                filename = osp.splitext(
                    osp.join(imgdirpath, osp.basename(xmlPath)[:-4]))[0] +'.'+ imgext

                if class_name not in classes.keys():
                    classes[class_name] = num_classes
                    num_classes += 1
                class_idx = classes[class_name]

                (height, width, _) = cv2.imread(filename).shape

                coord_min = box[0]
                coord_max = box[2]

                xcen = float((coord_min[0] + coord_max[0])) / 2 / width
                ycen = float((coord_min[1] + coord_max[1])) / 2 / height
                w = float((coord_max[0] - coord_min[0])) / width
                h = float((coord_max[1] - coord_min[1])) / height

                f.write("%d %.06f %.06f %.06f %.06f\n" % (class_idx, xcen, ycen, w, h))
                print(class_idx, xcen, ycen, w, h)

    with open(osp.join(datasetpath, "class_found.txt"), "w") as f:
        for key in classes.keys():
            f.write("%s\n" % key)
            print(key)
