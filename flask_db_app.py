from flask import Flask, g
import sqlite3

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect('./database.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite3_db = connect_db()
    return g.sqlite3_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite3_db.close()


@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

@app.route('/users')
def viewusers():
    db = get_db()
    cursor = db.execute('SELECT id, name FROM users;')
    results = cursor.fetchall()
    return f"<h1>The ID is {results[0]['id']},<br> The name is {results[0]['name']},<br> The age is {results[0]['age']}</h1>"

if __name__ == '__main__':
    app.run(debug=True)
