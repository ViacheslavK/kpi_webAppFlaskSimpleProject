

class Config(object):
    # Database connection (hardcoded becasue doesn't worked good as variables)
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://viacheslav:#$KLag8*0V9DAx*i80kp@viacheslav.mysql.pythonanywhere-services.com/viacheslav$course_work"
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False