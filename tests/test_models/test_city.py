#!/usr/bin/python3
"""test cases of city model"""
from models.city import City
import unittest


class TestCity(unittest.TestCase):
    """
    TestState class for City class
    """
    def test_city(self):
        """
        Test City class function
        """
        my_city = City()
        self.assertEqual(my_city.name, "")
        self.assertIsInstance(my_city.name, str)

        self.assertEqual(my_city.state_id, "")
        self.assertIsInstance(my_city.state_id, str)


if __name__ == "__main__":
    unittest.main()
