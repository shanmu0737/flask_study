from flask import redirect,request,session,url_for,flash,render_template,g
from flask import Blueprint
import sqlite3

logins = Blueprint('logins',__name__)

DATABASE_url = r'./db/feedback.db'


#u将游标获取的Tuple根据数据库列表转换为dict,将元组的行转换为字典表
def make_dicts(cursor,row):
    #enumerate 是全局函数，游标的description对象能够获取列索引，
    return dict((cursor.description[i][0], value) for i, value in enumerate(row))

#获取（建立数据库连接）
def get_db():
    # getattr有3个属性，第一个是获取谁的属性
    # 第一个是获取什么属性； 第三个如果没有属性，用默认的
    db = getattr(g,'_database',None)
    if db is None:
        db = sqlite3.connect(DATABASE_url)
        g._datebase = db
        db.row_factory = make_dicts     #行工厂转换为字典表，make_dict不要括号，代表现在不执行
    return db

#执行用于选择数据的sql语句
def query_sql(sql,prms=(), one=False):
    c = get_db().cursor()
    result = c.execute(sql,prms).fetchall()
    # 括号里的意思 默认情况下给我result[0],否则给我一个None
    return (result[0] if result else None) if one else result

@logins.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        sql = "select count(*) as [count] from UserInfo where UserName=? and Password=? "
        result = query_sql(sql,(username,pwd),one=True)
        if int(result.get('count')) > 0:
            session['admin'] = username
            return redirect(url_for('feedback_list'))
        else:
            flash("账号或密码不正确，请重新登录！")
    return render_template('wenti_login.html')