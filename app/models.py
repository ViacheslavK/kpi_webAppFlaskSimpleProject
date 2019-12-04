from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import db, login_manager
from datetime import datetime


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    users_firstname = db.Column(db.String(128))
    users_lastname = db.Column(db.String(128))
    users_description = db.Column(db.String(4096))
    user_email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    permission = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, username, users_firstname, users_lastname, user_email, password_hash):
        self.username = username
        self.users_firstname = users_firstname
        self.users_lastname = users_lastname
        self.users_description = ""
        self.user_email = user_email
        self.password_hash = password_hash
        self.permission = "commenter"
        self.confirmed = 0
        self.confirmed_on = None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {0}>'.format(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_id(self):
        return self.username

    def user_role(self):
        return self.permission


# Blog postig stuff
class BlogPost(db.Model):
    __tablename__ = "postings"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)
    blogger_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blogger = db.relationship('User', foreign_keys=blogger_id)


# Comments stuff
class Comment(db.Model):
    __tablename__ = "blog_comments"
    id = db.Column(db.Integer, primary_key=True)
    blog_posting = db.Column(db.Integer, db.ForeignKey('postings.id'), nullable=False)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)


# Company profile
class CompanyProfile(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(128), unique=True)
    company_description = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)
    # rating?

# Company profile
class CompanyRating(db.Model):
    __tablename__ = "company_ratings"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    company = db.relationship('CompanyProfile', foreign_keys=company_id)
    rater_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rater = db.relationship('User', foreign_keys=rater_id)
    posted = db.Column(db.DateTime, default=datetime.now)


# Company profile
class CompanyJob(db.Model):
    __tablename__ = "company_jobs"
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(128))
    job_description = db.Column(db.String(4096))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    company = db.relationship('CompanyProfile', foreign_keys=company_id)
    visible = db.Column(db.Boolean, default=True)
    posted = db.Column(db.DateTime, default=datetime.now)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()