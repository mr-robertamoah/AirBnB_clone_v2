#!/usr/bin/python3

"""A unit test module for the console (command interpreter).
"""

import json
import MySQLdb
from os import getenv
import sqlalchemy
import unittest
from io import StringIO
from unittest.mock import patch
from typing import TextIO
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User


def clear_stream(stream: TextIO):
    """Clears the stream

    Args:
        stream (TextIO): The stream to clear.
    """
    if stream.seekable():
        stream.seek(0)
        stream.truncate(0)


class TestHBNBCommand(unittest.TestCase):
    """test class for the HBNBCommand class.
    """
    @unittest.skipIf(
        getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_create(self):
        """Tests the create command with the file storage.
        """
        with patch('sys.stdout', new=StringIO()) as c_out:
            command = HBNBCommand()
            command.onecmd('create City name="Texas"')
            _id = c_out.getvalue().strip()
            clear_stream(c_out)
            self.assertIn('City.{}'.format(mdl_id), storage.all().keys())
            command.onecmd('show City {}'.format(_id))
            self.assertIn("'name': 'Texas'", c_out.getvalue().strip())
            clear_stream(c_out)
            command.onecmd('create User name="James" age=17 height=5.9')
            _id = c_out.getvalue().strip()
            self.assertIn('User.{}'.format(mdl_id), storage.all().keys())
            clear_stream(c_out)
            command.onecmd('show User {}'.format(_id))
            self.assertIn("'name': 'James'", c_out.getvalue().strip())
            self.assertIn("'age': 17", c_out.getvalue().strip())
            self.assertIn("'height': 5.9", c_out.getvalue().strip())

    @unittest.skipIf(
        getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """Tests the create command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as c_out:
            command = HBNBCommand()
            # creating a model with non-null attribute(s)
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                command.onecmd('create User')
            # creating a User instance
            clear_stream(c_out)
            command.onecmd('create User email="robert@gmail.com" password="123456"')
            _id = c_out.getvalue().strip()
            db_con = MySQLdb.connect(
                host=getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=getenv('HBNB_MYSQL_USER'),
                passwd=getenv('HBNB_MYSQL_PWD'),
                db=getenv('HBNB_MYSQL_DB')
            )
            cursor = db_con.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('robert@gmail.com', result)
            self.assertIn('123456', result)
            cursor.close()
            db_con.close()

    @unittest.skipIf(
        getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """Tests the show command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as c_out:
            command = HBNBCommand()
            # showing a User instance
            obj = User(email="robert@gmail.com", password="123456")
            db_con = MySQLdb.connect(
                host=getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=getenv('HBNB_MYSQL_USER'),
                passwd=getenv('HBNB_MYSQL_PWD'),
                db=getenv('HBNB_MYSQL_DB')
            )
            cursor = db_con.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is None)
            command.onecmd('show User {}'.format(obj.id))
            self.assertEqual(
                c_out.getvalue().strip(),
                '** no instance found **'
            )
            obj.save()
            db_con = MySQLdb.connect(
                host=getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=getenv('HBNB_MYSQL_USER'),
                passwd=getenv('HBNB_MYSQL_PWD'),
                db=getenv('HBNB_MYSQL_DB')
            )
            cursor = db_con.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            clear_stream(c_out)
            command.onecmd('show User {}'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('robert@gmail.com', result)
            self.assertIn('123456', result)
            self.assertIn('robert@gmail.com', c_out.getvalue())
            self.assertIn('123456', c_out.getvalue())
            cursor.close()
            db_con.close()

    @unittest.skipIf(
        getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """Tests the count command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as c_out:
            command = HBNBCommand()
            db_con = MySQLdb.connect(
                host=getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=getenv('HBNB_MYSQL_USER'),
                passwd=getenv('HBNB_MYSQL_PWD'),
                db=getenv('HBNB_MYSQL_DB')
            )
            cursor = db_con.cursor()
            cursor.execute('SELECT COUNT(*) FROM states;')
            res = cursor.fetchone()
            prev_count = int(res[0])
            command.onecmd('create State name="Enugu"')
            clear_stream(c_out)
            command.onecmd('count State')
            cnt = c_out.getvalue().strip()
            self.assertEqual(int(cnt), prev_count + 1)
            clear_stream(c_out)
            command.onecmd('count State')
            cursor.close()
            db_con.close()
