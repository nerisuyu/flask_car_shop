from functools import wraps
from flask import Blueprint, render_template, request
from sql.SQLMaster import SQLMaster
from access import group_permission_decorator
from tabulate import tabulate
import json

requests_app = Blueprint('requests', __name__, template_folder='templates')
SQLserver = SQLMaster('.\\blueprints\\requests\\sql')




@requests_app.route('/')
@group_permission_decorator
def requests_index():
    return render_template('requests_indexBootstrap.html')


@requests_app.route('/request1', methods=['GET', 'POST'])
@group_permission_decorator
def request1():
    # handle the POST request
    if request.method == 'POST':
        date1 = request.form.get('date1')
        date2 = request.form.get('date2')
        return render_template('result1.html',
                               result=tabulate(SQLserver.request('request1.sql', date1=date1, date2=date2),
                                               tablefmt='html',
                                               stralign='center',
                                               headers='keys'),
                               header='Покупатели, заключившие договора между {} и {}'.format(date1, date2))
    else:
        return render_template('request1.html')


@requests_app.route('/request2', methods=['GET', 'POST'])
@group_permission_decorator
def request2():
    # handle the POST request
    if request.method == 'POST':
        days = request.form.get('days')
        return render_template('result1.html',
                               result=tabulate(SQLserver.request('request2.sql', days=days),
                                               tablefmt='html',
                                               stralign='center',
                                               headers='keys'),
                               header='Покупатели, заключившие договора за последние {} дней'.format(days))
    else:
        return render_template('request2.html')
