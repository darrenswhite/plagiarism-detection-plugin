from base64 import b64decode

from Crypto.Cipher import AES


class AESCipher:
    def __init__(self, key):
        self.key = key

    def decrypt(self, enc):
        enc = b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return self.__unpad(cipher.decrypt(enc)).decode('utf8')

    @staticmethod
    def __unpad(s):
        return s[:-ord(s[len(s) - 1:])]
