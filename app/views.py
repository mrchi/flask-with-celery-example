# coding=utf-8

from flask import Blueprint
from app.celerytasks.add import my_add
from app.celerytasks.factorial import my_factorial


bp_main = Blueprint("main", "main")


@bp_main.route("/add")
def index():
    my_add.delay(1, 2)
    return "Hello, world!"


@bp_main.route("/fac")
def fac():
    my_factorial.delay(10)
    return "hello"
