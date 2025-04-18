from os import makedirs, path
from typing import List, final
from xml.etree.ElementTree import Element, ElementTree

from pandas import read_table

from tracklet_parser.tracklet import Tracklet


@final
class TrackletParser:
    """Parser for Tracklet label parsing in KITTI format."""

    _ATTRIBUTE_MAP = {
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
            tracklet_xml (str): The tracklet XML file path

        Returns:
            List[Tracklet]: The tracklets
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
            tracklet_element (Element): The tracklet element

        Returns:
            Tracklet: The parsed tracklet
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
    ):
        """Converts tracklet objects into KITTI format.

        Arguments:
            tracklets (List[Tracklet]): The tracklet objects
            frame_list (str): The frame list containing the mapping of actual
                point cloud file names
            output_dir (str): The label folder to contain tracklets
                information in KITTI format
        """

        # Create necessary folders for text file
        if not path.exists(output_dir):
            makedirs(output_dir)

        # The CVAT export includes a frame list containing frame index and
        # point cloud file mapping which can be used to create label files with
        # same naming as its corresponding point cloud file
        if not path.exists(frame_list):
            print(
                "CVAT frame list not found: Creating label file names in"
                " numerical ascending order.. "
            )

        frames: List[int] = []
        for tracklet in tracklets:
            # Label information
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
            information = list(map(str, information))
            label = " ".join(information)

            if path.exists(frame_list):
                label_data = read_table(
                    frame_list,
                    delim_whitespace=True,
                    names=["Frame Number", "File Prefix"],
                    dtype=str,
                )
                frame_numbers = list(
                    map(int, label_data["Frame Number"].to_list())
                )
                file_prefixes = list(
                    map(str, label_data["File Prefix"].to_list())
                )
                label_dict = dict(zip(frame_numbers, file_prefixes))
                label_file_name = label_dict[tracklet.frame_number]
            else:
                label_file_name = tracklet.frame_number
            label_file = path.join(output_dir, f"{label_file_name}.txt")

            # If frame is known, append the label file with new information
            if tracklet.frame_number in frames:
                with open(
                    label_file, mode="a", encoding="utf-8"
                ) as kitti_file:
                    kitti_file.write(f"{label}\n")
            # Otherwise, create new file
            else:
                with open(
                    label_file, mode="w", encoding="utf-8"
                ) as kitti_file:
                    kitti_file.seek(0)
                    kitti_file.write(f"{label}\n")
                    kitti_file.truncate()
                frames.append(tracklet.frame_number)
