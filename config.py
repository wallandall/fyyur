import os
from dotenv import load_dotenv

# take environment variables from .env.
load_dotenv()

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL

SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
    os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"),  os.getenv("DB_PORT"), os.getenv("DB"))
SQLALCHEMY_TRACK_MODIFICATIONS = False
print(SQLALCHEMY_DATABASE_URI)
