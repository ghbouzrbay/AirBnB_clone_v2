#!/usr/bin/python3
"""defines test cases of file_storage.py"""
import unittest
import models
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    """
    TestFileSrotage to test FileStorage class
    """

    def test_all(self):
        """
        testing all() function
        """
        self.assertEqual(FileStorage._FileStorage__file_path, "file.json")
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)
        test_base = BaseModel()
        self.assertIsInstance(models.storage, FileStorage)
        self.assertIsInstance(models.storage.all(), dict)
        self.assertIs(test_base in models.storage.all().values(), True)

    def test_save_reload_new_file(self):
        """
        testing save reload functions
        """
        FileStorage._FileStorage__objects = {}
        self.assertEqual(models.storage.all(), {})
        test2_base = BaseModel()
        models.storage.save()
        models.storage.reload()
        self.assertNotEqual(models.storage.all(), {})
        dict_base2 = test2_base.to_dict()
        test3_base = BaseModel(**dict_base2)
        models.storage.new(test3_base)
        self.assertIsNot(test3_base, test2_base)
        self.assertIsInstance(test3_base, BaseModel)
        base_model = BaseModel()
        dict_base_model = base_model.to_dict()
        base_model.save()
        second_dict = base_model.to_dict()
        self.assertNotEqual(dict_base_model, second_dict)


if __name__ == "__main__":
    unittest.main()
