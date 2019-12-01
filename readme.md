Once it's running, you need to import the database manager from your code:

``` from flask_app import db ```

Now, we want to create the tables. This is really easy:

``` db.create_all()```

Web-tutorials, used for create it:
1. https://blog.pythonanywhere.com/121/
2. https://blog.pythonanywhere.com/158/

List of packages in use:
1. https://flask-login.readthedocs.io/en/latest/