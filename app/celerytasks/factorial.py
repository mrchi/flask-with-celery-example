# coding=utf-8

from celery import Celery
from flask import current_app

from . import celeryconfig

factorial_app = Celery("factorial_app")
factorial_app.config_from_object(celeryconfig)


@factorial_app.task(shared=False)
def my_factorial(n):
    result = 1
    for i in range(1, n+1):
        result *= i
    print(f"{n}! = {result}")   # noqa
