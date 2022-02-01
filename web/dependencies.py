from db.core import client
from utils import config


def get_db():
    return client[config.MONGO_DB]
