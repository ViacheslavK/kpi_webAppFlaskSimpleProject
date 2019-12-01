Once it's running, you need to import the database manager from your code:

``` from flask_app import db ```

Now, we want to create the tables. This is really easy:

``` db.create_all()```