# Example from https://www.youtube.com/watch?v=51F_frStZCQ
# Suggested MySQL hosting: https://www.freemysqlhosting.net/
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_DB'] = ''
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE example (id INTEGER, name VARCHAR(20))''')
    cur.execute('''INSERT INTO example VALUES (1, 'Antony')''')
    cur.execute('''INSERT INTO example VALUES (2, 'Katerina')''')
    mysql.connection.commit()
    cur.execute('''SELECT * FROM example''')
    results = cur.fetchall()
    print(results)
    return 'Done!'