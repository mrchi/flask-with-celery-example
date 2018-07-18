# coding=utf-8

from flask import Flask
from app.views import bp_main
from app import celerytasks


def create_app(config_obj):
    """Factory function of Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_obj)

    app.register_blueprint(bp_main)

    celerytasks.init_app(app)

    return app
