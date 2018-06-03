from socket import *
import threading
import sys

host = '192.168.1.154'
port = 7778
buff_size = 1024

addr = (host, port)

class Client(object):

    def __init__(self, host, port):
        self.client_sock = (host, port)

    def listenToServer(self):
        while True:
            data = self.client_sock.recv(buff_size).decode('utf8')
            print(data)

    def connect(self):
        self.client_sock = socket(AF_INET, SOCK_STREAM)
        self.client_sock.connect(addr)
        print('You connected to server, which hosted on IP: {}, Port: {}'.format(host, port))
        my_port = self.client_sock.recv(buff_size).decode('utf8')
        print('Your Port: {}'.format(my_port))
        threading.Thread(target=self.listenToServer).start()

        while True:


            data = input()

            if 'SENDTO' in data:
                self.client_sock.send(data.encode('utf8'))
                port_for_send = input('Port: ')
                msg = input('Message: ')
                self.client_sock.send(str(port_for_send).encode('utf8'))
                self.client_sock.send(str(msg).encode('utf8'))
            else:
                if not data:
                    break

                self.client_sock.send(str(data).encode('utf8'))

        self.client_sock.close()

Client(host, port).connect()