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
    _rotation_z: float

    def __init__(self):
        self._frame_number = -1
        self._type = ""
        self._truncated = 0.0
        self._occluded = 0
        self._alpha = 0.0
        self._bbox = {"left": 0.0, "top": 0.0, "right": 0.0, "bottom": 0.0}
        self._dimensions = {"height": 0.0, "width": 0.0, "length": 0.0}
        self._location = {"x": 0.0, "y": 0.0, "z": 0.0}
        self._rotation_z = 0.0

    @property
    def frame_number(self) -> int:
        """Get the frame number. This represents the index of the recording
        within the dataset.

        Returns:
            int: The frame number
        """

        return self._frame_number

    @property
    def type(self) -> str:
        """Get the object type. This can be 'Pedestrian', 'Cyclist',..

        Returns:
            str: The object type
        """

        return self._type

    @property
    def truncated(self) -> float:
        """Get the truncation state. This is a range from 0 (non-truncated) to
        1 (truncated) where truncated refers to the object leaving image
        boundaries.

        Returns:
            float: The truncation state
        """

        return self._truncated

    @property
    def occluded(self) -> int:
        """Get the occlusion state.

        - 0: Fully visible
        - 1: Partly occluded
        - 2: Largely occluded
        - 3: Unknown

        Returns:
            int: The occlusion state
        """

        return self._occluded

    @property
    def alpha(self) -> float:
        """Get the observation angle `alpha` of the object ranging from [-PI,
        PI].

        Returns:
            float: The observation angle
        """

        return self._alpha

    @property
    def bbox(self) -> Dict[str, float]:
        """Get the 2D bounding box of the object in the image and contains
        left.

        , top, right, bottom pixel coordinates.

        Returns:
            Dict[str, float]: The 2D bounding box
        """

        return deepcopy(self._bbox)

    @property
    def dimensions(self) -> Dict[str, float]:
        """The 3D object dimensions height, width and length (in meters).

        Returns:
            Dict[str, float]: The 3D object dimensions
        """

        return deepcopy(self._dimensions)

    @property
    def location(self) -> Dict[str, float]:
        """The 3D object location x, y and z in LiDAR coordinates (in meters).

        Returns:
            Dict[str, float]: The 3D object location
        """

        return deepcopy(self._location)

    @property
    def rotation_z(self) -> float:
        """The rotation around Y-axis in camera coordinates ranging from [-PI,
        PI].

        Note: Keep in mind that this is in camera coordinates!

        Returns:
            float: The rotation angle around Y-axis
        """

        return self._rotation_z

    @frame_number.setter
    def frame_number(self, frame_number: int):
        """Set the frame number.

        Arguments:
            frame_number (int): The frame number
        """

        self._frame_number = frame_number

    @type.setter
    def type(self, object_type: str):
        """Set the object type.

        Arguments:
            object_type (str): The object type
        """

        self._type = object_type

    @truncated.setter
    def truncated(self, truncated: float):
        """Set the truncation state.

        Arguments:
            truncated (float): The truncation state
        """

        if not 0 <= truncated <= 1:
            raise ValueError(
                f"{truncated} is an unknown truncation representative."
            )
        self._truncated = truncated

    @occluded.setter
    def occluded(self, occluded: int):
        """Set the occlusion state.

        Arguments:
            occluded (int): The occlusion state
        """

        if not 0 <= occluded <= 3:
            raise ValueError(
                f"{occluded} is an unknown occlusion representative."
            )
        self._occluded = occluded

    @alpha.setter
    def alpha(self, alpha: float):
        """Set the observation angle of the object.

        Arguments:
            alpha (float): The observation angle of the object
        """

        self._alpha = alpha

    def put_bbox(self, key: str, value: float):
        """Set a new pixel coordinate for the 2D bounding box.

        Arguments:
            key (str): The 2D bounding orientation (left, top, right, bottom)
            value (str): The pixel coordinate
        """

        self._bbox[key] = value

    def put_dimension(self, key: str, value: float):
        """Set a new dimension value for the 3D object.

        Arguments:
            key (str): The dimension direction (height, width, length)
            value (str): The dimension value
        """

        self._dimensions[key] = value

    def put_location(self, key: str, value: float):
        """Set a new coordinate for the 3D object.

        Arguments:
            key (str): The axis (x, y, z)
            value (str): The coordinate
        """

        self._location[key] = value

    @rotation_z.setter
    def rotation_z(self, rotation_z: float):
        """Set the rotation angle.

        Arguments:
            rotation_z (float). The rotation angle
        """

        self._rotation_z = rotation_z
