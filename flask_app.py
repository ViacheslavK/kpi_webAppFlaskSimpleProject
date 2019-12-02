from flask import Flask, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

# Database connection variables (need to use in connection string)
databasename = "course_work"
dialect = "MySQL"
name = "Flask_App_DB"
password = "BUSDEVGjtx$mGn3@6L79"
port = 3306
hostname = "localhost"
username = "newuser"

# Database connection (hardcoded becasue doesn't worked good as variables)
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://newuser:BUSDEVGjtx$mGn3@6L79@127.0.0.1:3306/course_work"

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Database stuff: app created, app migrated if required
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Login stuff
app.secret_key = "something_only_you_know"
login_manager = LoginManager()
login_manager.init_app(app)

# Users info
class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    users_firstname = db.Column(db.String(128))
    users_lastname = db.Column(db.String(128))
    users_description = db.Column(db.String(4096))
    user_email = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(128))
    permission = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()


# Blog postig stuff
class BlogPost(db.Model):
    __tablename__ = "postings"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)
    blogger_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    commenter = db.relationship('User', foreign_keys=blogger_id)


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
    company_name = db.Column(db.String(128))
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
    __tablename__ = "company_ratings"
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(128))
    job_description = db.Column(db.String(4096))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    company = db.relationship('CompanyProfile', foreign_keys=company_id)
    visible = db.Column(db.TinyInt, default=1)
    posted = db.Column(db.DateTime, default=datetime.now)


# Routing (endpoints)
# Allow endpoint GET and POST actions; othrvice will get an error "Method is not allowed"
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # return render_template("main_page.html", comments=Comment.query.all())
        return render_template("main_page.html")
    
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    comment = Comment(content=request.form["contents"], commenter=current_user)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user) # flask_login function

    return redirect(url_for('index'))


@app.route("/logout/")
@login_required
# This is provided by Flask-Login and allows you to protect views so that they can only be accessed by logged-in users
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.test_request_context():
        print(url_for('login'))
        print(url_for('login', next='/'))
        print(url_for('profile', username='John Doe'))   
    app.run(debug=True)
    # Alt. runner properly for Code, where there is no need to use the in-browser debugger or the reloader
    # app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)

@app.route("/register/", methods=["GET", "POST"])
def register_user():
    pass

@app.route("/jobs/", methods=["GET", "POST"])
def jobs_listing():
    pass

@app.route("/blog/", methods=["GET", "POST"])
def blog_feed():
    pass

@app.route("/blog/<blog_id>", methods=["GET", "POST"])
def blog_posting():
    pass

@app.route("/profile/<user_id>", methods=["GET", "POST"])
def view_profile():
    pass

@app.route("/users/", methods=["GET", "POST"])
def get_users_list():
    pass