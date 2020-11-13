user = 'root'
password = "123456"
host = "127.0.0.1"
port = "3306"
database = "ii"
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(user, password, host, port, database)
#设置数据库追踪信息,压制警告
SQLALCHEMY_TRACK_MODIFICATIONS = True