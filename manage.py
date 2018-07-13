# coding=utf-8

import os

from app import create_app
from config import config

app = create_app(config[os.getenv('FLASK_ENV') or 'default'])
celery_app = app.celery_app


@app.shell_context_processor
def make_shell_context():
    return dict(celery_app=celery_app)
