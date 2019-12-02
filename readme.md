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
1. https://blog.pythonanywhere.com/121/ (application base DB connection and routing)
2. https://blog.pythonanywhere.com/158/ (login feature turn on and users added to DB)
3. https://blog.miguelgrinberg.com/post/setting-up-a-flask-application-in-visual-studio-code (setup tips for project env)
3.1. https://www.youtube.com/watch?v=UXqiVe6h3lA (video from the same author for VC)
3.2. https://www.youtube.com/watch?v=bZUokrYanFM (video from the same author for PyCharm)
4. https://flask.palletsprojects.com/en/1.1.x/tutorial/ (official tutorial)
5. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world (and next chapters)

List of packages in use:
1. https://palletsprojects.com/p/flask/ (Flask documentation itself)
2. https://flask.palletsprojects.com/en/1.1.x/ (Some more docs)
3. https://flask-login.readthedocs.io/en/latest/ (Serve login/auth features)
4. https://docs.python.org/3/library/time.html#time.strftime (Date-Time format)
5. https://flask-migrate.readthedocs.io/en/latest/#multiple-database-support (DataBase version control)

