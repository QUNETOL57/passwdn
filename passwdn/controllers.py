from cryptography.fernet import Fernet
import os.path
import sys
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


class GenPass(object):
    def __init__(self):
        pass


class CryptController(object):
    def __init__(self):
        self.step = 13
        self.file = sys.path[0] + '/local/' + 'cipher.key'
        self.alpha = ''.join(map(chr, range(ord(' '), ord('я') + 1)))
        self.key = self.get_key()
        self.cipher = Fernet(bytes(str(self.get_key()), encoding='utf-8'))

    def gen_key(self):
        cipher_key = Fernet.generate_key()
        file_handler = open(self.file, 'w')
        file_handler.write(str(cipher_key)[2:-1])
        file_handler.close()
        return str(cipher_key)[2:-1]

    def get_key(self):
        if os.path.isfile(self.file):
            file_handler = open(self.file, 'r')
            return file_handler.read()
        else:
            self.gen_key()

    def encode(self, text):
        text = bytes(text, encoding='utf-8')
        encrypted_text = self.cipher.encrypt(text)
        enc = str(encrypted_text)[2:-1]
        return enc.translate(str.maketrans(self.alpha, self.alpha[self.step:] + self.alpha[:self.step]))

    def decode(self, text):
        text = text.translate(str.maketrans(self.alpha[self.step:] + self.alpha[:self.step], self.alpha))
        dec = bytes(text, encoding='utf-8')
        decrypted_text = self.cipher.decrypt(dec)
        return str(decrypted_text)[2:-1]


class MainAction(object):
    def __init__(self, login_model, store_model):
        self.crypt_controller = CryptController()
        self.synchronization = Synchronization()
        self.login_model = login_model
        self.store_model = store_model
        self.prof_init = None

    def synchron(self):
        self.synchronization.authorization()
        # TODO предусмотреть для нескольких пользователей
        data_login = self.synchronization.read()[0]
        login = self.login_model.select_current()
        if data_login[1] == login[1] and data_login[2] == login[2]:
            if data_login[3] > login[3]:
                data_all = self.synchronization.read(False)
                self.store_model.delete_all()
                for data in data_all:
                    self.store_model.add(data[1:])
                # else:
                #     login_data = self.login_model.select_all()
                #     store_data = self.store_model.select_all()
                #     self.synchronization.write(login_data, store_data)

    def login_in(self, login, password):
        # TODO сделать инициализацию после идентификации
        log = self.login_model.select_all()
        for i in range(len(log)):
            for j in range(1, len(log[i]), 3):
                if self.crypt_controller.decode(log[i][j]) == login:
                    if self.crypt_controller.decode(log[i][j+1]) == password:
                        self.login_model.current_id = log[i][0]
                        self.synchron()
                        return True

    def create_prof(self, login, password):
        # TODO сделать создание пользователя
        data = [self.crypt_controller.encode(login), self.crypt_controller.encode(password)]
        self.login_model.add(data)
        print(self.crypt_controller.decode(data[0]), self.crypt_controller.decode(data[1]))

    def get_current(self):
        if self.store_model.current_id is None:
            return {
                'name': '',
                'address': '',
                'nickname': '',
                'email': '',
                'telnumber': '',
                'secretquest': '',
                'password': ''
            }
        else:
            dec = self.decrypt_data(self.store_model.select_current())
            return self.convert(dec)

    def update_current(self, data):
        data = self.encrypt_data(self.convert(data, True))
        if self.store_model.current_id is None:
            self.store_model.add(data)
        else:
            self.store_model.update(data)
        self.login_model.session_update()
        login_data = self.login_model.select_all()
        store_data = self.store_model.select_all()
        self.synchronization.write(login_data, store_data)

    def delete_current(self):
        self.store_model.delete()
        self.login_model.session_update()
        login_data = self.login_model.select_all()
        store_data = self.store_model.select_all()
        self.synchronization.write(login_data, store_data)

    def get_list(self):
        data = self.store_model.get_summary()
        for i in range(len(data)):
            mas = self.decrypt_data(data[i])
            val = str(mas[1])
            val = ' ' * (3 - len(val)) + val
            data[i] = [f'{val}| {mas[0]} |{mas[2]}|', mas[1]]
        return data

    def convert(self, data, dlist=False):
        if dlist is False:
            convert_data = {}
            for i in range(len(data)):
                convert_data[self.store_model.table_columns[i]] = data[i]
        else:
            convert_data = []
            for key in self.store_model.table_columns_short:
                convert_data.append(data[key])
        return convert_data

    def decrypt_data(self, data):
        # TODO сделать по красоте
        data = list(data)
        for i in range(len(data)):
            try:
                data[i] = self.crypt_controller.decode(data[i])
            except AttributeError:
                data[i] = data[i]
        return data

    def encrypt_data(self, data):
        for i in range(len(data)):
            data[i] = self.crypt_controller.encode(data[i])
        return data


class Synchronization(object):
    def __init__(self):
        self.CREDENTIALS_FILE = sys.path[0] + '/local/' + 'creds.json'
        self.spreadsheet_id = '1hhjCUhlmn6OBt8WdDgKtMxEVbDsZcfRyeOu53qsigSA'
        self.login_range = 'A1:D10'
        self.store_range = 'E1:L1000'
        self.all_range = 'A1:L1000'
        self.service = None

    def authorization(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    def read(self, login_only=True):
        if login_only is True:
            range_read = self.login_range
        else:
            range_read = self.store_range
        data = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range_read,
            majorDimension='ROWS'
        ).execute()
        values = data['values']
        return values

    def write(self, login_data, store_data):
        self.delete()
        request= self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={
                'valueInputOption': 'USER_ENTERED',
                'data': [
                    {
                        'range': self.login_range,
                        'majorDimension': 'ROWS',
                        'values': login_data
                    },
                    {
                        'range': self.store_range,
                         'majorDimension': 'ROWS',
                         'values': store_data
                    }
                ]
            }
        ).execute()

    def delete(self):
        request = self.service.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheet_id,
            range=self.all_range,
            # body=clear_values_request_body
        ).execute()


