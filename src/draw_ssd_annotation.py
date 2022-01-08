#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import cv2
import glob
import os.path as osp
from lxml import etree


# extract especially object true data
class ssd_annotation_xml(object):

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


def scale_to_width(img, width):
    scale = width / img.shape[1]
    return cv2.resize(img, dsize=None, fx=scale, fy=scale)


def draw_annotation(image_paths, xml_dirpath):
    for i, image_path in enumerate(image_paths):
        image = cv2.imread(image_path)

        xml_path = osp.join(
            xml_dirpath,
            osp.splitext(osp.basename(image_path))[0]+'.xml')
        if not osp.isfile(xml_path):
            print(xml_path + " is not existed, \
                  so this process will be continued.")
            exit()

        ssd_anno_xml = ssd_annotation_xml(xml_path)
        labels, bboxs = ssd_anno_xml.get_bbox(image.shape)

        # draw and view
        drawed = image.copy()
        for i, (label, bbox) in enumerate(zip(labels, bboxs)):
            # color = np.uint8(np.random.uniform(0, 255, 3))
            # c = tuple(map(int, color))
            # c = (255,255,255)
            if label == 'PlasticBottle':
                c = (0, 255, 0)
                label = 'Plastic bottle'
            elif label == 'Can':
                c = (255, 102, 153)
                label = 'Aluminum can'
            elif label == 'Bottle':
                c = (0, 153, 255)
                label = 'Glass bottle'

            text_pos = (int(bbox[0]), int(bbox[1]) - 10)
            cv2.putText(
                drawed, label, text_pos, cv2.FONT_HERSHEY_PLAIN, 3.5, c, 5)
            cv2.rectangle(
                drawed,
                (int(bbox[2]), int(bbox[3])), (int(bbox[0]), int(bbox[1])),
                c, 2)
            cv2.circle(
                drawed, (int(bbox[2]), int(bbox[3])), 10, c, -1)
            cv2.circle(
                drawed, (int(bbox[0]), int(bbox[3])), 10, c, -1)
            cv2.circle(
                drawed, (int(bbox[0]), int(bbox[1])), 10, c, -1)
            cv2.circle(
                drawed, (int(bbox[2]), int(bbox[1])), 10, c, -1)

        cv2.imshow("drawed", scale_to_width(drawed, 1000))
        cv2.imwrite(osp.join(
            dataset_dirpath,
            'result',
            osp.splitext(osp.basename(image_path))[0]+'.'+imgext),
            drawed)
        if cv2.waitKey(0) & 0xff == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':

    imgext = 'jpg'
    dataset_dirpath = osp.join(
        osp.dirname(__file__), "..", "dataset")
    image_paths = glob.glob(osp.join(
        dataset_dirpath, imgext, '*.'+imgext))
    xml_dirpath = osp.join(dataset_dirpath, "xml")
    draw_annotation(image_paths=image_paths, xml_dirpath=xml_dirpath)
