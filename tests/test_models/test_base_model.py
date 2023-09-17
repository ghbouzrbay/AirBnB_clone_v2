#!/usr/bin/python3
"""defines a test class to test models in this project"""
import unittest
import time
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import models


class TestBaseModel(unittest.TestCase):
    """
    Test class for the BaseModel class.
    """

    def test_initialization(self):
        """
        Test initialization of BaseModel instances.
        """
        base_model = BaseModel()
        self.assertIsInstance(base_model, BaseModel)
        self.assertIsInstance(base_model.id, str)
        self.assertIsInstance(base_model.created_at, datetime)
        self.assertIsInstance(base_model.updated_at, datetime)

    def test_functionality(self):
        """
        Test the should pass functionality cases of BaseModel """
        obj = BaseModel()
        self.assertIsInstance(obj, BaseModel)
        time.sleep(1)
        obj.name = "First_Model"
        obj2 = BaseModel(**obj.to_dict())
        self.assertEqual(obj.id, obj.to_dict()["id"])
        self.assertEqual(obj2.id, obj2.to_dict()["id"])
        self.assertIsNot(obj, obj2)
        self.assertEqual(obj2.id, obj.id)
        self.assertIn("name", obj.to_dict().keys())
        self.assertEqual(obj.name, obj.to_dict()["name"])
        self.assertNotEqual(obj.created_at, obj.updated_at)
        initial_updated_at = obj2.updated_at
        obj2.save()
        self.assertNotEqual(initial_updated_at, obj2.updated_at)

    def test_str_representation(self):
        """
        Test string representation of BaseModel instances.
        """
        base_model = BaseModel()
        expected_str = f"[BaseModel] ({base_model.id}) {base_model.__dict__}"
        self.assertEqual(str(base_model), expected_str)

    def test_to_dict_method(self):
        """
        Test the to_dict method of BaseModel instances.
        """
        base_model = BaseModel()
        base_model_dict = base_model.to_dict()

        self.assertIsInstance(base_model_dict, dict)
        self.assertIn("__class__", base_model_dict)
        self.assertIn("id", base_model_dict)
        self.assertIn("created_at", base_model_dict)
        self.assertIn("updated_at", base_model_dict)

        self.assertEqual(base_model_dict["__class__"], "BaseModel")
        self.assertEqual(base_model_dict["id"], base_model.id)
        self.assertEqual(
            base_model_dict["created_at"], base_model.created_at.isoformat()
        )
        self.assertEqual(
            base_model_dict["updated_at"], base_model.updated_at.isoformat()
        )
        """File Storage"""
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
