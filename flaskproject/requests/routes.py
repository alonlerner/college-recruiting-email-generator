from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskproject import db
from flaskproject.models import Request
from flaskproject.requests.forms import RequestForm


requests=Blueprint('requests', __name__)

@requests.route("/request/new", methods=['GET', 'POST'])
@login_required
def new_request():
    form=RequestForm()
    if form.validate_on_submit():
        emails_request=Request(name=form.name.data, subject=form.subject.data, content=form.content.data, teams=form.teams.data, sender=current_user)
        db.session.add(emails_request)
        db.session.commit()
        flash('Your emails have been sent!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_request.html', title='New Request', form=form)

@requests.route("/request/<int:request_id>")
def request_details(request_id):
    emails_request=Request.query.get_or_404(request_id)
    if emails_request.sender.email != current_user.email:
        return redirect(url_for('main.home'))
    return render_template('request.html', subject=emails_request.subject, emails_request=emails_request)
