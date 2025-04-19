from logging import Logger, getLogger
from os import makedirs, path
from typing import Dict, List, final
from xml.etree.ElementTree import Element, ElementTree

from pandas import read_table

from tracklet_parser.tracklet import Tracklet


@final
class TrackletParser:
    """A parser for handling tracklet labels in KITTI format.

    This class provides functionality to:

    - Parse tracklet annotations from XML files (e.g., exported from CVAT).
    - Convert parsed tracklets into KITTI label format for use in autonomous driving datasets.

    ## Example:

    ```python
    tracklets: List[Tracklet] = TrackletParser.parse_tracklet_xml("path/to/tracklet_labels.xml")

    TrackletParser.convert_tracklets_to_kitti(
        tracklets,
        frame_list="path/to/frame_list.txt",
        output_dir="path/to/output_dir"
    )
    ```
    """
    _LOGGER: Logger = getLogger(__name__)
    _ATTRIBUTE_MAP: Dict[str, str] = {
        "h": "height",
        "w": "width",
        "l": "length",
        "tx": "x",
        "ty": "y",
        "tz": "z",
    }

    @staticmethod
    def parse_tracklet_xml(tracklet_xml: str) -> List[Tracklet]:
        """Parses annotated tracklet labels from a given XML file.

        Arguments:
            tracklet_xml (str): The path to the tracklet XML file.

        Returns:
            List[Tracklet]: A list of parsed Tracklet objects.

        Raises:
            FileNotFoundError: If the specified XML file does not exist.
            ValueError: If the XML structure is invalid or the "tracklets" element is missing.
            ParseError: If the parser fails to parse the document.
        """
        if not path.exists(tracklet_xml):
            raise FileNotFoundError(f"Tracklet XML file not found: {tracklet_xml}")

        tree = ElementTree()
        tree.parse(tracklet_xml)

        # Extract tracklet information from XML
        tracklet_elements = tree.find("tracklets")
        if tracklet_elements is None:
            raise ValueError("Invalid XML structure: 'tracklets' element not found.")
        
        tracklets: List[Tracklet] = [TrackletParser._parse_tracklet(tracklet_element) for tracklet_element in tracklet_elements if tracklet_element.tag == "item"]

        # Sort tracklets by ascending frame number
        tracklets.sort(key=lambda tracklet: tracklet.frame_number)
        return tracklets
    
    @staticmethod
    def _parse_tracklet(tracklet_element: Element) -> Tracklet:
        """Parses a single tracklet element from the XML.

        Arguments:
            tracklet_element (Element): The XML element representing a tracklet.

        Returns:
            Tracklet: The parsed Tracklet object.
        """
        tracklet = Tracklet()
        for attribute in tracklet_element:
            if attribute.tag == "objectType":
                tracklet.type = attribute.text
            elif attribute.tag in ["h", "w", "l"]:
                tracklet.put_dimension(TrackletParser._ATTRIBUTE_MAP[attribute.tag], float(attribute.text))
            elif attribute.tag == "first_frame":
                tracklet.frame_number = int(attribute.text)
            elif attribute.tag == "poses":
                pose = attribute.find("item")
                if pose is not None:
                    for pose_attribute in pose:
                        if pose_attribute.tag in ["tx", "ty", "tz"]:
                            tracklet.put_location(
                                TrackletParser._ATTRIBUTE_MAP[pose_attribute.tag], float(pose_attribute.text)
                            )
                        elif pose_attribute.tag == "rz":
                            tracklet.rotation_z = float(pose_attribute.text)
                        elif pose_attribute.tag == "occlusion":
                            tracklet.occluded = int(pose_attribute.text)
                        elif pose_attribute.tag == "truncation":
                            tracklet.truncated = float(pose_attribute.text)
        return tracklet

    @staticmethod
    def convert_tracklets_to_kitti(
        tracklets: List[Tracklet], frame_list: str, output_dir: str
    ) -> None:
        """Converts a list of tracklet objects into KITTI format and writes them to the specified output directory.

        Arguments:
            tracklets (List[Tracklet]): A list of Tracklet objects to be converted.
            frame_list (str): Path to a file containing the mapping of frame numbers to point cloud file names.
            output_dir (str): Path to the output directory where the KITTI format label files will be saved.
        """
        if not path.exists(output_dir):
            makedirs(output_dir)

        label_dict: Dict[int, str] = TrackletParser._load_frame_list(frame_list)
        frames: List[int] = []

        for tracklet in tracklets:
            label = TrackletParser._map_tracklet_to_KITTI(tracklet)
            label_file_name = label_dict.get(tracklet.frame_number, tracklet.frame_number)
            label_file = path.join(output_dir, f"{label_file_name}.txt")

            TrackletParser._write_label_to_file(label_file, label, tracklet.frame_number, frames)

    @staticmethod
    def _load_frame_list(frame_list: str) -> Dict[int, str]:
        """Loads the frame list from the given file.

        Arguments:
            frame_list (str): The frame list file path.

        Returns:
            Dict[int, str]: A dictionary mapping frame numbers to file prefixes.

        Example:
            Input (frame list):
                0 frame_0000
                1 frame_0001
                2 frame_0002

            Output:
                {0: "frame_0000", 1: "frame_0001", 2: "frame_0002"}
        """
        if not path.exists(frame_list):
            TrackletParser._LOGGER.warning(
                "CVAT frame list file not found. Label file names will be generated "
                "using numerical ascending order based on frame numbers."
            )
            return {}

        # The CVAT export includes a frame list containing frame index and
        # point cloud file mapping which can be used to create label files with
        # same naming as its corresponding point cloud file
        label_data = read_table(
            frame_list,
            sep=" ",
            names=["Frame Number", "Point Cloud File"],
            dtype=str,
        )

        return dict(zip(map(int, label_data["Frame Number"]), label_data["Point Cloud File"]))

    @staticmethod
    def _map_tracklet_to_KITTI(tracklet: Tracklet) -> str:
        """Maps a tracklet object to KITTI format.

        Arguments:
            tracklet (Tracklet): The tracklet object.

        Returns:
            str: The tracklet in KITTI format.
        """
        information = [
            tracklet.type,
            tracklet.truncated,
            tracklet.occluded,
            tracklet.alpha,
            tracklet.bbox["left"],
            tracklet.bbox["top"],
            tracklet.bbox["right"],
            tracklet.bbox["bottom"],
            tracklet.dimensions["height"],
            tracklet.dimensions["width"],
            tracklet.dimensions["length"],
            tracklet.location["x"],
            tracklet.location["y"],
            tracklet.location["z"],
            tracklet.rotation_z,
        ]
        return " ".join(map(str, information))
    
    @staticmethod
    def _write_label_to_file(label_file: str, label: str, frame_number: int, frames: List[int]) -> None:
        """Writes a label to a specified file, either appending to it or creating a new file.

        Arguments:
            label_file (str): The path to the file where the label should be written.
            label (str): The label content to write to the file.
            frame_number (int): The frame number associated with the label.
            frames (List[int]): A list of frame numbers to track which frames have been seen.
        """
        mode = "a" if frame_number in frames else "w"

        with open(label_file, mode, encoding="utf-8") as kitti_file:
            kitti_file.write(f"{label}\n")

        if frame_number not in frames:
            frames.append(frame_number)
