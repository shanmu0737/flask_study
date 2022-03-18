# from flask.ext.bootstrap import Bootstrap
# bootstrap = Bootstrap(app)
import sqlite3,datetime
from flask import request
from flask import Flask,render_template,url_for,redirect,g
from datetime import datetime

app = Flask(__name__)
app.debug = True

#全局连接数据库地址
DATABASE_URL = r'./db/feedback.db'

#将游标获取的tuple根据数据库列表转换为dict
def make_dicts(cursor,row):         #cursor是游标，row是行
    # enumerate(row),遍历出序号和值，分别为i和value
    return dict((cursor.description[i][0],value) for i ,value in enumerate(row))

#执行sql语句不返回结果
def execue_sql(sql,prms=()):
    c = get_db().cursor()
    c.execute(sql,prms)
    c.connection.commit()

#执行用于返回数据的sql语句
def query_sql(sql,prms=()):
    pass



#获取（建立数据库连接）,从缓存里获DB,如果没有，创建数据库连接
def get_db():
    db = getattr(g,'_database',None)
    if db is None:
        db = sqlite3.connect(DATABASE_URL)
        g._database = db
        # db = g._database = sqlite3.connect(DATABASE_URL)   #简写，多目标赋值
    return db

#关闭连接,与app的生命周期关联
@app.teardown_appcontext
def close_connection(exeption):
    db = getattr(g,'_database',None)
    if db is not None:
        db.close()





@app.route('/')
def hello_world():
    return render_template('base.html')

@app.route('/feedback/')
def feedback():
    conn = sqlite3.connect(DATABASE_URL)
    c = conn.cursor()

    # categories = [(1,'产品质量'), (2,'客户服服'),(3,'购买支付')]
    sql = 'select ROWID,categoryName from category'
    categories =c.execute(sql).fetchall()
    c.close()
    conn.close()
    return render_template('post.html',categories=categories)

#提交反馈问题，保存到数据库
@app.route('/post_feedback/',methods=['POST'])
def post_feedback():
    # conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
    # c = conn.cursor()

    if request.method == 'POST':
        #获取表单值
        subject = request.form['subject']
        categoryid = request.form.get('category',1)
        username = request.form['username']
        email = request.form['email']
        body = request.form['body']
        release_time = datetime.now()
        state = 0
        # return subject

        conn = sqlite3.connect(DATABASE_URL,check_same_thread=False)
        c = conn.cursor()   #游标
        sql = "insert into feedback(Subject, CategoryID, UserName, Email,Body,State,ReleaseTime) values (?,?,?,?,?,?,?)"
        c.execute(sql,(subject,categoryid,username,email,body,state,release_time))
        conn.commit()
        conn.close()
        return redirect(url_for('feedback'))
        # print(sql)
        # return subject

#显示提交问题列表
@app.route('/admin/list')
def feedback_list():
    conn = sqlite3.connect(DATABASE_URL,check_same_thread=False)
    c = conn.cursor()
    # sql = 'select ROWID,* from feedback order by ROWID DESC'
    sql = "select f.ROWID,f.*,c.CategoryName from feedback f inner join category c on c.ROWID = f.CategoryID order by f.ROWID DESC "
    feedbacks = c.execute(sql).fetchall()
    conn.close()
    return render_template('feedback-list.html',items=feedbacks)

#删除提交问题记录
@app.route('/admin/feedback/del/<id>')
def delete_feedback(id=0):
    conn = sqlite3.connect(DATABASE_URL,check_same_thread=False)
    c = conn.cursor()
    sql = 'delete from feedback where ROWID = ?'
    c.execute(sql,(id,))
    conn.commit()
    conn.close()
    return redirect(url_for('feedback_list'))

#编辑提交的问题
@app.route('/admin/edit/<id>')
def edit_feefback(id=None):
    #显示分类表信息
    conn = sqlite3.connect(DATABASE_URL)
    c = conn.cursor()
    sql = 'select ROWID,categoryName from category'
    categories =c.execute(sql).fetchall()

    #获取当前ID的信息并绑定到Form表，以备修改
    sql = 'select ROWID,* from feedback where ROWID=?'
    current_feedback = c.execute(sql,(id,)).fetchone()
    c.close()
    conn.close()
    return render_template('edit.html', categories=categories,item=current_feedback)
    # return str(current_feedback)

@app.route('/admin/save_edit/',methods=['POST'])
def save_feedback():
    if request.method == 'POST':
        rowid = request.form.get('rowid',None)
        reply = request.form.get('reply')
        is_state = 1 if request.form.get('isprocessed',0) == 'on' else 0

        sql = """update feedback set Reply = ?, state = ? where rowid=?"""

        conn = sqlite3.connect(DATABASE_URL,check_same_thread=False)
        c = conn.cursor()
        c.execute(sql,(reply,is_state,rowid))
        conn.commit()
        conn.close()
        return redirect(url_for('feedback_list'))


if __name__ == '__main__':
    app.run()



























