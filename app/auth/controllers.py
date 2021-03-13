from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app import db
from app.auth.forms import LoginForm
from app.auth.forms import RegistrationForm
from app.auth.models import User

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    form = LoginForm(request.form)
    return render_template("auth/login.html", form=form)


@auth.route("/login", methods=["POST"])
def login_post():
    form = LoginForm(request.form)
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.", "is-danger")
        return render_template("auth/login.html", form=form)

    if not form.validate_on_submit():
        flash("An error occured. Please try again.", "is-danger")
        return render_template("auth/login.html", form=form)

    login_user(user, remember=remember)
    return redirect(url_for("page.profile"))


@auth.route("/register")
def register():
    form = RegistrationForm(request.form)
    return render_template("auth/register.html", form=form)


@auth.route("/register", methods=["POST"])
def register_post():
    form = RegistrationForm(request.form)
    email = request.form.get("email")
    name = request.form.get("username")
    password = request.form.get("password")

    if form.validate_on_submit():
        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password, method="sha256"),
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
