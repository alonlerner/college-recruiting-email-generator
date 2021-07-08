from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskproject.models import User


class RegistrationForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=3)])
    confirm_password=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    submit=SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is taken. Please choose a different one.')

class RequestForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    subject=StringField('Subject', validators=[DataRequired()])
    content=TextAreaField('Content', validators=[DataRequired()])
    teams=StringField('Teams', validators=[DataRequired()])
    submit=SubmitField('Send Emails')

class RequestResetForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    submit=SubmitField('Request Password Reset')

    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account associated with email. Please register first.')

class ResetPasswordForm(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired(),Length(min=3)])
    confirm_password=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Reset Password')