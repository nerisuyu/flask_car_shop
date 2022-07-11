from flask import Blueprint, render_template, request, redirect
from sql.SQLMaster import SQLMaster
from flask import session
from utils.utils import *
from access import group_permission_decorator
lists_app = Blueprint('lists', __name__, template_folder='templates')
SQLserver = SQLMaster('.\\blueprints\\lists\\sql')


@lists_app.route('/', methods=['GET', 'POST'])
@group_permission_decorator
def choose_customer():
    if request.method == 'POST':
        session['customer_id'] = request.form.get('id')
        return redirect("/lists/pick")
    else:
        return render_template('choose_customer.html', items=SQLserver.request('select_all_customers.sql'))


@lists_app.route('/pick', methods=['GET', 'POST'])
def choose_list():
    if request.method == 'POST':
        session['list_id'] = request.form.get('id')
        return redirect("/lists/show")
    else:
        if session.get('customer_id') is None:
            return redirect("/lists")
        return render_template('choose_list.html',
                               name=SQLserver.request('find_name.sql', id=session.get('customer_id')),
                               items=SQLserver.request('select_lists.sql', idCustomer=session.get('customer_id')))


@lists_app.route('/show', methods=['GET', 'POST'])
def show_list():
    strings = SQLserver.request('select_string.sql', id=session.get('list_id'))
    date = SQLserver.request('get_date.sql', id=session.get('list_id'))
    pairs = []
    summ = 0
    for s in strings:
        part = SQLserver.request('find_part.sql', id=s['idPart'])[0]
        summ = summ + part['costPart'] * s['amountString']
        pairs.append([s, part])
    return render_template('show_list.html', items=pairs, date=date, summ=summ)


@lists_app.route('/remove_list')
def rem_list():
    remove_list(session.get('list_id'))
    return redirect('/lists/pick')


@lists_app.route('/insert', methods=['GET', 'POST'])
def list_orders_handler():
    if request.method == 'GET':
        basket = session.get('basket', [])
        items = SQLserver.request('select_all_parts.sql')
        summ = 0
        for item in basket:
            a = item[1]
            summ = summ + a['costPart'] * item[2]
        session['summ']=summ
        return render_template('basket_order_list.html', basket=basket, items=items, summ=summ)
    else:
        item_id = request.form['item_id']
        items = SQLserver.request('find_part.sql', id=item_id)  # select part with item_id
        print(items)
        if items:
            add_to_basket(item_id, items[0])
        # else:
        #    return render_template('not_found_item.html')
        return redirect('/lists/insert')


@lists_app.route('/clear')
def clear_basket_handler():
    clear_basket()
    return redirect('/lists/insert')


@lists_app.route('/buy')
def buy_basket_handler():
    cost = session.get('summ')
    idCustomer = session.get('customer_id')
    if 'basket' in session:
        basket = session.get('basket')
        SQLserver.request('form_list.sql', costList=cost, idCustomer=idCustomer)
        id_list = SQLserver.request('get_list_id.sql', idCustomer=idCustomer)
        print(id_list)
        id=id_list[0]['idList']
        for item in basket:
            SQLserver.request('form_string.sql',amount=item[2],idList=id,idPart=item[0])
        clear_basket()
        return redirect('/lists/pick')
    return redirect('/lists/clear')
