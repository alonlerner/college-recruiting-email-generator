from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, InputRequired
from flaskproject.requests.utils import MultiCheckboxField

class RequestForm(FlaskForm):
    subject=StringField('Subject', validators=[DataRequired()])
    content=TextAreaField('Content', validators=[DataRequired()])
    teams=MultiCheckboxField('Teams', coerce=int, validators=[InputRequired()])
    submit=SubmitField('Review')

class ReviewRequestForm(FlaskForm):
    subject=StringField('Subject')
    content=TextAreaField('Content')
    teams=TextAreaField('Teams')
    submit=SubmitField('Continue')

class EmailCheckForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    recaptcha=RecaptchaField()
    submit=SubmitField('Send Emails')