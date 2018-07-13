# coding=utf-8

from flask import Blueprint, current_app


bp_main = Blueprint("main", "main")


@bp_main.route("/")
def index():
    current_app.my_add.delay(1, 2)
    return "Hello, world!"
