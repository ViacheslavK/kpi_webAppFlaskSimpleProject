from flask import Flask, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["DEBUG"] = True

databasename = "fla_app"
dialect = "MySQL"
name = "Flask_App_DB"
password = "BUSDEVGjtx$mGn3@6L79"
port = 3306
hostname = "localhost"
username = "newuser"

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://newuser:BUSDEVGjtx$mGn3@6L79@127.0.0.1:3306/fla_app".format(
    username="the username from the 'Databases' tab",
    password="the password you set on the 'Databases' tab",
    hostname="the database host address from the 'Databases' tab",
    databasename="the database name you chose, probably yourusername$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

app.secret_key = "something_only_you_know"
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


all_users = {
    "admin": User("admin", generate_password_hash("secret")),
    "bob": User("bob", generate_password_hash("less-secret")),
    "caroline": User("caroline", generate_password_hash("completely-secret")),
}

@login_manager.user_loader
def load_user(user_id):
    return all_users.get(user_id)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))

comments=[]

# Allow endpoint GET and POST actions; othrvice will get an error "Method is not allowed"
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.all())
    
    comment = Comment(content=request.form["contents"])
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    username = request.form["username"]
    if username not in all_users:
        return render_template("login_page.html", error=True)
    user = all_users[username]

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user) # flask_login function

    return redirect(url_for('index'))

@app.route("/logout/")
@login_required  # This is provided by Flask-Login and allows you to protect views so that they can only be accessed by logged-in users
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/wibble')
def wibble():
    return 'This is my pointless new page'

@app.route('/user/<username>')
def profile(username): 
    pass

if __name__ == '__main__':
    with app.test_request_context():
        print(url_for('login'))
        print(url_for('login', next='/'))
        print(url_for('profile', username='John Doe'))   
    app.run(debug=True) 