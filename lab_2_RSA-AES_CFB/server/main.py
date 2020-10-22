import socket
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

import os

path = r'C:\Users\Kizenkov_V\PycharmProjects\CSCD\lab_2_RSA-AES_CFB\server\data/'


def get_text(filename):
    text = ''
    with open(path + filename, 'r')as f:
        line = f.readline()
        while line:
            text += line
    return text


def get_file_list():
    list = ''
    tree = os.walk(path)
    for address, dirs, files in tree:
        for file in files:
            list += file + '\n'
    return list[:-1]


def create_and_fill_file(filename, text):
    with open(path + filename, 'w+')as f:
        f.write(text)
    return 'file {f} successfully created!'.format(f=filename)


def rewrite_file(filename, text):
    with open(path + filename, 'w')as f:
        f.write(text)
    return 'file {f} successfully edited!'.format(f=filename)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("172.16.97.113", 9090))
    sock.listen(1)
    conn, addr = sock.accept()

    print('connected', addr)

    public = conn.recv(1024)
    print(public)
    public = RSA.importKey(public, passphrase=None)
    session_key = get_random_bytes(16)
    print(session_key)
    cipher_rsa = PKCS1_OAEP.new(public)
    ecrypted = cipher_rsa.encrypt(session_key)
    print(ecrypted)
    conn.send(ecrypted)
    AES_cipher = AES.new(session_key, AES.MODE_CFB)
    enc_message = b''
    while True:

        enc_bytes = conn.recv(1024)
        if not enc_bytes:
            break
        enc_message += enc_bytes
        message = AES_cipher.decrypt(enc_message).decode('utf-8')
        params = message.split(' ')
        command = params[0]
        if command == 'show':
            message = get_file_list()
        elif command == 'read':
            message = get_text(params[1])
        elif command == 'create':
            message = create_and_fill_file(params[1], params[2])
        elif command == 'edit':
            message = rewrite_file(params[1], params[2])
        else:
            message = 'not correct'
        enc_message = AES_cipher.encrypt(bytes(message))
        conn.send(enc_message)
        conn.send(b'')
