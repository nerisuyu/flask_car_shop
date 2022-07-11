import pymysql
from pymysql import connect
from pymysql.err import OperationalError
import json

dbconfig = json.load(open(".\\configs\\configDataBase.json", 'r'))

errors = {1049: 'Ошибка в имени базы данных',
          1045: 'Ошибка в имени пользователя или пароле',
          2003: 'Неправильный host',
          1064: 'Ошибка в синтаксисе Select-запроса',
          1054: 'Несуществующий столбец таблицы',
          1146: 'Несуществующая таблица'}


class SQLConnect:

    def __init__(self):
        self.config = dbconfig
        self.cursor = None
        self.conn = None

    def __enter__(self):
        print('enter')
        try:
            self.connect()
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError:
            return None

    def connect(self):
        self.config = json.load(open(".\\configs\\configDataBase.json", 'r'))
        try:
            self.cursor = pymysql.cursors.DictCursor
            self.conn = connect(**self.config)
            return 'Success'
        except OperationalError as err:
            return errors.get(err.args[0])

    def __exit__(self, exc_type, exc_value, exc_trace):
        if exc_value:
            print(errors.get(exc_value.args[0]))
        if self.conn is not None and self.cursor is not None:
            self.conn.commit()
            self.conn.close()
        print('exit')
        return True
