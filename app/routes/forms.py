from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, Length, ValidationError
import re


def strong_password(form, field):
    pw = field.data or ""

    if len(pw) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", pw):
        raise ValidationError("Password must include at least one uppercase letter.")
    if not re.search(r"[a-z]", pw):
        raise ValidationError("Password must include at least one lowercase letter.")
    if not re.search(r"\d", pw):
        raise ValidationError("Password must include at least one number.")


class RegisterForm(FlaskForm):
    full_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=2, max=120)]
    )
    phone = StringField("Phone", validators=[Optional()])
    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField(
        "Password",
        validators=[DataRequired(), strong_password]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[EqualTo("password")]
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
