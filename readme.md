Once it's running, you need to import the database manager from your code:

``` from flask_app import db ```

Now, we want to create the tables. This is really easy:

``` db.create_all()```

Preparation of migrations for DB (to do inside virtual env)

```export FLASK_APP=flask_app.py```
```flask db init```

and then
```flask db migrate```

stamping of current state
```flask db stamp head```

Web-tutorials, used for create it:
1. https://blog.pythonanywhere.com/121/
2. https://blog.pythonanywhere.com/158/

List of packages in use:
1. https://flask-login.readthedocs.io/en/latest/
2. https://docs.python.org/3/library/time.html#time.strftime (Date-Time format)