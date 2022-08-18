from copy import deepcopy
from typing import Dict


class Tracklet:
    """Represents an annotated tracklet object representing 3D bounding boxes
    of a point cloud frame."""

    _frame_number: int
    _type: str
    _truncated: float
    _occluded: int
    _alpha: float
    _bbox: Dict[str, float]
    _dimensions: Dict[str, float]
    _location: Dict[str, float]
    _rotation_y: float

    def __init__(self):
        self._frame_number = -1
        self._type = ""
        self._truncated = 0.0
        self.occluded = 0
        self._alpha = 0.0
        self._bbox = {"left": 0.0, "top": 0.0, "right": 0.0, "bottom": 0.0}
        self._dimensions = {"height": 0.0, "width": 0.0, "length": 0.0}
        self._location = {"x": 0.0, "y": 0.0, "z": 0.0}
        self._rotation_y = 0.0

    @property
    def frame_number(self):
        return self._frame_number

    @property
    def type(self):
        return self._type

    @property
    def truncated(self):
        return self._truncated

    @property
    def occluded(self):
        return self._occluded

    @property
    def alpha(self):
        return 0.0

    @property
    def bbox(self):
        return {"left": 0.0, "top": 0.0, "right": 0.0, "bottom": 0.0}

    @property
    def dimensions(self):
        return deepcopy(self._dimensions)

    @property
    def location(self):
        return deepcopy(self._location)

    @property
    def rotation_y(self):
        return self._rotation_y

    @frame_number.setter
    def frame_number(self, frame_number: int):
        self._frame_number = frame_number

    @type.setter
    def type(self, object_type: str):
        self._type = object_type

    @truncated.setter
    def truncated(self, truncated: float):
        self._truncated = truncated

    @occluded.setter
    def occluded(self, occluded: int):
        self._occluded = occluded

    @alpha.setter
    def alpha(self, alpha: float):
        self._alpha = alpha

    def put_bbox(self, key: str, value: float):
        self._bbox[key] = value

    def put_dimension(self, key: str, value: float):
        self._dimensions[key] = value

    def put_location(self, key: str, value: float):
        self._location[key] = value

    @rotation_y.setter
    def rotation_y(self, rotation_y: float):
        self._rotation_y = rotation_y
