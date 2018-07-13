# coding=utf-8

from functools import wraps

from flask import current_app

celery_tasks = {}


def celery_task(func):
    """Use this decorator to store [funcname: func] into celery_tasks dict."""
    @wraps(func)
    def wrapper(*args, **kw):
        return func(*args, **kw)
    celery_tasks[func.__name__] = func
    return wrapper


@celery_task
def my_add(a, b):
    result = a + b
    print(f"{a} + {b} = {result}")  # noqa
    print(current_app.config["TEST_FOR_APP_CONTEXT"])
