from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, InputRequired
from flaskproject.requests.utils import MultiCheckboxField

class RequestForm(FlaskForm):
    subject=StringField('Subject', validators=[DataRequired()])
    content=TextAreaField('Content', validators=[DataRequired()])
    teams=MultiCheckboxField('Teams', coerce=int, validators=[InputRequired()])
    submit=SubmitField('Send Emails')

class EmailCheckForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Continue')