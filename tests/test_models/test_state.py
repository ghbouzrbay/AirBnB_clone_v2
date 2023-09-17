#!/usr/bin/python3
"""test cases of state model"""
from models.state import State
import unittest


class TestState(unittest.TestCase):
    """
    TestState class for State class
    """
    def test_state(self):
        """
        Test State class function
        """
        my_state = State()
        self.assertEqual(my_state.name, "")
        self.assertIsInstance(my_state.name, str)


if __name__ == "__main__":
    unittest.main()
