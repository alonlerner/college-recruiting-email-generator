from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, InputRequired
from flaskproject.requests.utils import MultiCheckboxField

class EmailCheckForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Continue')

class RequestForm(FlaskForm):
    subject=StringField('Subject', validators=[DataRequired()])
    content=TextAreaField('Content', validators=[DataRequired()])
    teams=MultiCheckboxField('Teams', coerce=int, validators=[InputRequired()])
    submit=SubmitField('Review')

class ReviewRequestForm(FlaskForm):
    email=StringField('Email')
    subject=StringField('Subject')
    content=TextAreaField('Content')
    teams=TextAreaField('Teams')
    submit=SubmitField('Send Emails')