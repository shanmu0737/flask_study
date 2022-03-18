from flask import Flask,render_template
from flask import Blueprint

product = Blueprint('product',__name__)

@product.route('/')
def product_list():
    # return '产品列表页'
    return render_template('product.html')

@product.route('/<id>/')
def product_detain(id=None):
    # return '产品详情页' + str(id)
    item={'id':id}
    return render_template('product.html',item=item)