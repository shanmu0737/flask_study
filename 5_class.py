from flask import Flask
from flask import render_template
from flask import request
from urllib.parse import unquote
app = Flask(__name__)


'''
第五节课 讲解requests内容
'''

@app.route('/')
def hello_world():
    return 'Hello World! Flask,today'

@app.route('/reg/')
def reg():
    return render_template('reg.html')

@app.route('/headers/')
def headers():
    data = dict(request.headers)
    return str(data)


@app.route('/doreg/',methods=['POST'])
def do_reg():
    name = request.form['username']
    # pwd = request.form['pwd']         #用form获取请求值，常用
    # pwd = request.form.get('pwd')       #用form.get获取请求址
    pwd = request.values['pwd']         #用values获取请于值
    return "注册成功,姓名：{}，密码：{}".format(name, pwd)

@app.route('/rqq/')
def hello_rq():
    path = request.path
    methon = request.method
    name = unquote(request.args.get('name','未找到'))
    return name

    return methon

if __name__ == '__main__':
    app.run()
