from flask import render_template, url_for, flash, redirect, request
from flaskproject import app, db, bcrypt, mail
from flaskproject.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestForm, RequestResetForm, ResetPasswordForm
from flaskproject.models import User, Request
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account was created for {form.email.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful!', 'danger')
    return render_template('Login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email=form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.email.data=current_user.email
    return render_template('account.html', title='Account', form=form)

@app.route("/request/new", methods=['GET', 'POST'])
@login_required
def new_request():
    form=RequestForm()
    if form.validate_on_submit():
        emails_request=Request(name=form.name.data, subject=form.subject.data, content=form.content.data, teams=form.teams.data, sender=current_user)
        db.session.add(emails_request)
        db.session.commit()
        flash('Your emails have been sent!', 'success')
        return redirect(url_for('home'))
    return render_template('create_request.html', title='New Request', form=form)

@app.route("/request/<int:request_id>")
def request_details(request_id):
    emails_request=Request.query.get_or_404(request_id)
    if emails_request.sender.email != current_user.email:
        return redirect(url_for('home'))
    return render_template('request.html', subject=emails_request.subject, emails_request=emails_request)

@app.route("/userrequests")
@login_required
def user_requests():
    page=request.args.get('page', 1, type=int)
    user=User.query.filter_by(email=current_user.email).first()
    requests=Request.query.filter_by(sender=current_user).order_by(Request.date_submitted.desc()).paginate(page=page, per_page=5)
    return render_template('user_requests.html', requests=requests, user=user)

def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message('Password Reset Request', sender='collegeemailsgenerator@gmail.com', recipients=[user.email])
    msg.body=f'''Visit to following link to reset your password:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email and no changes will be made
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Instructions to reset your password has been sent to your email!', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user=User.verify_reset_token(token)
    if user is None:
        flash('That is an expired or invalid token', 'warning')
        return redirect(url_for('reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash(f'Your password has been updated!', 'success')
        return redirect(url_for('home'))
    return render_template('reset_token.html', title='Reset Password', form=form)