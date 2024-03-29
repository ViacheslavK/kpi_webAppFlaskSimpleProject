from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from flask import request, url_for, render_template, redirect
from app import app, db
from app.models import User, BlogPost, CompanyProfile, CompanyJob, load_user
from sqlalchemy import desc

# Routing (endpoints)
# Allow endpoint GET and POST actions; othrvice will get an error "Method is not allowed"
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", blog_posts=BlogPost.query.order_by(desc(BlogPost.posted)).all())
    
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
    if request.method == "GET":
        return render_template("jobs_list.html", actual_jobs_list=CompanyJob.query.filter_by(visible=True).all(), companies_list=CompanyProfile.query.all())
    job_title = request.form['title']
    job_description = request.form['description']
    job_connected_company = request.form['company']
    job = CompanyJob(job_title=job_title,
                    job_description=job_description,
                    company_id=job_connected_company)
    db.session.add(job)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/inactive-jobs/", methods=["GET", "POST"])
def jobs_deactivated():
    if request.method == "GET":
        return render_template("jobs_deactivated.html", deactivated_jobs=CompanyJob.query.filter_by(visible=False).all())

    return redirect(url_for("index"))

@app.route("/jobs/<job_id>", methods=["GET", "POST"])
def send_cv(job_id):
    if request.method == "GET":
        return render_template("job_page.html", selected_job=CompanyJob.query.filter_by(id=job_id).first_or_404())

    return redirect(url_for("index"))

@app.route("/companies/", methods=["GET", "POST"])
def dev_companies():
    if request.method == "GET":
        return render_template("companies.html", companies_list=CompanyProfile.query.all())

@app.route("/companies/<company_name>", methods=["GET", "POST"])
def dev_company(company_name):
    updated_company=CompanyProfile.query.filter_by(company_name=company_name).first_or_404()
    if request.method == "GET":
        return render_template("company_page.html", displayed_company=updated_company)
           # company_jobs=CompanyJob.query.filter_by(id=company_id).filter_by(visible=True).all())
    else:
        updated_company_name=request.form["company_name"]
        updated_company_description=request.form["company_description"]
        check_company_name = CompanyProfile.query.filter_by(company_name=updated_company_name).first()
        if check_company_name != None:
            if check_company_name.id == updated_company.id:
                updated_company.company_description = updated_company_description
                db.session.commit()
                return redirect(url_for('dev_companies'))
            else:
                return redirect(url_for('dev_company', company_name=updated_company.company_name, alert="CompanyExist"))
        elif updated_company_name != None and updated_company_description != None:
            updated_company.company_name = updated_company_name
            updated_company.company_description = updated_company_description
            db.session.commit()
            return redirect(url_for('dev_companies'))
        else:
            pass # Handle incorrect_company_data error


@app.route("/companies/<company_name>/delete", methods=["GET", "POST"])
def delete_company(company_name):
    CompanyProfile.query.filter_by(company_name=company_name).delete()
    db.session.commit()
    return redirect(url_for('dev_companies'))


@app.route("/add_company/", methods=["GET", "POST"])
def add_company():
    if request.method == "GET" and current_user.is_authenticated and current_user.user_role() in ['admin']:
        return render_template("company_page.html", displayed_company=None)
    elif request.method == "POST" and current_user.is_authenticated and current_user.user_role() in ['admin']:
        new_company = CompanyProfile(company_name=request.form["company_name"], company_description=request.form["company_description"])
        db.session.add(new_company)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return redirect(url_for('index'))


@app.route("/blog/", methods=["GET", "POST"])
@login_required
def blog_post():
    if request.method == "GET" and current_user.is_authenticated and current_user.user_role() in ['admin', 'blogger']:
        return render_template("posting.html")
    elif request.method == "POST" and current_user.is_authenticated and current_user.user_role() in ['admin', 'blogger']:
        posting = BlogPost(content=request.form["contents"], 
                        blogger=current_user)
        db.session.add(posting)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return redirect(url_for('index'))


@app.route("/blog/<blogpost>", methods=["GET", "POST"])
def blog_posting(blogpost):
    post_for_update=BlogPost.query.filter_by(id=blogpost).first_or_404()
    if request.method == "GET":
        return render_template("blog_entry.html", post=post_for_update)
    elif request.form["contents"] != None:
        new_content=request.form["contents"]
        post_for_update.content=new_content
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route("/blog/<blogpost>/delete", methods=["GET", "POST"])
def delete_post(blogpost):
    BlogPost.query.filter_by(id=blogpost).delete()
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/user/', methods=["GET", "POST"])
@app.route('/user/<username>', methods=["GET", "POST"])
@login_required
def profile(username=None):
    if username == None:
        displayed_user = User.query.filter_by(username=current_user.get_id()).first()
    else:
        displayed_user = User.query.filter_by(username=username).first_or_404()
    if request.method == "GET":    
        return render_template('user_page.html', displayed_user=displayed_user)
    else:
        if request.form["firstName"] != "":
            desired_first_name=request.form["firstName"]
            displayed_user.users_firstname = desired_first_name
        if request.form["lastName"] != "":
            desired_last_name=request.form["lastName"]
            displayed_user.users_lastname = desired_last_name
        if request.form["userDescription"] != "":
            desired_description=request.form["userDescription"]
            displayed_user.users_description = desired_description
        if displayed_user != current_user:
            if request.form["user_permissions"] != "":    
                desired_permission=request.form["user_permissions"]
                displayed_user.permission = desired_permission
        else:
            if request.form["inputPassword"] != "":
                desired_password=generate_password_hash(request.form["inputPassword"])
                displayed_user.password_hash = desired_password
        db.session.commit()
        if current_user.user_role() == 'admin':
            return redirect(url_for("get_users_list"))
        else:
            return redirect(url_for("index"))
        

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