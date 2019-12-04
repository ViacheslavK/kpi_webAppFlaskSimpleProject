

class Config(object):
    # Database connection (hardcoded becasue doesn't worked good as variables)
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://newuser:BUSDEVGjtx$mGn3@6L79@127.0.0.1:3306/course_work"
    # SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://viacheslav:#$KLag8*0V9DAx*i80kp@viacheslav.mysql.pythonanywhere-services.com/viacheslav$course_work"
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database connection variables (need to use in connection string)
    databasename = "course_work"
    dialect = "MySQL"
    name = "Flask_App_DB"
    password = "BUSDEVGjtx$mGn3@6L79"
    port = 3306
    hostname = "localhost"
    username = "newuser"