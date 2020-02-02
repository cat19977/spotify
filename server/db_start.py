from api.models import *
from api import db, create_app
import os
from os import path

if path.exists('api/database.db'):
    os.remove('api/database.db')

db.create_all(app=create_app())