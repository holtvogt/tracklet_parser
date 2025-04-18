import os
import unittest
from typing import List

from tracklet_parser.tracklet import Tracklet
from tracklet_parser.tracklet_parser import TrackletParser


class TestTrackletParser(unittest.TestCase):
    def setUp(self):
        self.example_xml_path = os.path.join(
            os.path.dirname(__file__), "resources", "example_tracklet_labels.xml"
        )

    def test_parse_tracklet_xml(self):
        tracklets: List[Tracklet] = TrackletParser.parse_tracklet_xml(self.example_xml_path)

        # Assertions
        self.assertEqual(len(tracklets), 3) # Three tracklets in the XML

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


if __name__ == "__main__":
    unittest.main()
