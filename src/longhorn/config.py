# pylint: disable=too-few-public-methods
"""
Contains all the environment variables per build.
"""
from glob import glob
from os import getenv, urandom
from os.path import abspath, join
from secrets import token_urlsafe


class Config:
    """
    The default variables applied to all environments.
    """

    SECRET_KEY = urandom(16)
    LOGIN_DISABLED = False
    DEFAULT_TOKEN = token_urlsafe()
    AUTH_TOKENS = {getenv("LONGHORN_NPRD_TOKEN"): "longhorn-admin"}
    # recursively search for the processes.csv file in that path and return the absolute path
    PROCESS_FILE = abspath(
        join(abspath("."), glob("**/var/cache/processes.csv", recursive=True)[0])
    )
    SOURCE_OF_TRUTH = "netbox"
    NETBOX_URL = getenv("NETBOX_URL")
    NETBOX_TOKEN = getenv("NETBOX_TOKEN")


class DevelopmentConfig(Config):
    """
    Variables that add to/overwrite values from the default class for the development environment.
    """

    DEBUG = True
    ENVIRONMENT = "dev"
    FLASK_DEBUG = True
    PROCESS_TTL = 10


class TestingConfig(Config):
    """
    Variables that add to/overwrite values from the default class for the test environment.
    """

    DEBUG = True
    TESTING = True
    ENVIRONMENT = "test"
    PROCESS_TTL = 1
    AUTH_TOKENS = {"test": "unit-test"}
    PROCESS_FILE = "test/test_process/var/cache/test_processes.csv"


class BrokenConfig(TestingConfig):
    AUTH_TOKENS = {None: "some-user"}


config_by_name = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "broken": BrokenConfig,
}
