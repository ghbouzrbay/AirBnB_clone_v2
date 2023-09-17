#!/usr/bin/python3
"""test cases of amenity model"""
from models.amenity import Amenity
import unittest


class TestAmenity(unittest.TestCase):
    """
    TestAmenity class for Amenity class
    """
    def test_amenity(self):
        """
        Test Amenity class function
        """
        my_amenity = Amenity()
        self.assertEqual(my_amenity.name, "")
        self.assertIsInstance(my_amenity.name, str)


if __name__ == "__main__":
    unittest.main()
