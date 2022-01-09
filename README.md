# bbox-annotation-utils

Tools for bounding box annotations

## Requirements

- Python 3.7.3
  - lxml 4.7.0
  - opencv-python 4.5.1.48

## Installation

    $ git clone git@github.com:takuya-ki/bbox-annotation-utils.git; cd bbox-annotation-utils  
    $ pip install -r requirements.txt

## Usage

1. prepare dataset/class_list.txt 
2. save image files (extension is jpg or png) into dataset/jpg/ or dataset/png/
3. save annotation txt files into dataset/txt/ (e.g. txt files used for YOLO)  
    - `$ python src/txt2xml.py`  
    - check dataset/xml generated
4. or save annotation xml files into dataset/xml/ (e.g. txt files used for SSD)  
    - `$ python src/xml2txt.py`
    - check dataset/txt generated
5. save annotated images into dataset/img/ and draw them 
    - `$ python src/draw_xml_annotation.py`
    - `$ python src/draw_txt_annotation.py` (under dev)

## Author / Contributor

[Takuya Kiyokawa](https://takuya-ki.github.io/)

## License

This software is released under the MIT License, see [LICENSE](./LICENSE).
