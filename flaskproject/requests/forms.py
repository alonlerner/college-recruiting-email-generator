from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class RequestForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    subject=StringField('Subject', validators=[DataRequired()])
    content=TextAreaField('Content', validators=[DataRequired()])
    teams=StringField('Teams', validators=[DataRequired()])
    submit=SubmitField('Send Emails')
