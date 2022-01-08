# bbox-annotation-utils

Tools for annotation of 2d object detection.

## Requirements

- Python 3.7.3
  - lxml 4.5.0
  - Pillow 7.0.0
  - opencv-python 3.4.9.33

## Installation

    $ git clone git@github.com:takuya-ki/bbox-annotation-utils.git  

## Usage

1. Prepare dataset/class_list.txt  
2. Put annotation txt files for YOLO into dataset/txt/  
    `$ python src/txt2xml.py`  
3. or put annotation xml files for SSD into dataset/xml/  
    `$ python src/xml2txt.py`
4. Put annotated images into dataset/img/ and draw them with xml file  
    `$ python src/draw_ssd_annotation.py`

## Author

[Takuya Kiyokawa](https://takuya-ki.github.io/)
