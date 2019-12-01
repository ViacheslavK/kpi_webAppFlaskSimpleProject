Now let's add our users back in. Instead of putting them in code (where their passwords are available in plaintext for all to see), we'll add them to the database from the command line. To start a Python shell with all of the Flask stuff loaded, run this in your bash console:

```flask shell```
In the Python interpreter that appears, firstly import our User class and the database connection:

```from flask_app import db, User```
Next, import the password-hashing function that we were previously using in the code:

```from werkzeug.security import generate_password_hash```
Finally, add the users you want, using commands like the ones below but with different passwords:

```admin = User(username="admin", password_hash=generate_password_hash("new-secret"))
db.session.add(admin)
bob = User(username="bob", password_hash=generate_password_hash("super-secret"))
db.session.add(bob)
caroline = User(username="caroline", password_hash=generate_password_hash("8fwe5jYCE98lXl0ZovYW"))
db.session.add(caroline)
db.session.commit()```