"""
Imports the modules necessary to build the Flask application.
Module contains the `create_app` method to build the appropriate environment.
"""
from flask import Flask
from flask.logging import create_logger

from .config import config_by_name


def create_app(config_name: str = None):
    # pylint: disable=import-outside-toplevel
    """
    Builds the Flask application based on the `config_name` passed.
    Available configs are:

    - prod
    - test
    - dev

    :param config_name: A string value defining what environment you want the src built for
    """
    app = Flask(__name__)
    app.logger = create_logger(app)
    app.logger.setLevel(10)  # Debug

    if not config_name:
        app.logger.warning("`LONGHORN_ENV' not found. Defaulting to Development environment")
        config_name = 'dev'
    else:
        app.logger.info("Running in: %s mode", config_name)

    app.config.from_object(config_by_name[config_name])

    # AUTH_TOKENS would look as such: {None: 'some-user'}
    if None in app.config["AUTH_TOKENS"]:
        app.logger.warning("No authorization tokens detected. Defaulting to: %s", app.config['DEFAULT_TOKEN'])
        app.config['AUTH_TOKENS'] = {app.config['DEFAULT_TOKEN']: 'INSECURE-SESSION'}

    from src.longhorn.link_down import link_down as link_down_blueprint

    app.register_blueprint(link_down_blueprint, url_prefix="/link-down")

    return app
