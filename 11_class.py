# from flask.ext.bootstrap import Bootstrap
# bootstrap = Bootstrap(app)
import sqlite3
from flask import request
from flask import Flask,render_template,url_for,redirect,g,flash,send_from_directory,session
from datetime import datetime
import os

"""
seng_from_directory    通过某一个目录来发送消息
"""

app = Flask(__name__)
app.debug = True
app.secret_key = "kfjkldsjdsj234324@34323"

"""
第11课主讲内容
1、图片上传功能
2、登录错误提示语
flask
app="fkdlfkl"
login_bag.html页，接收flash，
"""

#全局连接数据库地址
DATABASE_URL = r'./db/feedback.db'
#上传图片的全局路径
UPLOAD_FOLDER = r'./uploads'
#文件上传类型可以上传多种，这里只允许上传图片，限制图片上传格式
ALLOWED_EXTENSIONS = ['.jpg','.png','.gif','.jpeg']

#呈现特定目录下的资源
@app.route('/profile/<filename>')    #设置为全局函数
def render_file(filename):
    return send_from_directory(UPLOAD_FOLDER,filename)   #第一个值是路径，第二个是文件名


#检查文件是否允许上传
def allowed_file(filename):
    #filename = 'abcd.JPG'
    _,ext = os.path.splitext(filename)  #splitext作用是把上传的文件截取为两个值，如果要忽略一个值，可输入下划线
    return ext.lower() in ALLOWED_EXTENSIONS    #lower()函数把大写转换为小写


#将游标获取的tuple根据数据库列表转换为dict
def make_dicts(cursor,row):         #cursor是游标，row是行
    # enumerate(row),遍历出序号和值，分别为i和value
    return dict((cursor.description[i][0],value) for i ,value in enumerate(row))

#获取（建立数据库连接）,从缓存里获DB,如果没有，创建数据库连接
def get_db():
    db = getattr(g,'_database',None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_URL)   #简写，多目标赋值
        # row_factory为行工厂，make_dicts不加括号，代表调用，加上括号表示立即执行
        db.row_factory = make_dicts
    # print("DB=",db)
    return db

#执行sql语句不返回结果
def execue_sql(sql,prms=()):
    c = get_db().cursor()
    c.execute(sql,prms)
    c.connection.commit()

#执行用于返回数据的sql语句
def query_sql(sql,prms=(), one=False):
    c = get_db().cursor()
    result = c.execute(sql,prms).fetchall()
    c.close()
    #设置默认获取内容不为单行，如果不是单行，返回result
    #如果返回值不为一行，返回None
    return (result[0] if result else None) if one else result




#关闭连接,装饰器与app的生命周期关联
@app.teardown_appcontext
def close_connection(exeption):
    db = getattr(g,'_database',None)
    if db is not None:
        db.close()



@app.route('/')
def hello_world():
    return render_template('base.html')

@app.route('/login_bag/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        sql = 'select count(*) as [Count] from UserInfo where UserName = ? and Password = ?'
        result = query_sql(sql,(username,pwd), one=True)
        # session.get('admin', None)
        if int(result.get('Count')) > 0:
            # session.get('admin',None)= username
            # session['admin','None'] = username
            return redirect(url_for('feedback_list'))
        flash('用户名或密码错误')
    return  render_template('login.html')

@app.route('/feedback/')
def feedback():
    conn = sqlite3.connect(DATABASE_URL)
    c = conn.cursor()

    # categories = [(1,'产品质量'), (2,'客户服服'),(3,'购买支付')]
    sql = 'select ROWID,categoryName from category'
    categories =c.execute(sql).fetchall()
    c.close()
    conn.close()
    return render_template('post.html', categories=categories)

#提交反馈问题，保存到数据库
@app.route('/post_feedback/',methods=['POST'])
def post_feedback():
    conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
    c = conn.cursor()

    if request.method == 'POST':
        #获取表单值
        subject = request.form['subject']
        categoryid = request.form.get('category',1)
        username = request.form['username']
        email = request.form['email']
        body = request.form['body']
        release_time = datetime.now()
        state = 0
        img_path = None     #等于None，在数据库里存一个空
        if request.files.get('screenshort',None):
            #获取图片上传，并且获取文件名，以便于和其它字段一并插入数据库
            img = request.files['screenshort']
            if allowed_file(img.filename):
                img_path = datetime.now().strftime('%Y%m%d%H%M%f') + os.path.splitext(img.filename)[1]
                img.save(os.path.join(UPLOAD_FOLDER,img_path))  #保存，连接文件名和后缀，join用来连接
                print(img_path)

        conn = sqlite3.connect(DATABASE_URL,check_same_thread=False)
        c = conn.cursor()   #游标
        sql = "insert into feedback(Subject, CategoryID, UserName, Email,Body,State,ReleaseTime,Image) values (?,?,?,?,?,?,?,?)"
        c.execute(sql,(subject,categoryid,username,email,body,state,release_time,img_path))
        conn.commit()
        conn.close()
        return redirect(url_for('feedback'))
        # print(sql)
        # return subject

#显示提交问题列表
@app.route('/admin/list')
def feedback_list():
    key = request.args.get('key', '')
    sql = "select f.ROWID,f.*,c.CategoryName from feedback f inner join category c on " \
          "c.ROWID = f.CategoryID where f.Subject like ? order by f.ROWID DESC "
    feedbacks = query_sql(sql, ('%{}%'.format(key),))   # ？ 加入了模糊查询
    # return str(feedbacks)
    # print(feedbacks)
    return render_template('feedback-list.html', items=feedbacks)


#删除提交问题记录
@app.route('/admin/feedback/del/<id>')
def delete_feedback(id=0):
    sql = 'delete from feedback where ROWID = ?'
    execue_sql(sql,(id,))
    return redirect(url_for('feedback_list'))

#编辑提交的问题
@app.route('/admin/edit/<id>')
def edit_feefback(id=None):
    if session.get('admin',None) is None:
        return redirect(url_for('login'))
    else:
        sql = 'select ROWID,categoryName from category'
        categories =query_sql(sql)

        #获取当前ID的信息并绑定到Form表，以备修改
        sql = 'select ROWID,* from feedback where ROWID=?'
        current_feedback = query_sql(sql,(id,), one=True)    #one 得到一条数据
        print(str(current_feedback))
        return render_template('edit.html', categories=categories, item=current_feedback)
        # return str(current_feedback)

@app.route('/admin/save_edit/',methods=['POST'])
def save_feedback():
    if request.method == 'POST':
        subject = request.form.get('subject')
        rowid = request.form.get('rowid',None)
        reply = request.form.get('reply')
        is_state = 1 if request.form.get('isprocessed',0) == 'on' else 0

        sql = 'update feedback set Subject = ?, Reply = ?, State = ? where rowid=?'

        conn = sqlite3.connect(DATABASE_URL,check_same_thread=False)
        c = conn.cursor()
        c.execute(sql,(subject,reply,is_state,rowid))
        conn.commit()
        conn.close()
        return redirect(url_for('feedback_list'))


if __name__ == '__main__':
    app.run()



























