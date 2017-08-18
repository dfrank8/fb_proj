import os
from os import path

# App details
BASE_DIRECTORY = path.abspath(path.dirname(__file__))
DEBUG = True
SECRET_KEY = str(os.urandom(24))

# Database details
SQLALCHEMY_DATABASE_URI = '{0}{1}'.format('sqlite:///',
                                          path.join(BASE_DIRECTORY, 'app.db'))
