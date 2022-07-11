from flask import Blueprint, session, render_template, request, current_app
from sql.SQLMaster import SQLMaster
import json
auth_app = Blueprint('auth', __name__, template_folder='templates')
SQLserver=SQLMaster('.\\blueprints\\auth\\sql')
@auth_app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        session.clear()
        return render_template('authorization_formBootsrap.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        print(login, password)
        role=SQLserver.request('find_user.sql', name=login, password=password)
        print(role)
        if not role:
            print("err")
            return render_template('authorization_error.html')
        else:
            session['group_name']=role[0]['roleUsers']
            return render_template('authorization_success.html',role=role[0]['roleUsers'])

