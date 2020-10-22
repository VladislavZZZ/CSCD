import socket
from Crypto.Random import new
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
random_generator = new().read

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('172.16.97.113', 9090))
    key = RSA.generate(1024, random_generator)
    public_key = key.publickey().exportKey(format='PEM', passphrase=None, pkcs=1)
    print(public_key)
    sock.send(public_key)

    data = sock.recv(1024)
    print(data)
    decrypter = PKCS1_OAEP.new(key)
    decrypto = decrypter.decrypt(data)
    messageDecr = AES.new(decrypto, AES.MODE_CFB)
    while True:
        print('HELP\nshow - show file list\nread [filename] - for read text\ncreate [filename] [text] - for create file\n'
              'edit [filename] [text] - rewrite exciting file\nexit - end programm')
        message = input()
        enc_message = messageDecr.encrypt(message.encode('utf-8'))
        sock.send(enc_message)
        enc_message = b''
        while True:
            enc_ans = sock.recv(1024)
            if not enc_ans:
                break
            enc_message += enc_ans

        message = messageDecr.decrypt(enc_message).decode('utf-8')
        print(message)