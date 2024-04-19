#!/usr/bin/python3
"""Defines unnittests for models/engine/db_storage.py."""
import models
import unittest
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Engine


class TestDBStorage(unittest.TestCase):
    """Unittests for testing the DBStorage class."""

    @classmethod
    def setUpClass(cls):
        """DBStorage testing setup.
        """
        models.storage = DBStorage()

        cls.storage = models.storage
        Base.metadata.create_all(cls.storage._DBStorage__engine)
        Session = sessionmaker(bind=cls.storage._DBStorage__engine)
        cls.storage._DBStorage__session = Session()
        cls.state = State(name="California")
        cls.storage._DBStorage__session.add(cls.state)
        cls.city = City(name="San_Jose", state_id=cls.state.id)
        cls.storage._DBStorage__session.add(cls.city)
        cls.user = User(email="poppy@holberton.com", password="betty")
        cls.storage._DBStorage__session.add(cls.user)
        cls.place = Place(city_id=cls.city.id, user_id=cls.user.id,
                          name="School")
        cls.storage._DBStorage__session.add(cls.place)
        cls.amenity = Amenity(name="Wifi")
        cls.storage._DBStorage__session.add(cls.amenity)
        cls.review = Review(place_id=cls.place.id, user_id=cls.user.id,
                            text="stellar")
        cls.storage._DBStorage__session.add(cls.review)
        cls.storage._DBStorage__session.commit()

    def test_docstrings(self):
        self.assertIsNotNone(DBStorage.__doc__)
        self.assertIsNotNone(DBStorage.all.__doc__)
        self.assertIsNotNone(DBStorage.new.__doc__)
        self.assertIsNotNone(DBStorage.save.__doc__)
        self.assertIsNotNone(DBStorage.delete.__doc__)
        self.assertIsNotNone(DBStorage.reload.__doc__)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_attributes(self):
        self.assertTrue(isinstance(self.storage._DBStorage__engine, Engine))
        self.assertTrue(isinstance(self.storage._DBStorage__session, Session))

    def test_methods(self):
        self.assertTrue(hasattr(DBStorage, "__init__"))
        self.assertTrue(hasattr(DBStorage, "all"))
        self.assertTrue(hasattr(DBStorage, "new"))
        self.assertTrue(hasattr(DBStorage, "save"))
        self.assertTrue(hasattr(DBStorage, "delete"))
        self.assertTrue(hasattr(DBStorage, "reload"))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_init(self):
        """Test initialization."""
        self.assertTrue(isinstance(self.storage, DBStorage))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_all(self):
        """Test default all method."""
        obj = self.storage.all()
        self.assertEqual(type(obj), dict)
        self.assertEqual(len(obj), len(self.storage.all()))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_new(self):
        st = State(name="Washington")
        self.storage.new(st)
        x = self.storage._DBStorage__session.query(
            State).filter(State.id == st.id).first()
        self.assertEqual(st, x)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_get(self):
        state = State(name='Albania')
        self.storage.new(state)
        x = self.storage.get(State, state.id)
        self.assertEqual(x, state)

    @unittest.skipIf(models.storage == FileStorage, 'Testing Filestorage')
    def test_count(self):
        state = State(name='another')
        self.storage.new(state)
        self.assertEqual(len(self.storage.all()), self.storage.count())
        self.assertEqual(len(self.storage.all(State)),
                         self.storage.count(State))


if __name__ == "__main__":
    unittest.main()