from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo


class SignUpForm(FlaskForm):
    full_name = StringField('Full Name')
    email = StringField('Email',
                        validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(), EqualTo('password')])
    currency = StringField('Default Currency')
    submit = SubmitField('Sign Up')


class EditUserForm(FlaskForm):
    full_name = StringField('Full Name')
    email = StringField('Email',
                        validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(), EqualTo('password')])
    currency = StringField('Default Currency')
    submit = SubmitField('Update')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class CurrencyExchangeForm(FlaskForm):
    from_currency = StringField('From Currency')
    to_currency = StringField('To Currency')
    submit = SubmitField('Exchange')


class TransferFundsForm(FlaskForm):
    from_user = StringField('From User')
    to_user = StringField('To User')
    amount = StringField('Amount')
    submit = SubmitField('Transfer')
