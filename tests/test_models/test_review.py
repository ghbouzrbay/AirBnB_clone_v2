#!/usr/bin/python3
"""test cases of review model"""
from models.review import Review
import unittest


class TestReview(unittest.TestCase):
    """
    TestReview class for Review class
    """
    def test_review(self):
        """
        Test Review class function
        """
        my_review = Review()
        self.assertEqual(my_review.place_id, "")
        self.assertIsInstance(my_review.place_id, str)

        self.assertEqual(my_review.user_id, "")
        self.assertIsInstance(my_review.user_id, str)

        self.assertEqual(my_review.text, "")
        self.assertIsInstance(my_review.text, str)


if __name__ == "__main__":
    unittest.main()
