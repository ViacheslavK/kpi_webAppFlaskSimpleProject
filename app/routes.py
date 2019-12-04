from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from flask import request, url_for, render_template, redirect
from app import app
from app.models import User, BlogPost

blog_posts = []

# Routing (endpoints)
# Allow endpoint GET and POST actions; othrvice will get an error "Method is not allowed"
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", blog_posts=BlogPost.query.all())
    
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    return redirect(url_for("index"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)
    
    login = login_user(user)
    return redirect(url_for('index'))


@app.route("/register/", methods=["GET", "POST"])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == "GET":
        return render_template("register.html", error='')

    password = request.form['password']
    password_repeat = request.form['password_repeat']
    entered_email = request.form["email"]
    new_username = request.form["username"]

    exists_email = User.query.filter_by(user_email=entered_email).first()

    if password != password_repeat:
        return render_template("register.html", error='password')

    if load_user(new_username) is not None:
        return render_template("register.html", error='already_registered_name')

    if exists_email is not None:
        return render_template("register.html", error='already_registered_email')

    user = User(username=request.form["username"],
                users_firstname = request.form["first_name"],
                users_lastname = request.form["last_name"],
                user_email=request.form["email"],
                password_hash=generate_password_hash(request.form["password"]))
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route("/jobs/", methods=["GET", "POST"])
def jobs_listing():
    pass

@app.route("/companies/", methods=["GET", "POST"])
def dev_companies():
    pass

@app.route("/blog/", methods=["GET", "POST"])
@login_required
def blog_post():
    if request.method == "GET" and current_user.is_authenticated and current_user.user_role() in ['admin', 'blogger']:
        return render_template("posting.html")
    else:
        return redirect(url_for('index'))
    
    posting = BlogPost(content=request.form["contents"], 
                    blogger=current_user)
    db.session.add(posting)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/blog/<blog_id>", methods=["GET", "POST"])
def blog_posting():
    pass

@app.route('/user/', methods=["GET", "POST"])
@app.route('/user/<username>', methods=["GET", "POST"])
@login_required
def profile(username=None):
    return render_template('profile_page.html', username=username)

@app.route("/users/", methods=["GET", "POST"])
@login_required
def get_users_list():
    if request.method == "GET" and current_user.user_role() == 'admin':
        return render_template("users_list.html", registered_users=User.query.all())

    return redirect(url_for("index"))

@app.route("/logout/")
@login_required
# This is provided by Flask-Login and allows you to protect views so that they can only be accessed by logged-in users
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    return redirect(url_for('index'))