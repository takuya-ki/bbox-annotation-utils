#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import os.path as osp
from math import floor
import xml.dom.minidom as minidom
import xml.etree.cElementTree as ET


def generate_xml(imgname, width, height, ch, voc_labels, xmlpath):
    # create root
    root = ET.Element("annotations")
    ET.SubElement(root, "filename").text = imgname
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(ch)

    # create object_annotation
    for voc_label in voc_labels:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = voc_label[0]
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = str(0)
        ET.SubElement(obj, "difficult").text = str(0)
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(voc_label[1])
        ET.SubElement(bbox, "ymin").text = str(voc_label[2])
        ET.SubElement(bbox, "xmax").text = str(voc_label[3])
        ET.SubElement(bbox, "ymax").text = str(voc_label[4])

    xml_string = ET.tostring(root, 'utf-8')
    pretty_string = minidom.parseString(
        xml_string).toprettyxml(indent=' ', encoding='utf-8')

    with open(xmlpath, mode='wb') as f:
        f.write(pretty_string)


def txt2xml(txtpath, imgpath, classes, xmlpath):
    h, w, ch = cv2.imread(imgpath).shape
    with open(txtpath) as file:
        lines = file.readlines()
        voc_labels = []
        for line in lines:
            voc = []
            line = line.strip()
            data = line.split()
            voc.append(classes.get(data[0]))
            bbox_width = float(data[3]) * w
            bbox_height = float(data[4]) * h
            center_x = float(data[1]) * w
            center_y = float(data[2]) * h
            voc.append(floor(center_x - (bbox_width / 2)))
            voc.append(floor(center_y - (bbox_height / 2)))
            voc.append(floor(center_x + (bbox_width / 2)))
            voc.append(floor(center_y + (bbox_height / 2)))
            voc_labels.append(voc)
        generate_xml(osp.basename(imgpath), w, h, ch, voc_labels, xmlpath)
    print("Processing complete for file: {}".format(txtpath))


if __name__ == "__main__":

    classes = dict()
    imgext = 'jpg'
    datasetpath = osp.join(
        osp.dirname(__file__), "..", "dataset")
    xmldirpath = osp.join(
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
            classes = {str(k): v for (k, v) in enumerate(class_list)}
    os.makedirs(xmldirpath, exist_ok=True)  # generate output directory

    for txtname in os.listdir(txtdirpath):
        if txtname.endswith('txt'):
            txtpath = osp.join(txtdirpath, txtname)
            if os.stat(txtpath).st_size > 0:  # not empty txt
                txt_prefix = txtname.split(".txt")[0]
                imgname = txt_prefix + '.' + imgext
                imgpath = osp.join(imgdirpath, imgname)
                xmlpath = osp.join(xmldirpath, txt_prefix + ".xml")
                txt2xml(txtpath, imgpath, classes, xmlpath)
        else:
            print("Skipping file: {}".format(txtname))
