from flask import Flask,request,render_template
from flask import Blueprint
from flask.views import MethodView

article = Blueprint('articles',__name__)

# @article.route('/articles/')
# def article_list():
#     return render_template('reg.html')

#
# @article.route('/articles/<id>/')
# def article_detail(id=None):
#     items = {'id':id}
#     return render_template('reg.html',items=items)

class ArticleListView(MethodView):
    def get(self):
        return render_template('news.html')

    def post(self):
        pass

article.add_url_rule('/',view_func=ArticleListView.as_view('article_list'))

class ArticleDetailView(MethodView):
    def get(self,id=None):
        item = {'id':id}
        return render_template('news.html',item=item)



article.add_url_rule('/<id>/',view_func=ArticleDetailView.as_view('article_detail'))