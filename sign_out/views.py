from flask import redirect,url_for,session
from flask import Blueprint
import sqlite3

sign_outt = Blueprint('sign_outt',__name__)

@sign_outt.route('/')
def sign_out():
    if session.get('admin',None) is None:
        return redirect(url_for('login_bag'))
    else:
        session.pop('admin')
        # return render_template('login_bag.html')
        return redirect(url_for('feedback_list'))