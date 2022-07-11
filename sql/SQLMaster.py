from sql.SQLConnect import SQLConnect
from sql.SQLProvider import SQLProvider
import pymysql
from tabulate import tabulate


class SQLMaster:
    def __init__(self,filename):
        #self.db_request = SQLProvider(r'.\sql\sql')  # Сюда путь до папки с запросами
        self.db_request = SQLProvider(filename)  # Сюда путь до папки с запросами

    def request(self, filename, **kwargs) -> dict:
        with SQLConnect() as cursor:
            request = self.db_request.get(filename, **kwargs)
            result = []
            if cursor is None:
                raise ValueError('Cursor is None')
            elif cursor:
                cursor.execute(request)
                schema = [column[0] for column in cursor.description]
                print(schema)
                for item in cursor.fetchall():
                    result.append(dict(zip(schema, item)))
                print('resulting ', result)
                return result

# todo это хуйня переделай
