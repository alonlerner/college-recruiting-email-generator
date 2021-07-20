from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email

class RequestForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    subject=StringField('Subject', validators=[DataRequired()])
    content=TextAreaField('Content', validators=[DataRequired()])
    teams=StringField('Teams', validators=[DataRequired()])
    submit=SubmitField('Send Emails')

class EmailCheckForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Continue')