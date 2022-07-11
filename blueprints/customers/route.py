from flask import Blueprint, render_template, request
from sql.SQLMaster import SQLMaster
from utils.utils import *
from access import group_permission_decorator

customers_app = Blueprint('customers', __name__, template_folder='templates')
SQLserver = SQLMaster('.\\blueprints\\customers\\sql')


@customers_app.route('/', methods=['GET', 'POST'])
@group_permission_decorator
def edit_customers():
    if request.method == 'POST':
        id = request.form.get('id')
        remove_customer(id)
        return render_template('customers_list.html', items=SQLserver.request('select_all_customers.sql'))
    else:
        return render_template('customers_list.html', items=SQLserver.request('select_all_customers.sql'))

        #todo добаить лист заголовков как нить
        #todo удалять вместе с внешними ключами

@customers_app.route('/insert', methods=['GET', 'POST'])
@group_permission_decorator
def insert_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form.get('city')
        SQLserver.request('insert_customer.sql', name=name,city=city)
        return render_template('customer_insert.html')
    else:
        return render_template('customer_insert.html')
