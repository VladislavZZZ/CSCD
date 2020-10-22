import base64

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class AESCipher:
    def __init__(self, key):
        self.key = key
        self.iv = key

    def encrypt(self, raw):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(self.__pad(raw).encode())).decode()

    def decrypt(self, enc):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self.__unpad(cipher.decrypt(base64.b64decode(enc)).decode())

    def __pad(self, text):
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def __unpad(self, text):
        pad = ord(text[-1])
        return text[:-pad]


if __name__ == '__main__':
    cipher = AESCipher(get_random_bytes(16))
    text = "hello server!"
    encrypt = cipher.encrypt(text)
    print('加密后:\n%s' % encrypt)
    decrypt = cipher.decrypt(encrypt)
    print('解密后:\n%s' % decrypt)