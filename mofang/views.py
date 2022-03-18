from flask import Flask,render_template
from flask import Blueprint,request,flash,g,make_response,redirect,url_for
import sqlite3

mofang = Blueprint('mofang',__name__)

DATABASE_url = r'./db/feedback.db'


@mofang.route('/')
def mofang_list():
    return render_template('register.html')


@mofang.route('/<id>/')
def mofang_num(id=None):
    return '第{}个魔方'.format(id)

@mofang.route('/register_user/',methods=['GET','POST'])
def register_user():
    if request.method == 'POST':
        if request.form.get('username') == '':
            flash('用户名不能为空')
            # return "用户名不能为空"
        elif request.form['email']== '':
            flash( "邮箱不能为空")
        elif request.form.get('password') == '':
            flash( "密码不能为空")
        else:
            username = request.form.get('username')
            email = request.form['email']
            password = request.form.get('password')

            conn = sqlite3.connect(DATABASE_url)
            c = conn.cursor()
            sql = "insert into UserInfo(Username,Email,Password) values (?,?,?)"
            c.execute(sql,(username,email,password))
            conn.commit()
            conn.close()
            return str(username)
            # return redirect(url_for('login_bag'))
    # return render_template('register.html')
