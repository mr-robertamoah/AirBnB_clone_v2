#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models import storage
import os


class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove(self.file_path)
        except Exception:
            pass

    def setUp(self):
        """ called before each test """

        self.file_path = "file.json"
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_initialization(self):
        """ test what happens on the initialization of instance """

        self.assertFalse(os.path.exists(self.file_path))
        storage = FileStorage()
        self.assertFalse(os.path.exists(self.file_path))

    def test_all_instance_method(self):
        """ tests the all instance method on the FileStorage instance """

        storage = FileStorage()
        all_objects = storage.all()
        self.assertIsInstance(all_objects, dict)
        all_objects_len = len(all_objects)
        self.assertTrue(len(all_objects) == all_objects_len)

        model1 = BaseModel()
        all_objects = storage.all()
        self.assertTrue(len(all_objects) == 1 + all_objects_len)
        self.assertIn(model1, all_objects.values())

        model2 = BaseModel()
        all_objects = storage.all()
        self.assertTrue(len(all_objects) == 2 + all_objects_len)
        self.assertIn(model2, all_objects.values())

        with self.assertRaises(TypeError):
            storage.all("name")

    def test_new_instance_method(self):
        """ tests the new instance method on the FileStorage instance """

        storage = FileStorage()
        all_objects = storage.all()
        self.assertIsInstance(all_objects, dict)
        all_objects_len = len(all_objects)
        self.assertTrue(len(all_objects) == all_objects_len)

        model1 = BaseModel()
        all_objects = storage.all()
        self.assertTrue(len(all_objects) == 1 + all_objects_len)
        self.assertIn(model1, all_objects.values())

        model2 = BaseModel(**model1.to_dict())
        all_objects = storage.all()
        self.assertNotIn(model2, all_objects.values())
        self.assertTrue(len(all_objects) == 1 + all_objects_len)
        model2.id = str(uuid.uuid4())
        storage.new(model2)
        all_objects = storage.all()
        self.assertTrue(len(all_objects) == 2 + all_objects_len)
        self.assertIn(model2, all_objects.values())

        with self.assertRaises(TypeError):
            storage.new()

        with self.assertRaises(TypeError):
            storage.all(model1, model2)

        with self.assertRaises(AttributeError):
            storage.new("string")

        with self.assertRaises(AttributeError):
            storage.new(1)

        with self.assertRaises(AttributeError):
            storage.new({"a": 12})

        with self.assertRaises(AttributeError):
            storage.new((1, 2))

        with self.assertRaises(AttributeError):
            storage.new(1.5)

    def test_save_instance_method(self):
        """ tests the save instance method on the FileStorage instance """

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        storage = FileStorage()
        all_objects = storage.all()
        all_objects_len = len(all_objects)

        # saving with storage directly
        model1 = BaseModel()
        all_objects = storage.all()
        self.assertTrue(len(all_objects) == 1 + all_objects_len)
        self.assertIn(model1, all_objects.values())

        self.assertFalse(os.path.exists(self.file_path))
        storage.save()
        self.assertTrue(os.path.exists(self.file_path))

        with open(self.file_path, "r") as file:
            models_dict = json.load(file)
            key = model1.__class__.__name__ + "." + model1.id
            self.assertEqual(model1.to_dict(), models_dict[key])

        # saving with storage using model
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        model1 = BaseModel()
        all_objects = storage.all()
        self.assertTrue(len(all_objects) == 2 + all_objects_len)
        self.assertIn(model1, all_objects.values())

        self.assertFalse(os.path.exists(self.file_path))
        model1.save()
        self.assertTrue(os.path.exists(self.file_path))

        with open(self.file_path, "r") as file:
            models_dict = json.load(file)
            key = model1.__class__.__name__ + "." + model1.id
            self.assertEqual(model1.to_dict(), models_dict[key])

        with self.assertRaises(TypeError):
            storage.save(1.5)

    def test_save_instance_method(self):
        """ tests the save instance method on the FileStorage instance """

        storage = FileStorage()
        all_objects = storage.all()
        all_objects_len = len(all_objects)

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        storage.reload()

        self.assertTrue(all_objects_len == len(storage.all()))

        # saving with storage directly
        model1 = BaseModel()
        all_objects = storage.all()
        self.assertTrue(len(all_objects) == 1 + all_objects_len)
        self.assertIn(model1, all_objects.values())

        self.assertFalse(os.path.exists(self.file_path))
        storage.save()
        self.assertTrue(os.path.exists(self.file_path))

        storage.reload()
        key = model1.__class__.__name__ + "." + model1.id
        self.assertEqual(model1.id, storage.all()[key].id)

        # saving with storage using model
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        model1 = BaseModel()
        all_objects = storage.all()
        self.assertTrue(len(all_objects) == 2 + all_objects_len)
        self.assertIn(model1, all_objects.values())

        self.assertFalse(os.path.exists(self.file_path))
        model1.save()
        self.assertTrue(os.path.exists(self.file_path))

        storage.reload()
        key = model1.__class__.__name__ + "." + model1.id
        self.assertEqual(model1.id, storage.all()[key].id)

        with self.assertRaises(TypeError):
            storage.reload(1.5)
