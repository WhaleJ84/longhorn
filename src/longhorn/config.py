# pylint: disable=too-few-public-methods
"""
Contains all the environment variables per build.
"""
from os import getenv, urandom
from secrets import token_urlsafe


class Config:
    """
    The default variables applied to all environments.
    """
    SECRET_KEY = urandom(16)
    LOGIN_DISABLED = False
    DEFAULT_TOKEN = token_urlsafe()
    AUTH_TOKENS = {getenv("LONGHORN_NPRD_TOKEN"): "longhorn-admin"}


class DevelopmentConfig(Config):
    """
    Variables that add to/overwrite values from the default class for the development environment.
    """
    DEBUG = True
    ENVIRONMENT = 'dev'
    FLASK_DEBUG = True
    PROCESS_TTL = 10


class TestingConfig(Config):
    """
    Variables that add to/overwrite values from the default class for the test environment.
    """
    DEBUG = True
    TESTING = True
    ENVIRONMENT = 'test'
    PROCESS_TTL = 1
    AUTH_TOKENS = {"test": "unit-test"}


config_by_name = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
}
