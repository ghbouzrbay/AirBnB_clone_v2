#!/usr/bin/python3
"""Defines the FileStorage class."""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """class that manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a list of objects of one type of class.

        Args:
            cls (any, optional): Class of object. Defaults to None.

        Returns:
            list: list of objects of one type of class.
        """
        if cls is None:
            return FileStorage.__objects
        return {
            key_str: arg for key_str, arg in self.__objects.items()
            if type(arg) is cls
        }

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            value = {}
            value.update(FileStorage.__objects) 
            for key_str, val in value.items():
                value[key_str] = val.to_dict()
            json.dump(value, f)

    def reload(self):
        """Loads storage dictionary from file"""
        cls = {
                    'BaseModel': BaseModel,
                    'User': User, 'Place': Place,
                    'State': State, 'City': City,
                    'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            js_file = {}
            with open(FileStorage.__file_path, 'r') as f:
                js_file = json.load(f)
                for key_str, val in temp.items():
                    self.all()[key_str] = cls[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects If obj is equal to None, the method should not do anything.
        Args:
            obj (models.class.<any model>, optional): object to delete.
            Defaults to None.
        """
        if obj in self.__objects.values():
            key_str = "{}.{}".format(type(obj).__name__, obj.id)
            del(self.__objects[key_str])
        return

    def close(self):
        """Calls reload method for deserializing the JSON file to objects
        """
        self.reload()
