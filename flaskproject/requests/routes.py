from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, session
from flask.globals import current_app
from flask_login import current_user, login_required
from flaskproject import db, mail
from flaskproject.models import Request, Team, Coach
from flaskproject.requests.forms import RequestForm, EmailCheckForm, ReviewRequestForm
from flask_mail import Message
from flaskproject.requests.utils import default_subject, default_content, send_emails

requests=Blueprint('requests', __name__)

@requests.route("/request/info", methods=['GET', 'POST'])
@login_required
def request_info():
    teamsChoices = [{"id": row.id, "name": row.name, "division": row.division, "conference": row.conference, "state":row.state} for row in Team.query.all()]
    teamsChoices=sorted(teamsChoices, key=lambda i: (i['name']))
    print(teamsChoices)
    divisions=[]
    for team in Team.query.all():
        divisions.append(team.division)
    divisions=list(set(divisions))
    divisions.sort()
    conferences=[]
    for team in Team.query.all():
        conferences.append(team.conference)
    conferences=list(set(conferences))
    conferences.sort()
    states=[]
    for team in Team.query.all():
        states.append(team.state)
    states=list(set(states))
    states.sort()

    #if request.method == 'POST':

    return render_template('request_info.html', title='New Request', teamsChoices=teamsChoices, divisions=divisions, conferences=conferences, states=states, default_subject=default_subject, default_content=default_content)

@requests.route("/submit_request_info", methods=['GET', 'POST'])
@login_required
def submit_request_info():
    session['subject']=request.get_json()['subject']
    session['content']=request.get_json()['content']
    session['teams']=request.get_json()['teams']
    print(session['teams'])
    return redirect(url_for('requests.review_request'))

@requests.route("/request/new", methods=['GET', 'POST'])
@login_required
def new_request():
    form=RequestForm()
    form.teams.choices = [(row.id, f'{row.name} ({row.division}, {row.conference}, {row.state})') for row in Team.query.all()]
    if form.validate_on_submit():
        session['subject']=form.subject.data
        session['content']=form.content.data
        session['teams']=form.teams.data
        return redirect(url_for('requests.review_request'))
    return render_template('create_request.html', title='New Request', form=form, default_subject=default_subject, default_content=default_content)

@requests.route("/request/review", methods=['GET', 'POST'])
@login_required
def review_request():
    if not 'subject' in session or not 'content' in session or not 'teams' in session:
        flash('Session expired! Please fill the form again.', 'danger')
        return redirect(url_for('requests.new_request'))
    form=ReviewRequestForm()
    teams=''
    for team in session['teams']:
        teams = teams + Team.query.filter_by(id=team['id']).first().name + '; '
    subject=session['subject'].replace("[team]", Team.query.filter_by(id=team['id']).first().name).replace("[division]", Team.query.filter_by(id=team['id']).first().division).replace("[conference]", Team.query.filter_by(id=team['id']).first().conference).replace("[state]", Team.query.filter_by(id=team['id']).first().state).replace("[mascot]", Team.query.filter_by(id=team['id']).first().mascot).replace("[coach-first-name]", Coach.query.filter_by(team_id=team['id']).first().first_name).replace("[coach-last-name]", Coach.query.filter_by(team_id=team['id']).first().last_name)
    content=session['content'].replace("[team]", Team.query.filter_by(id=team['id']).first().name).replace("[division]", Team.query.filter_by(id=team['id']).first().division).replace("[conference]", Team.query.filter_by(id=team['id']).first().conference).replace("[state]", Team.query.filter_by(id=team['id']).first().state).replace("[mascot]", Team.query.filter_by(id=team['id']).first().mascot).replace("[coach-first-name]", Coach.query.filter_by(team_id=team['id']).first().first_name).replace("[coach-last-name]", Coach.query.filter_by(team_id=team['id']).first().last_name)
    if form.validate_on_submit():
        return redirect(url_for('requests.check_email'))
    return render_template('review_request.html', title='Review Request', form=form, subject=subject, content=content, teams=teams)
    
@requests.route("/request/check_email", methods=['GET','POST'])
@login_required
def check_email():
    if not 'subject' in session or not 'content' in session or not 'teams' in session:
        flash('Session expired! Please fill the form again.', 'danger')
        return redirect(url_for('requests.new_request'))
    form=EmailCheckForm()
    if form.validate_on_submit():
        current_app.config.update(dict(
            MAIL_USERNAME=form.email.data,
            MAIL_PASSWORD=form.password.data
        ))
        mail.init_app(current_app)
        msg=Message('Test',sender=form.email.data, recipients=['collegeemailsgenerator@gmail.com'])
        try:
            mail.send(msg)
        except:
            flash('Error! The email and password are invalid or the less secure apps on your gmail account is turned off.','danger')
        else:
            emails_request=Request(email=form.email.data, subject=session['subject'], content=session['content'], sender=current_user)
            db.session.add(emails_request)
            for team in session['teams']:
                emails_request.teams.append(Team.query.filter_by(id=team['id']).first())
            db.session.commit()
            send_emails(form.email.data, form.password.data)
            session.pop('subject')
            session.pop('content')
            session.pop('teams')
            flash('Your emails have been sent!', 'success')
            return redirect(url_for('main.home'))
    return render_template('check_email.html', title='New Request', form=form)

@requests.route("/request/<int:request_id>")
def request_details(request_id):
    emails_request=Request.query.get_or_404(request_id)
    if emails_request.sender.email != current_user.email:
        return redirect(url_for('main.home'))
    return render_template('request.html', subject=emails_request.subject, emails_request=emails_request)

