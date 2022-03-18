from flask import render_template,request,session,redirect,url_for
from flask.views import View,MethodView

#基于类的视图
class RegUser(View):
    methods = ['GET','POST']
    def dispatch_request(self):
        return render_template('reg.html')

#基于方法的类
class dfd(MethodView):
    def get(self):
        return render_template('reg.html')

    def post(self):
        # if request.method == 'POST':
        #     pass
        return None

#登录
class UserLogin(View):
    methods = ['GET', 'POST']
    def dispatch_request(self):
        return render_template('login.html')


#退出
class Sign_out(View):
    def dispatch_request(self):
        if session.get('admin',None) is None:
            return render_template('login.html')
        else:
            session.pop('admin')
            return render_template('feedback-list.html')
