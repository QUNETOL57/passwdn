from cryptography.fernet import Fernet
import os.path


class CryptController(object):
    def __init__(self):
        self.step = 13
        # TODO переместить в local
        self.file = 'cipher.key'
        self.alpha = "".join(map(chr, range(ord(' '), ord('я') + 1)))
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
        self.login_model = login_model
        self.store_model = store_model
        self.prof_init = None

    def login_in(self, login, password):
        # TODO сделать инициализацию после идентификации
        log = self.login_model.select_all()
        for i in range(len(log)):
            for j in range(1, len(log[i]), 3):
                if self.crypt_controller.decode(log[i][j]) == login:
                    if self.crypt_controller.decode(log[i][j+1]) == password:
                        return True

    # TODO сделать создание пользователя
    def create_prof(self, login, password):
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