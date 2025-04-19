import os
import unittest
from tempfile import TemporaryDirectory
from typing import List
from xml.etree.ElementTree import ParseError

from tracklet_parser.tracklet import Tracklet
from tracklet_parser.tracklet_parser import TrackletParser


class TestTrackletParser(unittest.TestCase):
    def setUp(self):
        # Paths to example resources
        self.example_xml_path = os.path.join(
            os.path.dirname(__file__), "resources", "example_tracklet_labels.xml"
        )
        self.example_frame_list_path = os.path.join(
            os.path.dirname(__file__), "resources", "example_frame_list.txt"
        )
        self.temp_dir = TemporaryDirectory()
        self.example_output_dir = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parse_tracklet_xml(self):
        """Test parsing a valid tracklet XML file."""
        tracklets: List[Tracklet] = TrackletParser.parse_tracklet_xml(self.example_xml_path)
        self.assertEqual(len(tracklets), 3)

        # First Tracklet
        tracklet1 = tracklets[0]
        self.assertEqual(tracklet1.type, "Pedestrian")
        self.assertEqual(tracklet1.dimensions["height"], 0.56)
        self.assertEqual(tracklet1.dimensions["width"], 0.72)
        self.assertEqual(tracklet1.dimensions["length"], 1.71)
        self.assertEqual(tracklet1.frame_number, 42)
        self.assertEqual(tracklet1.location["x"], 0.85)
        self.assertEqual(tracklet1.location["y"], -1.34)
        self.assertEqual(tracklet1.location["z"], -1.61)
        self.assertEqual(tracklet1.rotation_z, 0.0)
        self.assertEqual(tracklet1.occluded, 1)
        self.assertEqual(tracklet1.truncated, 0.1)

        # Second Tracklet
        tracklet2 = tracklets[1]
        self.assertEqual(tracklet2.type, "Car")
        self.assertEqual(tracklet2.dimensions["height"], 1.50)
        self.assertEqual(tracklet2.dimensions["width"], 1.80)
        self.assertEqual(tracklet2.dimensions["length"], 4.20)
        self.assertEqual(tracklet2.frame_number, 100)
        self.assertEqual(tracklet2.location["x"], 5.0)
        self.assertEqual(tracklet2.location["y"], 2.0)
        self.assertEqual(tracklet2.location["z"], 0.0)
        self.assertEqual(tracklet2.rotation_z, 1.57)
        self.assertEqual(tracklet2.occluded, 2)
        self.assertEqual(tracklet2.truncated, 0.5)

        # Third Tracklet (Edge Case)
        tracklet3 = tracklets[2]
        self.assertEqual(tracklet3.type, "Cyclist")
        self.assertEqual(tracklet3.dimensions["height"], 1.70)
        self.assertEqual(tracklet3.dimensions["width"], 0.60)
        self.assertEqual(tracklet3.dimensions["length"], 1.90)
        self.assertEqual(tracklet3.frame_number, 200)
        self.assertEqual(tracklet3.location["x"], 0.0) # Default value
        self.assertEqual(tracklet3.location["y"], 0.0) # Default value
        self.assertEqual(tracklet3.location["z"], 0.0) # Default value
        self.assertEqual(tracklet3.rotation_z, 0.0) # Default value
        self.assertEqual(tracklet3.occluded, 0) # Default value
        self.assertEqual(tracklet3.truncated, 0.0) # Default value

    def test_parse_tracklet_xml_file_not_found(self):
        """Test parsing a non-existent XML file."""
        with self.assertRaises(FileNotFoundError):
            TrackletParser.parse_tracklet_xml("non_existent_file.xml")

    def test_parse_tracklet_xml_invalid_structure(self):
        """Test parsing an XML file with an invalid structure."""
        invalid_xml_path = self._create_temp_file("<invalid_root></invalid_root>")
        with self.assertRaises(ValueError):
            TrackletParser.parse_tracklet_xml(invalid_xml_path)

    def test_parse_tracklet_xml_empty_file(self):
        """Test parsing an empty XML file."""
        empty_xml_path = self._create_temp_file("")
        with self.assertRaises(ParseError):
            TrackletParser.parse_tracklet_xml(empty_xml_path)

    def test_load_frame_list_empty_dict(self):
        """Test loading a non-existent frame list."""
        label_dict = TrackletParser._load_frame_list("non_existent_frame_list.txt")
        self.assertEqual(label_dict, {})

    def test_convert_tracklets_to_kitti(self):
        """Test converting tracklets to KITTI format."""
        tracklets: List[Tracklet] = TrackletParser.parse_tracklet_xml(self.example_xml_path)
        TrackletParser.convert_tracklets_to_kitti(
            tracklets, self.example_frame_list_path, self.example_output_dir
        )

        # Check if expected files are created
        expected_files = ["point_cloud_042.txt", "point_cloud_100.txt", "point_cloud_200.txt"]
        for file_name in expected_files:
            self.assertTrue(os.path.exists(os.path.join(self.example_output_dir, file_name)))

    def test_convert_tracklets_to_kitti_empty_tracklets(self):
        """Test converting an empty list of tracklets."""
        TrackletParser.convert_tracklets_to_kitti([], self.example_frame_list_path, self.example_output_dir)
        # Ensure no files are created
        self.assertEqual(len(os.listdir(self.example_output_dir)), 0)

    def _create_temp_file(self, content: str) -> str:
        """Helper method to create a temporary file with the given content."""
        temp_file = os.path.join(self.temp_dir.name, "temp_file.xml")
        with open(temp_file, "w") as file:
            file.write(content)
        return temp_file


if __name__ == "__main__":
    unittest.main()
