from flask import Flask, request, url_for, render_template, redirect

app = Flask(__name__)

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
    app.config["DEBUG"] = True
    app.run(debug=True) 