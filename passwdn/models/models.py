import sqlite3

class ContactModel(object):
    def __init__(self):
        # Create a database in RAM
        # self._db = sqlite3.connect(':memory:')
        self._db = sqlite3.connect('base.sqlite3')
        self._db.row_factory = sqlite3.Row

        # Create the basic contact table.
        self._db.cursor().execute('''
            CREATE TABLE IF NOT EXISTS contacts(
                id INTEGER PRIMARY KEY,
                name TEXT,
                phone TEXT,
                address TEXT,
                email TEXT,
                notes TEXT)
        ''')
        self._db.commit()

        # Current contact when editing.
        self.current_id = None

    def add(self, contact):
        self._db.cursor().execute(
            '''
            INSERT INTO contacts(name, phone, address, email, notes)
            VALUES(:name, :phone, :address, :email, :notes)''', contact)
        self._db.commit()

    def get_summary(self):
        return self._db.cursor().execute(
            "SELECT name, id from contacts").fetchall()

    def get_contact(self, contact_id):
        return self._db.cursor().execute("SELECT * from contacts WHERE id=:id",
                                         {
                                             "id": contact_id
                                         }).fetchone()

    def get_current_contact(self):
        if self.current_id is None:
            return {
                "name": "",
                "address": "",
                "phone": "",
                "email": "",
                "notes": ""
            }
        else:
            return self.get_contact(self.current_id)

    def update_current_contact(self, details):
        if self.current_id is None:
            self.add(details)
        else:
            self._db.cursor().execute(
                '''
                UPDATE contacts SET name=:name, phone=:phone, address=:address,
                email=:email, notes=:notes WHERE id=:id''', details)
            self._db.commit()

    def delete_contact(self, contact_id):
        self._db.cursor().execute(
            '''
            DELETE FROM contacts WHERE id=:id''', {"id": contact_id})
        self._db.commit()