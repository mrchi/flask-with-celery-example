# coding=utf-8

from .add import add_app
from .factorial import factorial_app

celery_apps = [add_app, factorial_app]


def init_app(app):
    app.celery_apps = {}
    for celery_app in celery_apps:

        class ContextTask(celery_app.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        celery_app.Task = ContextTask

        name = celery_app.main
        if name in app.celery_apps:
            raise NameError(f"Celery app name '{name}' is repeated.")   # noqa
        app.celery_apps[name] = celery_app
