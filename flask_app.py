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

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}:3306/{databasename}".format(
    username="the username from the 'Databases' tab",
    password="the password you set on the 'Databases' tab",
    hostname="the database host address from the 'Databases' tab",
    databasename="the database name you chose, probably yourusername$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

comments=[]

# Allow endpoint GET and POST actions; othrvice will get an error "Method is not allowed"
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=comments)
    
    comments.append(request.form["contents"])
    return redirect(url_for("index"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()

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