#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import os.path as osp
from PIL import Image
from math import floor
import xml.dom.minidom as minidom
import xml.etree.cElementTree as ET


def create_root(file_prefix, width, height):
    root = ET.Element("annotations")
    ET.SubElement(root, "filename").text = file_prefix + '.' + imgext
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(imgchnls)
    return root


def create_object_annotation(root, voc_labels):
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
    return root


def create_file(file_prefix, width, height, voc_labels):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    save_xml_path = osp.join(xmldirpath, file_prefix+".xml")
    # tree = ET.ElementTree(root)
    # tree.write(save_xml_path)

    xml_string = ET.tostring(root, 'utf-8')
    pretty_string = minidom.parseString(
        xml_string).toprettyxml(indent=' ', encoding='utf-8')

    with open(save_xml_path, mode='wb') as f:
        f.write(pretty_string)


def read_file(file_path):
    file_prefix = file_path.split(".txt")[0]
    image_file_name = file_prefix + '.' + imgext
    img = Image.open(osp.join(imgdirpath, image_file_name))

    w, h = img.size
    prueba = osp.join(txtdirpath, file_path)
    with open(prueba) as file:
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
        create_file(file_prefix, w, h, voc_labels)
    print("Processing complete for file: {}".format(file_path))


if __name__ == "__main__":

    imgchnls = 3  # RGB:3, Grayscale:1
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
    os.makedirs(xmldirpath, exist_ok=True)
    for filename in os.listdir(txtdirpath):
        if filename.endswith('txt'):
            PathFileName = osp.join(txtdirpath, filename)
            if os.stat(PathFileName).st_size > 0:
                read_file(filename)
        else:
            print("Skipping file: {}".format(filename))
