from flask import Blueprint, render_template, request
from sql.SQLMaster import SQLMaster
from utils.utils import *
edit_app = Blueprint('edit', __name__, template_folder='templates')
SQLserver = SQLMaster('.\\blueprints\\edit\\sql')
from access import group_permission_decorator


@edit_app.route('/', methods=['GET', 'POST'])
@group_permission_decorator
def edit_part():
    if request.method == 'POST':
        id = request.form.get('item_id')
        remove_part(id)
        return render_template('parts_list.html', items=SQLserver.request('edit_part.sql'))
    else:
        return render_template('parts_list.html', items=SQLserver.request('edit_part.sql'))

        #todo добаить лист заголовков как нить
        #todo удалять вместе с внешними ключами

@edit_app.route('/insert', methods=['GET', 'POST'])
def insert_part():
    if request.method == 'POST':

        type = request.form.get('type')
        material = request.form.get('material')
        weight = request.form.get('weight')
        cost = request.form.get('cost')
        SQLserver.request('insert_part.sql', type=type, material=material, weight=weight, cost=cost)
        print('insert')
        return render_template('part_insert.html')
    else:
        return render_template('part_insert.html')
