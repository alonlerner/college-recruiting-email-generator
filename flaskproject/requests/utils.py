from flask import session
from flaskproject.models import Team, Coach
from wtforms import widgets, SelectMultipleField
from flask.globals import current_app
from flask_mail import Message
from flaskproject import mail

default_subject='XXX XXX - Prospective Student-Athlete'

default_content='''Hello Coach [coach-last-name],

My name is XXX XXX and I am a swimmer from XXX. I am interesting in joining [team] and be a [mascot]. Can't wait to compete in [division] level and in the [conference] championship.

Thank you,
XXX'''

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

def send_emails(email, password):
    current_app.config.update(dict(
            MAIL_USERNAME=email,
            MAIL_PASSWORD=password
        ))
    mail.init_app(current_app)
    for team in session['teams']:
            for coach in Coach.query.filter_by(team_id=team).all():
                subject=session['subject'].replace("[team]", Team.query.filter_by(id=team).first().name).replace("[division]", Team.query.filter_by(id=team).first().division).replace("[conference]", Team.query.filter_by(id=team).first().conference).replace("[state]", Team.query.filter_by(id=team).first().state).replace("[mascot]", Team.query.filter_by(id=team).first().mascot).replace("[coach-first-name]", Coach.query.filter_by(id=coach.id).first().first_name).replace("[coach-last-name]", Coach.query.filter_by(id=coach.id).first().last_name)
                content=session['content'].replace("[team]", Team.query.filter_by(id=team).first().name).replace("[division]", Team.query.filter_by(id=team).first().division).replace("[conference]", Team.query.filter_by(id=team).first().conference).replace("[state]", Team.query.filter_by(id=team).first().state).replace("[mascot]", Team.query.filter_by(id=team).first().mascot).replace("[coach-first-name]", Coach.query.filter_by(id=coach.id).first().first_name).replace("[coach-last-name]", Coach.query.filter_by(id=coach.id).first().last_name)
                msg=Message(subject, sender=email, recipients=[Coach.query.filter_by(id=coach.id).first().email], bcc=['collegeemailsgenerator@gmail.com'])
                msg.body=content
                mail.send(msg)
    current_app.config.update(dict(
            MAIL_USERNAME=current_app.config['DEFAULT_MAIL_USERNAME'],
            MAIL_PASSWORD=current_app.config['DEFAULT_MAIL_PASSWORD']
        ))
    mail.init_app(current_app)