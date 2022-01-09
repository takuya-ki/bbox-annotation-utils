# bbox-annotation-utils

Tools for bounding box annotations

## Requirements

- Python 3.7.3
  - lxml 4.7.0
  - Pillow 8.4.0
  - opencv-python 4.5.1.48

## Installation

    $ git clone git@github.com:takuya-ki/bbox-annotation-utils.git  
    $ pip install -r requirements.txt

## Usage

1. Prepare dataset/class_list.txt  
2. Put annotation txt files for YOLO into dataset/txt/  
    `$ python src/txt2xml.py`  
3. or put annotation xml files for SSD into dataset/xml/  
    `$ python src/xml2txt.py`
4. Put annotated images into dataset/img/ and draw them 
    `$ python src/draw_ssd_annotation.py`

## Author / Contributor

[Takuya Kiyokawa](https://takuya-ki.github.io/)

## License

This software is released under the MIT License, see [LICENSE](./LICENSE).
