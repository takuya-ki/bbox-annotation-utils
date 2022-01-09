# bbox-annotation-utils

Tools for bounding box annotations

## Requirements

- Python 3.7.3
  - lxml 4.7.0
  - opencv-python 4.5.1.48

## Installation

    $ git clone git@github.com:takuya-ki/bbox-annotation-utils.git  
    $ pip install -r requirements.txt

## Usage

1. Prepare dataset/class_list.txt  
2. Put annotation txt files into dataset/txt/ (e.g. txt files used for YOLO)  
    `$ python src/txt2xml.py`  
3. or put annotation xml files into dataset/xml/ (e.g. txt files used for SSD)  
    `$ python src/xml2txt.py`

## Author / Contributor

[Takuya Kiyokawa](https://takuya-ki.github.io/)

## License

This software is released under the MIT License, see [LICENSE](./LICENSE).
