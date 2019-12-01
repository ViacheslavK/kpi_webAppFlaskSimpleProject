from flask import Flask, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

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

    if request.form["username"] != "admin" or request.form["password"] != "secret":
        return render_template("login_page.html", error=True)

    return redirect(url_for('index'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         do_the_login()
#     else:
#         show_the_login_form()

def do_the_login():
    pass 

def show_the_login_form():
    pass 

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