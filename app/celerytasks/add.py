# coding=utf-8

from celery import Celery
from flask import current_app

from . import celeryconfig

add_app = Celery("add_app")
add_app.config_from_object(celeryconfig)


@add_app.task(shared=False)
def my_add(a, b):
    result = a + b
    print(f"{a} + {b} = {result}")  # noqa
    print(current_app.config["TEST_FOR_APP_CONTEXT"])
