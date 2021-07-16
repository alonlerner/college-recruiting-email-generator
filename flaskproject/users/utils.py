from flask import url_for
from flask_mail import Message
from flaskproject import mail

def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message('Password Reset Request', sender='collegeemailsgenerator@gmail.com', recipients=[user.email])
    msg.body=f'''Visit to following link to reset your password:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email and no changes will be made
'''
    mail.send(msg)