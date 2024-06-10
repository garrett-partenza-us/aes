from aes import AES

if __name__ == '__main__':

    encryptor = AES()

    data = "hello world"

    encryptor.encrypt(data)
