import os
from access import group_permission_decorator
from flask import Blueprint, render_template, request, current_app, session, redirect
from sql.SQLMaster import SQLMaster


SQLserver = SQLMaster('.\\blueprints\\basket\\sql')
basket_app = Blueprint('basket', __name__, template_folder='templates')


@basket_app.route('/', methods=['GET', 'POST'])
@group_permission_decorator
def list_orders_handler():
    if request.method == 'GET':
        basket = session.get('basket', [])
        items = SQLserver.request('select_all_parts.sql')
        summ=0
        for item in basket:
            a=item[1]
            summ=summ+a['costPart']*item[2]
        return render_template('basket_order_list.html', basket=basket, items=items,summ=summ)
    else:
        item_id = request.form['item_id']
        items = SQLserver.request('find_part.sql', idPart=item_id)  # select part with item_id
        print(items)
        if items:
            add_to_basket(item_id, items[0])
        # else:
        #    return render_template('not_found_item.html')
        return redirect('/basket')


@basket_app.route('/clear')
def clear_basket_handler():
    clear_basket()
    return redirect('/basket')


@basket_app.route('/buy')
def buy_basket_handler():
    cost = 0
    idCustomer = 1
    if 'basket' in session:
        basket = session.get('basket')
        SQLserver.request('form_list.sql', costList=cost, idCustomer=idCustomer)
        id_list = SQLserver.request('get_list_id.sql', idCustomer=idCustomer)
        id=id_list[0]['idList']
        for item in basket:
            SQLserver.request('form_string.sql',amount=item[2],idList=id,idPart=item[0])
        return render_template("thanks.html")
    return redirect('/basket/clear')
