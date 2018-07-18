# coding=utf-8

import os

from app import create_app
from config import config

app = create_app(config[os.getenv('FLASK_ENV') or 'default'])

# add celery apps to module namespace
for name, celery_app in app.celery_apps.items():
    if name in globals():
        raise NameError(f"Celery app name '{name}' is repeated.")   # noqa
    globals()[name] = celery_app


@app.shell_context_processor
def make_shell_context():
    return dict(**app.celery_apps)
