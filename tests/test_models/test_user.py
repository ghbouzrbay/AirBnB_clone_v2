#!/usr/bin/python3
"""defines a test class to test user model in this project"""
import unittest
import sys
import io
import time
from datetime import datetime
from models.user import User


class TestUser(unittest.TestCase):
    """
    Test class for the User class.
    """

    def test_initialization(self):
        """
        Test initialization of User instances.
        """
        user = User()
        self.assertIsInstance(user, User)
        self.assertIsInstance(user.id, str)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)
        self.assertIsInstance(user.first_name, str)
        self.assertIsInstance(user.last_name, str)
        self.assertIsInstance(user.email, str)
        self.assertIsInstance(user.password, str)

    def test_to_dict_method(self):
        """
        Test the to_dict method of User instances.
        """
        user = User()
        user.first_name = "adam"
        user.last_name = "yonatan"
        user.email = "yona@gmail.com"
        user.password = "123"

        user_dict = user.to_dict()
        user2 = User()

        self.assertIsInstance(user_dict, dict)
        self.assertIn("__class__", user_dict)
        self.assertIn("id", user_dict)
        self.assertIn("created_at", user_dict)
        self.assertIn("updated_at", user_dict)
        self.assertIn("first_name", user_dict)
        self.assertIn("last_name", user_dict)
        self.assertIn("email", user_dict)
        self.assertIn("password", user_dict)

        self.assertEqual(user_dict["__class__"], "User")
        self.assertEqual(user_dict["id"], user.id)
        self.assertEqual(user_dict["first_name"], user.first_name)
        self.assertEqual(user_dict["last_name"], user.last_name)
        self.assertEqual(user_dict["email"], user.email)
        self.assertEqual(user_dict["password"], user.password)
        self.assertEqual(
            user_dict["created_at"], user.created_at.isoformat()
        )
        self.assertEqual(
            user_dict["updated_at"], user.updated_at.isoformat()
        )
        self.assertIsNot(user, user2)
        self.assertNotEqual(user2.id, user.id)
        initial_updated_at = user2.updated_at
        user2.save()
        self.assertNotEqual(initial_updated_at, user2.updated_at)

    def test_print(self):
        """
        Test function that print
        """
        usr = User()
        usr2 = User(**usr.to_dict())
        usr_print = io.StringIO()
        sys.stdout = usr_print
        print(usr)
        sys.stdout = sys.__stdout__
        test_str = f"[User] ({usr.id}) {usr.__dict__}"
        self.maxDiff = None
        usr_print.truncate(len(test_str))
        self.assertEqual(usr_print.getvalue(), test_str)


if __name__ == "__main__":
    unittest.main()
