import os
import configparser

_config = configparser.ConfigParser()
_config.read("config.ini", encoding="utf-8")


def _get_from_config_or_env(key: str) -> str:
    result = _config["DEFAULT"].get(key)
    if not result:
        result = os.environ[key]
    return result


MOTOR_URI = _get_from_config_or_env("motor_uri")
MONGO_DB = _get_from_config_or_env("mongo_db")
GET_ENTITIES_DEFAULT_LIMIT = int(_get_from_config_or_env("get_entities_default_limit"))
DEBUG = bool(int(_get_from_config_or_env("debug")))
TEST_MONGO_DB = _get_from_config_or_env("test_mongo_db")
