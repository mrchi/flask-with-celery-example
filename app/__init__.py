# coding=utf-8

from flask import Flask
from celery import Celery

from app.views import bp_main
from app.celerytasks import celery_tasks


def create_app(config_obj):
    """Factory function of Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_obj)

    app.register_blueprint(bp_main)

    app.celery_app = make_celery(app)

    return app


def make_celery(app):
    """
    Function of creating Celery app.

    Ref: http://flask.pocoo.org/docs/1.0/patterns/celery
    """
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    # register task functions into Celery app, and bind function to Flask app.
    for func_name in celery_tasks:
        if not getattr(app, func_name, None):
            setattr(app, func_name, celery.task(celery_tasks[func_name]))
        else:
            raise ValueError(f"Repated name '{func_name}'")     # noqa

    return celery
