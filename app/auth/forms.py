from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import ValidationError
from wtforms import validators
from wtforms.fields.html5 import EmailField

from app.auth.models import User


class LoginForm(FlaskForm):
    email = EmailField(
        "Email Address",
        [
            validators.Email(),
            validators.DataRequired(),
        ],
    )
    password = PasswordField(
        "Password",
        [
            validators.InputRequired(),
        ],
    )
    remember = BooleanField("Remember me")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        [
            validators.DataRequired(),
            validators.Length(min=4, max=25),
        ],
    )
    email = EmailField(
        "Email Address",
        [
            validators.DataRequired(),
            validators.Email(message="Please enter a valide email address"),
            validators.Length(min=6, max=35),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            validators.InputRequired(),
            validators.EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Confirm Password")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            msg = u"A user with this email address already exists."
            raise ValidationError(msg)
