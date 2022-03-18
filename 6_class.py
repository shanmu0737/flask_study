from flask import Flask, request,make_response,render_template,redirect,url_for
import json
# from flask import render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.debug = True

'''
第六节课  讲解
render_template 模板
redirect 重定向
url_for  用于生成一个地址

'''

@app.route('/')
def hello_world():
    return 'Hello World! 首页~~~~'

@app.route('/a/')
def rq_a():
    # return redirect(url_for('rq_b'))
    # return 'rq_a'
    return render_template('pate_a.html')



@app.route('/about-us/')
def rq_b():
    return render_template('pate_b.html')



@app.route('/rq/')
def test_rq():
    data = {}
    data['ip'] = request.remote_addr
    # data['environ'] = request.environ
    data['url'] = request.url
    data['full_path'] = request.full_path
    return str(data)



if __name__ == '__main__':
    app.run()