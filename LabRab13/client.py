from socket import *
from RSA import rsa

host = '192.168.1.154'
port = 9000
buff_size = 1024

addr = (host, port)

class Client(object):

    def __init__(self, host, port):
        self.client_sock = (host, port)


    def connect(self):
        self.client_sock = socket(AF_INET, SOCK_STREAM)

        self.client_sock.connect(addr)

        e = int((self.client_sock.recv(buff_size)).decode('utf8'))
        n = int((self.client_sock.recv(buff_size)).decode('utf8'))
        public = e, n
        while True:

            data = input('>')
            msg = data

            if not data:
                break

            data = rsa.encrypt(public, data)
            self.client_sock.send(str(data).encode('utf8'))
            self.client_sock.send(str(msg).encode('utf8'))

        self.client_sock.close()

Client(host, port).connect()