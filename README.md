# Tracklet Parser
A parser for tracklet labels in KITTI Raw Format 1.0 created by the [Computer Vision Annotation Tool (CVAT)](https://github.com/openvinotoolkit/cvat).

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
from tracklet_parser import TrackletParser

def main():
    tracklet_labels = "C:\\Foo\\tracklet_labels.xml"
    frame_list = "C:\\Foo\\frame_list.txt"
    output_dir = "C:\\Foo\\Bar"
    
    tracklets = TrackletParser.parse_tracklet_xml(tracklet_labels)
    # Create n label text files in C:\Foo\Bar for n recordings
    TrackletParser.convert_tracklets_to_kitti(tracklets, frame_list, output_dir)

if __name__ == "__main__":
    main()
```
