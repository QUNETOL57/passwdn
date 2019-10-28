import sqlite3

db = sqlite3.connect('base.sqlite3')
db.row_factory = sqlite3.Row
# dictt = db.cursor().execute(f"SELECT * FROM store").fetchall()

a = db.cursor().execute("SELECT * from store WHERE id=:id", {"id": '1'}).fetchone()
print(a)