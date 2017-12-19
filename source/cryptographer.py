from PyQt5.QtCore import QByteArray

from source.message import Message, Mode


class Cryptographer:
    def __init__(self, encoding, key):
        self.encoding = encoding
        self.key = key

    def encrypt(self, bytes, key):
        byte_key = bytearray(key, encoding=self.encoding)
        encrypted = bytearray(len(bytes))
        for i in range(len(bytes)):
            byte = byte_key[i % len(byte_key)]
            b = bytes[i]
            encrypted[i] = byte ^ bytes[i]
        return encrypted

    def decrypt(self, bytes, key):
        return self.encrypt(bytes, key)

    # def try_decrypt(self, bytes):
    #     decrypted = self.decrypt(bytes)
    #     text = decrypted.decode(encoding=self.encoding)
    #     if self.is_decrypted(text):
    #         return True, text
    #     return False, None

    # def is_decrypted(self, text):
    #     return text[:len(self.key)] == self.key


# if __name__ == '__main__':
#     c = Cryptographer('utf-8', 'desktop')
#     m = Message('192.168.1.33', 'desktop: some text', Mode.Normal)
#     b = Message.to_bytes(m)
#     e = c.encrypt(b)
#     try:
#         new_m = Message.from_bytes(e)
#     except Exception:
#         new_m = Message.from_bytes(c.decrypt(e))
#     except Exception:
#         print('kek')
#         exit(1)
#     print(new_m.content)