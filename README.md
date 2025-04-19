# Tracklet Parser

[![license](https://img.shields.io/badge/license-MIT-green)](https://github.com/holtvogt/tracklet_parser/blob/develop/LICENSE.txt)
[![python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/downloads/)
[![black](https://img.shields.io/badge/style-black-black)](https://github.com/psf/black)

A parser for tracklet labels in KITTI Raw Format 1.0 created by the [Computer Vision Annotation Tool (CVAT)](https://github.com/openvinotoolkit/cvat).

## Table of Contents

- [Tracklet Parser](#tracklet-parser)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Testing](#testing)
  - [Contributing](#contributing)

## Installation

Install the package directly using `pip` from [PyPI](https://pypi.org/):

```bash
pip install tracklet-parser
```

## Usage

To use the `tracklet-parser`, you need a `tracklet_labels.xml` file and, optionally, a `frame_list.txt` file that maps frame indices to point cloud file names. The parser generates one KITTI format label file per frame, storing them in the specified output directory.

Creating KITTI format label files from tracklet data is straightforward with the `tracklet-parser`. Each output file corresponds to a single frame and contains labeling information for all detected objects in that frame (e.g., `Car`, `Pedestrian`, etc.).

Here is an example script demonstrating how to parse a `tracklet_labels.xml` file and convert the tracklet data into KITTI format label files:

```python
from tracklet_parser.tracklet import Tracklet
from tracklet_parser.tracklet_parser import TrackletParser

def main():
    tracklet_labels: str = "path/to/tracklet_labels.xml"
    frame_list: str = "path/to/frame_list.txt"
    output_dir: str = "path/to/output_dir"

    tracklets: List[Tracklet] = TrackletParser.parse_tracklet_xml(tracklet_labels)
    # Create n label text files in path/to/output_dir for n (labeled) recordings in KITTI format
    TrackletParser.convert_tracklets_to_kitti(tracklets, frame_list, output_dir)

if __name__ == "__main__":
    main()
```

## Testing

To run the tests, use the following command:

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a clear description of your changes.

Please ensure your code adheres to the [Black](https://github.com/psf/black) coding style.
