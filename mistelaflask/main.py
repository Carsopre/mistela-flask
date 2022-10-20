from flask import Blueprint, render_template

from mistelaflask import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
def profile():
    return render_template("profile.html")
