import sqlite3


class MainModel(object):
    db_name = 'base.sqlite3'
    db_tables = {
        'login': ['id', 'login', 'password'],
        'store': ['id', 'name', 'address', 'nickname', 'email', 'telnumber', 'secretquest', 'password'],
    }

    def __init__(self, tname):
        self.table_name = tname
        self.table_columns = self.db_tables[self.table_name]
        # поля таблицы без id
        self.table_columns_short = self.table_columns[1:]
        self.current_id = 2

        self.db = sqlite3.connect(self.db_name)
        # self.db.row_factory = sqlite3.Row
        # создание таблиц из db_tables
        for key, values in self.db_tables.items():
            self.sql = f"CREATE TABLE IF NOT EXISTS {key}("
            for value in values:
                self.sql += f'{value} INTEGER PRIMARY KEY, ' if value == 'id' else f'{value} TEXT, '
            self.sql = self.sql[:-2] + ');'
            self.db.cursor().execute(self.sql)
            self.db.commit()

    def count(self):
        return self.db.cursor().execute(f"SELECT COUNT(*) FROM {self.table_name}").fetchone()[0]

    def select_all(self):
        sql = f"SELECT {self.str_columns(id=True)} FROM {self.table_name}"
        return self.db.cursor().execute(sql).fetchall()

    def select_current(self):
        sql = f"SELECT {self.str_columns(id=True)} FROM {self.table_name} WHERE id={self.current_id}"
        return self.db.cursor().execute(sql).fetchone()

    def add(self, data):
        sql = f"INSERT INTO {self.table_name}({self.str_columns()}) VALUES({self.str_columns(data, val=True)})"
        self.db.cursor().execute(sql)
        self.db.commit()

    def delete(self):
        sql = f"DELETE FROM {self.table_name} WHERE id={self.current_id}"
        self.db.cursor().execute(sql)
        self.db.commit()

    def update(self, data):
        sql = f"UPDATE {self.table_name} SET "
        for i in range(len(data)):
            sql += f"{self.table_columns_short[i]} = '{data[i]}', "
        sql = sql[:-2] + f" WHERE id={self.current_id}"
        self.db.cursor().execute(sql)
        self.db.commit()

    def quit(self):
        self.db.close()

    def str_columns(self, columns=None, id=False, val=False):
        str_col = ''
        if columns is None:
            columns = self.table_columns_short if (id is False) else self.table_columns
        for col in columns:
            str_col += f"{col}, " if (val is False) else f"'{col}', "
        return str_col[:-2]


class LoginModel(MainModel):
    table_name = 'login'

    def __init__(self):
        super().__init__(self.table_name)


class StoreModel(MainModel):
    table_name = 'store'

    def __init__(self):
        super().__init__(self.table_name)

# TODO убрать
# m = LoginModel()
# m.add(['admin', 'password'])
# m.delete(1)
# m.current_id = 2
# m.update(['aaa', 'jjdfdj'])
# print(m.select_current())
# m.delete()
# print(m.select_all())
# print(m.count())

# m.quit()
