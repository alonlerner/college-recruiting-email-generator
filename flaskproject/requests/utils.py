from flask import session
from flaskproject.models import Team, Coach
from wtforms import widgets, SelectMultipleField
from flask.globals import current_app
from flask_mail import Message
from flaskproject import mail

default_subject='XXX XXX - Prospective Student-Athlete'

default_content='''Hello Coach [coach-last-name],

My name is XXX XXX and I am a swimmer from XXX. My SAT score is XXX. Please recruit me!'''

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

def send_emails():
    current_app.config.update(dict(
            MAIL_USERNAME=session["email"],
            MAIL_PASSWORD=session["password"]
        ))
    mail.init_app(current_app)
    for team in session['teams']:
            for coach in Coach.query.filter_by(team_id=team).all():
                subject=session['subject'].replace("[team]", Team.query.filter_by(id=team).first().name).replace("[division]", Team.query.filter_by(id=team).first().division).replace("[conference]", Team.query.filter_by(id=team).first().conference).replace("[mascot]", Team.query.filter_by(id=team).first().mascot).replace("[coach-first-name]", Coach.query.filter_by(id=coach.id).first().first_name).replace("[coach-last-name]", Coach.query.filter_by(id=coach.id).first().last_name)
                content=session['content'].replace("[team]", Team.query.filter_by(id=team).first().name).replace("[division]", Team.query.filter_by(id=team).first().division).replace("[conference]", Team.query.filter_by(id=team).first().conference).replace("[mascot]", Team.query.filter_by(id=team).first().mascot).replace("[coach-first-name]", Coach.query.filter_by(id=coach.id).first().first_name).replace("[coach-last-name]", Coach.query.filter_by(id=coach.id).first().last_name)
                msg=Message(subject, sender=session["email"], recipients=[Coach.query.filter_by(id=coach.id).first().email])
                msg.body=content
                mail.send(msg)