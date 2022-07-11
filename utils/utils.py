from flask import Blueprint, render_template, request, redirect
from sql.SQLMaster import SQLMaster
from flask import session

SQLserver = SQLMaster('.\\utils\\sql')


def remove_string(id):
    SQLserver.request('delete_string.sql', id=id)


def add_List(idCustomer, strings):
    pass


def remove_list(id):
    strings = SQLserver.request('find_string.sql', id=id)
    for s in strings:
        remove_string(s['idString'])
    SQLserver.request('delete_list.sql', id=id)


def add_customer(name, city):
    pass


def remove_customer(id):
    lists = SQLserver.request('find_list.sql', id=id)
    for l in lists:
        remove_list(l['idlist'])
    SQLserver.request('delete_customer.sql', id=id)


def remove_part(id):
    strings = SQLserver.request('find_string_by_part.sql', id=id)
    if strings:
        for s in strings:
            remove_string(s['idString'])
    SQLserver.request('delete_part.sql', item_id=id)


def add_to_basket(item_id: str, item: dict) -> None:
    basket = session.get('basket', [])
    if basket:
        for i in range(len(basket)):
            if basket[i][0] == item_id:
                basket[i][2] += 1
                session['basket'] = basket
                return None
    basket.append([item_id, item, 1])
    session['basket'] = basket


def clear_basket() -> None:
    if 'basket' in session:
        session.pop('basket')
