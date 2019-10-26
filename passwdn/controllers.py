from cryptography.fernet import Fernet
import os.path

from models import LoginModel, StoreModel


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

    def __init__(self):
        self.crypt_controller = CryptController()
        self.login_model = LoginModel()

    def login_in(self, login, password):
        log = self.login_model.select_all()
        for i in range(len(log)):
            for j in range(1, len(log[i]), 3):
                if self.crypt_controller.decode(log[i][j]) == login:
                    if self.crypt_controller.decode(log[i][j+1]) == password:
                        print(login, password)

    # TODO сделать создание пользователя
    def create_prof(self, login, password):
        data = [self.crypt_controller.encode(login), self.crypt_controller.encode(password)]
        self.login_model.add(data)
        print(self.crypt_controller.decode(data[0]), self.crypt_controller.decode(data[1]))

    def decrypt_data(self, data):
        if type(data) is list:
            dec_data = []
            for value in data:
                dec_data += self.crypt_controller.decode(value)
        else:
            dec_data = self.crypt_controller.decode(data)
        return dec_data


# TODO убрать
m = MainAction().login_in('admin','123')
# m = MainAction().create_prof('admin','123')