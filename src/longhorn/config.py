# pylint: disable=too-few-public-methods
"""
Contains all the environment variables per build.
"""
from os import getenv, urandom


class Config:
    """
    The default variables applied to all environments.
    """
    SECRET_KEY = urandom(16)
    LOGIN_DISABLED = False
    DEFAULT_TOKEN = 'dGhpc19pc19pbnNlY3VyZQ=='
    AUTH_TOKENS = {getenv("LONGHORN_NPRD_TOKEN"): "longhorn-admin"}


class DevelopmentConfig(Config):
    """
    Variables that add to/overwrite values from the default class for the development environment.
    """
    DEBUG = True
    ENVIRONMENT = 'dev'
    FLASK_DEBUG = True
    PROCESS_TTL = 10


config_by_name = {
    "dev": DevelopmentConfig,
}
