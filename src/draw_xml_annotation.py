#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import os.path as osp
from lxml import etree

from utils import get_file_paths, scale_to_width


class annotation_xml(object):

    def __init__(self, data_path):
        self.file_path = data_path
        self.root = None
        self.object_name_list = None
        self._get_root()

    def _get_root(self):
        if '.xml' in self.file_path:
            tree = etree.parse(self.file_path)
            self.root = tree.getroot()

    def get_bbox(self, img_shape):
        img_height, img_width = img_shape[:2]
        height = int(self.root.find('size').find('height').text)
        width = int(self.root.find('size').find('width').text)

        label_names = []
        bounding_boxes = []
        for object_tree in self.root.findall('object'):
            for bb in object_tree.iter('bndbox'):
                xmin = float(bb.find('xmin').text)
                ymin = float(bb.find('ymin').text)
                xmax = float(bb.find('xmax').text)
                ymax = float(bb.find('ymax').text)
            label_names.append(object_tree.find('name').text)
            bounding_box = [xmin, ymin, xmax, ymax]

            if height != img_height or width != img_width:
                bounding_box[0] = bounding_box[0] * img_width / width
                bounding_box[1] = bounding_box[1] * img_height / height
                bounding_box[2] = bounding_box[2] * img_width / width
                bounding_box[3] = bounding_box[3] * img_height / height
                print("Bounding box positions of \
                       the ground truth are modified. \
                       (Not sure if this always does work.)")
            bounding_boxes.append(bounding_box)

        return label_names, bounding_boxes


def draw_annotation(imgpath, xmlpath, is_save=True):
    img = cv2.imread(imgpath)
    if not osp.isfile(xmlpath):
        print(xmlpath + " is not existed.")
        exit()

    anno_xml = annotation_xml(xmlpath)
    labels, bboxs = anno_xml.get_bbox(img.shape)

    # draw and view
    for i, (lab, bb) in enumerate(zip(labels, bboxs)):
        # color = np.uint8(np.random.uniform(0, 255, 3))
        # c = tuple(map(int, color))
        # c = (255, 255, 255)
        if lab == 'PlasticBottle':
            c = (0, 255, 0)
            lab = 'Plastic bottle'
        elif lab == 'Can':
            c = (255, 102, 153)
            lab = 'Aluminum can'
        elif lab == 'Bottle':
            c = (0, 153, 255)
            lab = 'Glass bottle'

        bb = [int(i) for i in bb]
        text_pos = (bb[0], bb[1] - 10)
        cv2.putText(
            img, lab, text_pos, cv2.FONT_HERSHEY_PLAIN, 3.5, c, 5)
        cv2.rectangle(img, (bb[2], bb[3]), (bb[0], bb[1]), c, 2)
        cv2.circle(img, (bb[2], bb[3]), 10, c, -1)
        cv2.circle(img, (bb[0], bb[3]), 10, c, -1)
        cv2.circle(img, (bb[0], bb[1]), 10, c, -1)
        cv2.circle(img, (bb[2], bb[1]), 10, c, -1)

    cv2.imshow("drawed", scale_to_width(img, 1000))
    if is_save:
        dirpath, imgname = osp.split(imgpath)
        outdirpath = osp.join(dirpath, 'result')
        os.makedirs(outdirpath, exist_ok=True)  # generate output directory
        cv2.imwrite(osp.join(outdirpath, imgname), img)
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()


if __name__ == '__main__':

    imgext = 'jpg'
    datasetpath = osp.join(
        osp.dirname(__file__), "..", "dataset")
    imgdirpath = osp.join(
        datasetpath, imgext)
    xmldirpath = osp.join(
        datasetpath, "xml")

    imgpaths, imgnames = get_file_paths(imgdirpath, imgext)
    for imgpath, imgname in zip(imgpaths, imgnames):
        xmlpath = osp.join(xmldirpath, imgname+'.xml')
        if os.stat(xmlpath).st_size > 0:  # not empty xml
            draw_annotation(imgpath=imgpath, xmlpath=xmlpath)
        else:
            print("Skipping file (empty xml file): {}".format(xmlpath))
