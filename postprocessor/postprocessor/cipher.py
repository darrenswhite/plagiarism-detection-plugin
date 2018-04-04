from base64 import b64decode

from Crypto.Cipher import AES


class AESCipher:
    """
    The class decrypts AES encrypted data using a key

    Based on: https://gist.github.com/forkd/7ed4a8392fe7b69307155ab379846019
    """

    def __init__(self, key):
        """
        Create a new AESCipher with the given key
        :param key:
        """
        self.key = key

    def decrypt(self, enc):
        """
        Decrypt the encrypted base64 encoded data
        :param enc: The encrypted data
        :return: The decrypted data
        """
        # Decode base 64
        enc = b64decode(enc)
        # Java uses ECB
        cipher = AES.new(self.key, AES.MODE_ECB)
        return self.__unpad(cipher.decrypt(enc)).decode('utf8')

    @staticmethod
    def __unpad(s):
        return s[:-ord(s[len(s) - 1:])]
