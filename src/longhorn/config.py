# pylint: disable=too-few-public-methods
"""
Contains all the environment variables per build.
"""
from glob import glob
from os import getenv, urandom
from os.path import abspath, join
from secrets import token_urlsafe

# Lists containing supported values
# Options below should chose from list to prevent errors
alert_transports = [
    None,
    "email"
]
sources_of_truth = [
    None,
    "netbox"
]
ticketing_systems = [
    None,
    "faveo"
]


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
    SOURCE_OF_TRUTH = sources_of_truth[1]
    NETBOX_URL = getenv("NETBOX_URL")
    ALERT_TRANSPORT = alert_transports[1]
    NETBOX_TOKEN = getenv("NETBOX_TOKEN")
    ENGINEERS_EMAIL = "4whalj16@solent.ac.uk"
    MAIL_DEFAULT_SENDER = "longhorn@james-whale.com"


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
    ALERT_TRANSPORT = alert_transports[0]


class BrokenConfig(TestingConfig):
    """
    Variables that add to/overwrite values from the default class for the testing environment.
    """

    AUTH_TOKENS = {None: "some-user"}


config_by_name = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "broken": BrokenConfig,
}
