"""
Used to start the Flask application based on the environment variable passed.
"""
from os import getenv

from longhorn import create_app


app = create_app(getenv("LONGHORN_ENV") or "dev")

if __name__ == "__main__":
    app.run()
