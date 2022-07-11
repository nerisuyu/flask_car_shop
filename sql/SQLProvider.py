import os
from string import Template


class SQLProvider:
    def __init__(self, file_path):
        self._scripts = {}

        for file in os.listdir(file_path):
            _, expression = os.path.splitext(file)
            if expression == '.sql':
                self._scripts[file] = Template(open(f'{file_path}/{file}', 'r', encoding="utf-8-sig").read())

    def get(self, file_name, **kwargs):
        f=file_name
        k=kwargs
        return self._scripts[file_name].substitute(**kwargs)
