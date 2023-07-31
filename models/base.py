import os
import peewee
from peewee import *
from dotenv import load_dotenv
from utils.import_helper import ImportHelper

if os.getenv("isloaded", "false").lower() != "true":
    load_dotenv()


class Database:
    def __init__(self, database=None) -> None:
        self.database = database
        if self.database is None:
            self.load_database()
        self.Model = self.get_model_class()

    def load_database(self):
        self.database_name = os.getenv("database_name")
        self.database_engine = os.getenv("database_engine")
        if not self.database_name or not self.database_engine:
            raise ImproperlyConfigured(
                'Please specify a "name" and "engine" for your database'
            )
        try:
            self.database_class = ImportHelper.load_class(self.database_engine)
            assert issubclass(self.database_class, peewee.Database)
        except ImportError:
            raise ImproperlyConfigured('Unable to import: "%s"' % self.database_engine)
        except AttributeError:
            raise ImproperlyConfigured(
                'Database engine not found: "%s"' % self.database_engine
            )
        except AssertionError:
            raise ImproperlyConfigured(
                'Database engine not a subclass of peewee.Database: "%s"'
                % self.database_engine
            )
        self.database_config = eval(os.getenv("database_config"))
        self.database = self.database_class(self.database_name, **self.database_config)

    def get_model_class(self):
        class BaseModel(Model):
            class Meta:
                database = self.database

        return BaseModel

    def connect_db(self):
        if self.database.is_closed():
            self.database.connect()

    def close_db(self):
        if not self.database.is_closed():
            self.database.close()

    def __enter__(self):
        self.connect_db()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close_db()


db = Database()
