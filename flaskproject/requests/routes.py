from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, session
from flask.globals import current_app
from flask_login import current_user, login_required
from flaskproject import db, mail
from flaskproject.models import Request, Team
from flaskproject.requests.forms import RequestForm, EmailCheckForm
from flask_mail import Message
from flaskproject.requests.utils import default_subject, default_content

requests=Blueprint('requests', __name__)

@requests.route("/request/new", methods=['GET', 'POST'])
@login_required
def new_request():
    if not 'first_name' in session:
        return redirect(url_for('requests.check_email'))
    form=RequestForm()
    form.teams.choices = [(row.id, f'{row.name} ({row.division})') for row in Team.query.all()]
    if form.validate_on_submit():
        emails_request=Request(first_name=session['first_name'], last_name=session['last_name'], email=session['email'], subject=form.subject.data, content=form.content.data, sender=current_user)
        db.session.add(emails_request)
        for team in form.teams.data:
            emails_request.teams.append(Team.query.filter_by(id=team).first())
        db.session.commit()
        session.pop('first_name')
        session.pop('last_name')
        session.pop('email')
        session.pop('password')
        flash('Your emails have been sent!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_request.html', title='New Request', form=form, default_subject=default_subject, default_content=default_content)

@requests.route("/request/<int:request_id>")
def request_details(request_id):
    emails_request=Request.query.get_or_404(request_id)
    if emails_request.sender.email != current_user.email:
        return redirect(url_for('main.home'))
    return render_template('request.html', subject=emails_request.subject, emails_request=emails_request)

@requests.route("/request/check_email", methods=['GET','POST'])
@login_required
def check_email():
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
            session['first_name']=form.first_name.data
            session['last_name']=form.last_name.data
            session['email']=form.email.data
            session['password']=form.password.data
            return redirect(url_for('requests.new_request'))
    return render_template('check_email.html', title='New Request', form=form)
