from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from mistelaflask import db
from mistelaflask.models import User

auth = Blueprint("auth", __name__)


@auth.route("/otp")
def login_otp():
    return render_template("auth/otp_login.html")


@auth.route("/otp", methods=["POST"])
def login_otp_post():
    _username = request.form.get("username")
    _otp = request.form.get("otp", None)
    if not _otp:
        flash("The OTP is required for the first log-in. Contact us in case of error.")
        return redirect(url_for("auth.login_otp"))
    _password = request.form.get("password", None)
    if not _password:
        flash("Please provide a new password. The provided OTP is only valid once.")
        return redirect(url_for("auth.login_otp"))

    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(username=_username, otp=_otp).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user:
        flash("Please check your login details and try again.")
        return redirect(
            url_for("auth.login_otp")
        )  # if the user doesn't exist or password is wrong, reload the page

    user.otp = None
    user.password = generate_password_hash(_password, method="sha256")
    login_user(user, remember=remember)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("main.index"))


@auth.route("/login")
def login():
    return render_template("auth/login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    # login code goes here
    name = request.form.get("name")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(name=name).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(
            url_for("auth.login")
        )  # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)
    return redirect(url_for("main.index"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
