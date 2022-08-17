# Tracklet Parser
A parser for KITTI Raw Format 1.0 tracklet labels created by the [Computer Vision Annotation Tool (CVAT). (CVAT)](https://github.com/openvinotoolkit/cvat).

[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/holtvogt/tracklet_parser/blob/master/LICENSE)
[![Python](https://img.shields.io/badge/python-3.9-blue)](https://www.python.org/downloads/)

## Installation
Assuming that you already have a working Python environment, you can install all necessary packages with

```bash
python setup.py install
```

## Usage
Creating a folder with text files in KITTI format. Each text file contains the labeling information of its corresponding recording.

```python
from tracklet_parser.tracklet_parser import parse_tracklet_xml, convert_tracklets_to_kitti

def main():
    xml = "C:\\Foo\\tracklet_labels.xml"
    output_dir = "C:\\Foo\\Bar"
    frame_list = "C:\\Foo\\frame_list.txt"
    
    tracklets = parse_tracklet_xml(xml)
    # Create n label text files in C:\Foo\Bar for n recordings
    convert_tracklets_to_kitti(tracklets, output_dir, frame_list)

if __name__ == "__main__":
    main()
```
