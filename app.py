from flask import Flask, render_template, session
from blueprints.requests.route import requests_app
from blueprints.auth.route import auth_app
from blueprints.edit.route import edit_app
from blueprints.basket.route import basket_app
from blueprints.customers.route import customers_app
from blueprints.lists.route import lists_app
import json
from access import group_permission_decorator
from flask_bootstrap import Bootstrap
from utils.utils import *


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.register_blueprint(lists_app,url_prefix='/lists')
app.register_blueprint(customers_app, url_prefix='/customers')
app.register_blueprint(basket_app, url_prefix='/basket')
app.register_blueprint(requests_app, url_prefix='/requests')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(edit_app, url_prefix='/edit')
app.config['access_config'] = json.load(open("configs/access.json"))
app.config['SECRET_KEY'] = 'my secret key'

@app.route('/')
def index():

    return render_template('indexBootstrap.html', )


@app.route('/exit')
@group_permission_decorator
def exit_page():
    session.clear()
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
