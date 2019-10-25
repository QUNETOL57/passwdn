from cryptography.fernet import Fernet


class CryptController(object):
    def __init__(self):
        self.step = 13
        self.alpha = "".join(map(chr, range(ord(' '), ord('я') + 1)))
        self.key = self.get_key()
        self.cipher = Fernet(self.key)

    def gen_key(self):
        cipher_key = Fernet.generate_key()
        file_handler = open('../local/cipher.key', 'w')
        file_handler.write(str(cipher_key)[2:-1])
        file_handler.close()

    def get_key(self):
        file_handler = open('../local/cipher.key', 'r')
        return bytes(file_handler.read(), encoding='utf-8')

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



# c = CryptController().gen_key()
# cript = c.encode('serpent26rus@gmail.com')
# print(cript, c.decode(cript))
