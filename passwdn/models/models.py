import sqlite3


#
# class ContactModel(object):
#     def __init__(self):
#         # Create a database in RAM
#         # self._db = sqlite3.connect(':memory:')
#         self._db = sqlite3.connect('base.sqlite3')
#         self._db.row_factory = sqlite3.Row
#
#         # Create the basic contact table.
#         self._db.cursor().execute('''
#             CREATE TABLE IF NOT EXISTS contacts(
#                 id INTEGER PRIMARY KEY,
#                 name TEXT,
#                 phone TEXT,
#                 address TEXT,
#                 email TEXT,
#                 notes TEXT)
#         ''')
#         self._db.commit()
#
#         # Current contact when editing.
#         self.current_id = None
#
#     def add(self, contact):
#         self._db.cursor().execute(
#             '''
#             INSERT INTO contacts(name, phone, address, email, notes)
#             VALUES(:name, :phone, :address, :email, :notes)''', contact)
#         self._db.commit()
#
#     def get_summary(self):
#         return self._db.cursor().execute(
#             "SELECT name, id from contacts").fetchall()
#
#     def get_contact(self, contact_id):
#         return self._db.cursor().execute("SELECT * from contacts WHERE id=:id",
#                                          {
#                                              "id": contact_id
#                                          }).fetchone()
#
#     def get_current_contact(self):
#         if self.current_id is None:
#             return {
#                 "name": "",
#                 "address": "",
#                 "phone": "",
#                 "email": "",
#                 "notes": ""
#             }
#         else:
#             return self.get_contact(self.current_id)
#
#     def update_current_contact(self, details):
#         if self.current_id is None:
#             self.add(details)
#         else:
#             self._db.cursor().execute(
#                 '''
#                 UPDATE contacts SET name=:name, phone=:phone, address=:address,
#                 email=:email, notes=:notes WHERE id=:id''', details)
#             self._db.commit()
#
#     def delete_contact(self, contact_id):
#         self._db.cursor().execute(
#             '''
#             DELETE FROM contacts WHERE id=:id''', {"id": contact_id})
#         self._db.commit()


class MainModel(object):
    db_name = 'base.sqlite3'
    db_tables = {
        'login': ['id', 'login', 'password'],
        'store': ['id', 'name', 'address', 'nickname', 'email', 'telnumber', 'secretquest', 'password'],
    }

    def __init__(self, tname):
        self.table_name = tname
        self.table_columns = self.db_tables[self.table_name]
        self.current_id = None
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

    def select(self):
        sql = f"SELECT {self.str_columns(id=True)} from {self.table_name}"
        return self.db.cursor().execute(sql).fetchall()

    def add(self, data):
        sql = f"INSERT INTO {self.table_name}({self.str_columns()}) VALUES({self.str_columns(data, val=True)})"
        self.db.cursor().execute(sql)
        self.db.commit()

    def delete(self, id):
        sql = f"DELETE FROM {self.table_name} WHERE id={id}"
        self.db.cursor().execute(sql)
        self.db.commit()

    def update(self, values):
        sql = f"UPDATE {self.table_name} SET "
        for i in range(values):
            sql += f"{values[i]}={self.table_columns[i + 1]}, "
        sql = sql[:-2] + f"WHERE id={self.current_id}"

    def quit(self):
        self.db.close()

    def str_columns(self, columns=None, id=False, val=False):
        str_col = ''
        if columns is None:
            columns = self.table_columns[1:] if (id is False) else self.table_columns
        for col in columns:
            str_col += f"{col}, " if (val is False) else f"'{col}', "
        return str_col[:-2]


class LoginModel(MainModel):
    table_name = 'login'

    def __init__(self):
        super().__init__(self.table_name)


m = LoginModel()
# m.add(['admin', 'password'])
# m.delete(1)
print(m.select())
m.quit()

# class LoginModel(object):
#
#     table_name = 'login'
#     table_columns = []
#
#     def __init__(self):
#         self._db = sqlite3.connect('base.sqlite3')
#         self._db.row_factory = sqlite3.Row
#
#         # Create the basic contact table.
#         self._db.cursor().execute('''
#             CREATE TABLE IF NOT EXISTS login(
#                 id INTEGER PRIMARY KEY,
#                 login TEXT,
#                 password TEXT)
#         ''')
#         self._db.commit()
#
#         # Current contact when editing.
#         self.current_id = None
#
#     def add(self, contact):
#         self._db.cursor().execute(
#             '''
#             INSERT INTO contacts(name, phone, address, email, notes)
#             VALUES(:name, :phone, :address, :email, :notes)''', contact)
#         self._db.commit()
#
#     def get_summary(self):
#         return self._db.cursor().execute(
#             "SELECT name, id from contacts").fetchall()
#
#     def get_contact(self, contact_id):
#         return self._db.cursor().execute("SELECT * from contacts WHERE id=:id",
#                                          {
#                                              "id": contact_id
#                                          }).fetchone()
#
#     def get_current_contact(self):
#         if self.current_id is None:
#             return {
#                 "name": "",
#                 "address": "",
#                 "phone": "",
#                 "email": "",
#                 "notes": ""
#             }
#         else:
#             return self.get_contact(self.current_id)
#
#     def update_current_contact(self, details):
#         if self.current_id is None:
#             self.add(details)
#         else:
#             self._db.cursor().execute(
#                 '''
#                 UPDATE contacts SET name=:name, phone=:phone, address=:address,
#                 email=:email, notes=:notes WHERE id=:id''', details)
#             self._db.commit()
#
#     def delete_contact(self, contact_id):
#         self._db.cursor().execute(
#             '''
#             DELETE FROM contacts WHERE id=:id''', {"id": contact_id})
#         self._db.commit()
