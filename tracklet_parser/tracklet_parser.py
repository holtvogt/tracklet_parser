from os import makedirs, path
from typing import List, final
from xml.etree.ElementTree import ElementTree

from pandas import read_table

from tracklet import Tracklet


@final
class TrackletParser:
    """Parser for tracklet label parsing in KITTI format."""

    @staticmethod
    def parse_tracklet_xml(tracklet_xml: str) -> List[Tracklet]:
        """Parses annotated tracklet labels from a given XML file.

        Arguments:
            tracklet_xml (str): The tracklet XML file path

        Returns:
            List[Tracklet]: The tracklets
        """

        if not path.exists(tracklet_xml):
            print("No tracklet XML file found.")
            return []

        tree = ElementTree()
        tree.parse(tracklet_xml)

        # Extract tracklet information from XML
        tracklets: List[Tracklet] = []
        tracklet_elements = tree.find("tracklets")
        for tracklet_element in tracklet_elements:
            if tracklet_element.tag == "item":
                tracklet = Tracklet()
                for attribute in tracklet_element:
                    if attribute.tag == "objectType":
                        tracklet.type = attribute.text
                    elif attribute.tag == "h":
                        tracklet.put_dimension("height", float(attribute.text))
                    elif attribute.tag == "w":
                        tracklet.put_dimension("width", float(attribute.text))
                    elif attribute.tag == "l":
                        tracklet.put_dimension("length", float(attribute.text))
                    elif attribute.tag == "first_frame":
                        tracklet.frame_number = int(attribute.text)
                    elif attribute.tag == "poses":
                        for pose in attribute:
                            if pose.tag == "item":
                                for pose_attribute in pose:
                                    if pose_attribute.tag == "tx":
                                        tracklet.put_location(
                                            "x", float(pose_attribute.text)
                                        )
                                    elif pose_attribute.tag == "ty":
                                        tracklet.put_location(
                                            "y", float(pose_attribute.text)
                                        )
                                    elif pose_attribute.tag == "tz":
                                        tracklet.put_location(
                                            "z", float(pose_attribute.text)
                                        )
                                    elif pose_attribute.tag == "rz":
                                        tracklet.rotation_z = float(
                                            pose_attribute.text
                                        )
                                    elif pose_attribute.tag == "occlusion":
                                        tracklet.occluded = int(
                                            pose_attribute.text
                                        )
                                    elif pose_attribute.tag == "truncation":
                                        tracklet.truncated = float(
                                            pose_attribute.text
                                        )
                tracklets.append(tracklet)

        # Sort tracklets by ascending frame number
        tracklets.sort(key=lambda x: x.frame_number)
        return tracklets

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
