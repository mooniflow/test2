import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db')) # database가 어디에 있는가를 찾는다. 지정한다?
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"