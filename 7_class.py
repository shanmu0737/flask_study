import sqlite3
from datetime import datetime,timedelta
import os
from flask import Flask,render_template,request,redirect,url_for
from flask import  g,flash,send_from_directory,session,make_response
from account.views import RegUser
from article.views import article
from product.views import product
from mofang.views import mofang         #注册模块
from sign_out.views import sign_outt    #退出模块
from login_bag.views import logins          #登录模块

app = Flask(__name__)
app.debug = True
app.secret_key="sfjlsjkdl#(@*$&*(&%ffjfjklfj@kfjfk"

DATABASE_url = r'./db/feedback.db'
UPLOADS = r'./uploads'
ALLOWED = ['.jpg','.png','.gif']

#注册一个blueprint
app.register_blueprint(article,url_prefix='/articles/')

app.register_blueprint(product,url_prefix='/products/')

app.register_blueprint(mofang,url_prefix='/mofangs/')   #注册

app.register_blueprint(sign_outt,url_prefix='/sing_out/')   #登出

app.register_blueprint(logins,url_prefix='/login/')     #登录

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

#关闭连接（在当前app上下文销毁时关闭连接,装饰器）
@app.teardown_appcontext
def close_connection(exeption):
    db = getattr(g,'_database',None)
    if db is not None:
        db.close()

#执行sql语句不返回数据结果,用于添加、 更新、删除操作
def execute_sql(sql,prms=()):
    c = get_db().cursor()  #游标
    c.execute(sql,prms)   #执行sql
    # c.connection.commit()   #连接

#执行用于选择数据的sql语句
def query_sql(sql,prms=(), one=False):
    c = get_db().cursor()
    result = c.execute(sql,prms).fetchall()
    # 括号里的意思 默认情况下给我result[0],否则给我一个None
    return (result[0] if result else None) if one else result

conn = sqlite3.connect(r'./db/feedback.db',check_same_thread = False)
c = conn.cursor()

#呈现特定目录下的资源函数
@app.route('/profile/<filename>/')
def render_file(filename):
    #send_from_directory是获取特定资源函数，传递两个值，一个是目录，一个是文件名
    return send_from_directory(UPLOADS,filename)

@app.route('/')
def hello_world():
    return render_template('base.html')
    # return render_template('wenti_list.html')

"""登录"""
#登录
# @app.route('/login/',methods=['GET','POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         pwd = request.form.get('pwd')
#         sql = "select count(*) as [count] from UserInfo where UserName=? and Password=? "
#         result = query_sql(sql,(username,pwd),one=True)
#         if int(result.get('count')) > 0:
#             session['admin'] = username
#             return redirect(url_for('feedback_list'))
#         else:
#             flash("账号或密码不正确，请重新登录！")
#     return render_template('wenti_login.html')

"""退出"""
#登出
# @app.route('/sign_out/')
# def sign_out():
#     if session.get('admin',None) is None:
#         return redirect(url_for('login'))
#     else:
#         session.pop('admin')
#         # return render_template('login.html')
#         return redirect(url_for('feedback_list'))

#显示注册页
"""注册页"""
# @app.route('/register/')
# def register():
#     return render_template('register.html')

"""注册"""
 # 注册1
# @app.route('/register_user/',methods=['TET','POST'])
# def register_user():
#     if request.method == 'POST':
#         if request.form.get('username') == '':
#             flash('用户名不能为空')
#             # return "用户名不能为空"
#         elif request.form['email']== '':
#             flash( "邮箱不能为空")
#         elif request.form.get('password') == '':
#             flash( "密码不能为空")
#         else:
#             username = request.form.get('username')
#             email = request.form['email']
#             password = request.form.get('password')
#
#             conn = sqlite3.connect(DATABASE_url)
#             c = conn.cursor()
#             sql = "insert into UserInfo(Username,Email,Password) values (?,?,?)"
#             c.execute(sql,(username,email,password))
#             conn.commit()
#             conn.close()
#             return redirect(url_for('login'))
#     return render_template('register.html')
#
#         # return render_template('register.html')

@app.route('/feedback/')
def feedback():
    # categories = [(1,'产品质量'), (2,'客户服服'),(3,'购买支付')]
    sql = 'select ROWID,categoryName from category'
    categories =c.execute(sql).fetchall()
    return render_template('wenti_post.html',categories=categories)

#检测图片是否符合格式要求，
def allowd_file(filename):
    #splitext 能将文件名拆分了两个值
    _,ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED



@app.route('/post_feedback/', methods=['POST'])
def post_feedback():
    if request.method == 'POST':
        subject = request.form.get('subject')
        categoryid = request.form.get('category',1)
        username = request.form['username']
        email = request.form['email']
        body = request.form['body']
        release_time = datetime.now()
        is_processed = 0
        img_path= None
        if request.files.get('screenshort'):
            img = request.files['screenshort']
            if allowd_file(img.filename) == True:
                img_path = datetime.now().strftime('%Y%m%d%H%M%f') + os.path.splitext(img.filename)[1]
                img.save(os.path.join(UPLOADS,img_path))
                print(img_path)
        # return subject

        conn = sqlite3.connect(DATABASE_url)
        c = conn.cursor()
        sql = "insert into feedback(Subject,CategoryID,UserName,Email,Body,State,ReleaseTime,Image) " \
              "values (?,?,?,?,?,?,?,?)"
        c.execute(sql,(subject, categoryid, username, email, body,is_processed,release_time,img_path))
        conn.commit()
        conn.close()
        return redirect(url_for('feedback'))

@app.route('/admin/list/')
def feedback_list():
    if session.get('admin',None) is None:
        return redirect(url_for('login'))
    else:
        key = request.args.get('key','')
        sql = "select f.ROWID,*,categoryName from feedback f inner join category c on f.CategoryID = c.ROWID where f.subject like ? order by f.ROWID desc"
        feedbacks = query_sql(sql,('%{}%'.format(key),))
        return render_template('wenti_list.html',items=feedbacks)
        # return str(feedbacks)



@app.route('/admin/feedback/del/<id>')
def delete_feedback(id):
    # conn = sqlite3.connect(DATABASE_url)
    # c = conn.cursor()
    sql = "delete from feedback where ROWID = ?"
    # c.execute(sql,(id,))
    # conn.commit()
    # conn.close()
    execute_sql(sql,(id,))
    return redirect(url_for('feedback_list'))

@app.route('/admin/wenti_edit/<id>/')
def edit_feedback(id):
    if session['admin'] is None:
        return redirect(url_for('login'))
    else:
        # conn = sqlite3.connect(DATABASE_url)
        # c = conn.cursor()
        sql = "select ROWID,* from category "
        categories = query_sql(sql)
        # categories = c.execute(sql).fetchall()

        #获取当前id的信息并绑定至form表单，以备修改
        sql = "select ROWID,* from feedback where ROWID = ?"
        # dd = c.execute(sql,(id,)).fetchone()
        dd = query_sql(sql,(id,),one=True)
        return render_template('wenti_edit.html',categories=categories,items=dd)
        # return str(dd)

@app.route('/admin/wenti_save/', methods=['POST'])
def save_feedback():
    if request.method == 'POST':
        rowid = request.form.get('rowid',None)
        reply = request.form.get('reply')
        is_processed = 1 if request.form.get('isprocessed',0) =='on' else 0

        sql = "update feedback set Reply = ?,State = ? where rowid = ?"
        # sql = """update feedback set Reply = ?, state = ? where rowid=?"""

        conn = sqlite3.connect(DATABASE_url)
        c = conn.cursor()
        c.execute(sql,(reply,is_processed,rowid))
        conn.commit()
        conn.close()
        return redirect(url_for('feedback_list'))
        # return str(rowid)
        # return str(reply)

#创建cookies
@app.route('/set_mycookie/')
def set_mycookie():
    resp = make_response('ok')
    #timedelta设置时间段
    resp.set_cookie('username','Benson',path='/',expires=datetime.now()+ timedelta(days=7))
    return resp

#获取cookie
@app.route('/get_mycookie/')
def get_mycookei():
    ck = request.cookies.get('username',None)
    if ck:
        return ck
    else:
        return "未找到cookie"

#为导入的基于类的视图添加分配url规则
app.add_url_rule('/reg/',view_func=RegUser.as_view('reg_user'))

#login
# app.add_url_rule('/login/',view_func=UserLogin.as_view('loginn'))

#退出
# app.add_url_rule('sign_out',view_func=Sign_out.as_view('sign_out'))

if __name__ == '__main__':
    app.run()

