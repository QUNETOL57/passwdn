import getpass
import sqlite3
import cript
import settings
class User_QCLI:
    """
    Hello
    """
    def __init__(self,progect_name):
        conn = sqlite3.connect(f"{progect_name}.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users")
        except sqlite3.OperationalError:
            cursor.execute("CREATE TABLE users (login text, password text)")
            print("Creating new profile")
            login = self.login_create()
            password = self.password_create()
            login = cript.encryptDecrypt('E',login,settings.key)
            password = cript.encryptDecrypt('E',password,settings.key)
            cursor.execute(f"INSERT INTO users VALUES ('{login}', '{password}')")
            conn.commit()
            cursor.execute("SELECT * FROM users")
        self.login_in(cursor.fetchall())

    def login_create(self):
        login = input("Enter the login | ")
        return login

    def password_create(self):
        password1 = input("Enter the password | ")
        password2 = input("Enter the password again | ")
        if password1 == password2:
            return password2
            print("All right!")

    def login_in(self,llist):
        logins = [line[0] for line in llist]
        sms = ''
        while True:
            settings.clear()
            settings.print_logo()
            print(sms)
            login = input("Login: ")
            login = cript.encryptDecrypt('E',login,settings.key)
            if login not in logins:
                sms = '[X] Incorrect Login.'
                continue
            else:
                ind = logins.index(login)
            password = getpass.getpass('Password: ')
            password = cript.encryptDecrypt('E',password,settings.key)
            if password != llist[ind][1]:
                sms = '[X] Incorrect Password.'
                continue
            break
        settings.clear()


u = User_QCLI('passwdn')
