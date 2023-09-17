#!/usr/bin/python3
"""test cases of place model"""
from models.place import Place
import unittest


class TestPlace(unittest.TestCase):
    """
    TestPlace class for Place class
    """
    def test_place(self):
        """
        Test Place class function
        """
        my_place = Place()
        self.assertEqual(my_place.city_id, "")
        self.assertIsInstance(my_place.city_id, str)

        self.assertEqual(my_place.user_id, "")
        self.assertIsInstance(my_place.user_id, str)

        self.assertEqual(my_place.name, "")
        self.assertIsInstance(my_place.name, str)

        self.assertEqual(my_place.description, "")
        self.assertIsInstance(my_place.description, str)

        self.assertEqual(my_place.number_rooms, 0)
        self.assertIsInstance(my_place.number_rooms, int)

        self.assertEqual(my_place.number_bathrooms, 0)
        self.assertIsInstance(my_place.number_bathrooms, int)

        self.assertEqual(my_place.max_guest, 0)
        self.assertIsInstance(my_place.max_guest, int)

        self.assertEqual(my_place.price_by_night, 0)
        self.assertIsInstance(my_place.price_by_night, int)

        self.assertEqual(my_place.latitude, 0.0)
        self.assertIsInstance(my_place.latitude, float)

        self.assertEqual(my_place.longitude, 0.0)
        self.assertIsInstance(my_place.longitude, float)

        self.assertEqual(my_place.amenity_ids, [])
        self.assertIsInstance(my_place.amenity_ids, list)


if __name__ == "__main__":
    unittest.main()
