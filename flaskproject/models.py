from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskproject import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(120),unique=True, nullable=False)
    password=db.Column(db.String(60),nullable=False)
    access=db.Column(db.String(10), nullable=False, default='user')
    requests=db.relationship('Request', backref='sender',lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s=Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.email}, {self.id}')"

rtrelationship=db.Table('rtrelationship', 
    db.Column('request_id', db.Integer, db.ForeignKey('requests.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id')),
    extend_existing=True
)

class Request(db.Model):
    __tablename__ = "requests"
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(120), nullable=False)
    subject=db.Column(db.String(100), nullable=False)
    content=db.Column(db.Text, nullable=False)
    date_submitted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Request('{self.first_name}, {self.last_name}, {self.subject}, {self.date_submitted}')"

class Team(db.Model):
    __tablename__ = "teams"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(40), nullable=False)
    division=db.Column(db.String(40), nullable=False)
    conference=db.Column(db.String(40), nullable=False)
    state=db.Column(db.String(40), nullable=False)
    mascot=db.Column(db.String(40), nullable=False)
    coaches=db.relationship('Coach', backref='team', lazy=True)
    teams=db.relationship('Request', secondary=rtrelationship, backref=db.backref('teams', lazy='dynamic'))

    def __repr__(self):
        return f"Team('{self.name}, {self.division}, {self.conference}, {self.state}')"

class Coach(db.Model):
    __tablename__ = "coaches"
    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(20), nullable=False)
    last_name=db.Column(db.String(20), nullable=False)
    position=db.Column(db.String(20), nullable=False)
    email=db.Column(db.String(120),unique=True, nullable=False)
    team_id=db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    def __repr__(self):
        return f"Coach('{self.first_name}, {self.last_name}, {self.email}, {self.team_id}')"
