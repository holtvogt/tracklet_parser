# Tracklet Parser

[![license](https://img.shields.io/badge/license-MIT-green)](https://github.com/holtvogt/tracklet_parser/blob/develop/LICENSE.txt)
[![python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/downloads/)
[![black](https://img.shields.io/badge/style-black-black)](https://github.com/psf/black)

A parser for tracklet labels in KITTI Raw Format 1.0 created by the [Computer Vision Annotation Tool (CVAT)](https://github.com/openvinotoolkit/cvat).

## Installation

Assuming that you already have a working Python environment, you can install all necessary packages with

```bash
pip install tracklet-parser
```

## Usage

Creating a folder with text files in KITTI format. Each text file contains the labeling information of its corresponding recording.

```python
from tracklet_parser.tracklet import Tracklet
from tracklet_parser.tracklet_parser import TrackletParser

def main():
    tracklet_labels: str = "C:\\Foo\\tracklet_labels.xml"
    frame_list: str = "C:\\Foo\\frame_list.txt"
    output_dir: str = "C:\\Foo\\Bar"

    tracklets: List[Tracklet] = TrackletParser.parse_tracklet_xml(tracklet_labels)
    # Create n label text files in C:\Foo\Bar for n (labeled) recordings
    TrackletParser.convert_tracklets_to_kitti(tracklets, frame_list, output_dir)

if __name__ == "__main__":
    main()
```
