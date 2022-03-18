from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.debug = True
# DATABASE_url = r'./db/feedback.db'
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///./db/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#创建数据库核心对象
db = SQLAlchemy(app)
#app=Flask 为db.init_app所用
# db.init_app(app)    #初始化绑定app对象

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    userneme = db.Column(db.String(50),unique=True)
    email = db.Column(db.String(200),unique=True)
    password = db.Column(db.String(100))
    created_time = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,username,email,password,created_time = datetime.now()):
        self.userneme = username
        self.email = email
        self.password = password
        self.created_time = created_time

    #表现函数
    def __repr__(self):
        return '<用户：{}{}{}>'.format(self.id,self.userneme,self.email)

@app.route('/db/')
def initialize_db():
    db.create_all()
    return 'ok'

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
