from socket import *
from RSA import rsa
import threading
import time

public, private = rsa.generateKeys()
e, n = public
d, n = private

host = ''
port = 40001
class Server(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((host, port))

    def listenToClient(self, client, addr):
        size = 1024
        while True:
            try:
                time.sleep(5)
                data = client.recv(size).decode('utf8')
                client_ip, client_port = addr
                if data:
                    msg = client.recv(size)
                    print('======================================================')
                    print('From IP: {}, Port: {}\n'.format(client_ip, client_port))
                    print('Secret message: ', end='')
                    for char in data:
                        if char != ']' and char != ',' and char != '[' and char != ' ':
                            print(char, end='')
                    print('\n\nMessage: ', end='')
                    print(msg.decode('utf8'))
                    print('======================================================\n')
                else:
                    raise error('Client disconnected')
            except:
                print('Disconnected form IP: {}, Port: {}'.format(client_ip, client_port))
                client.close()
                return False

    def listen(self):
        self.sock.listen(10)
        self.size = 1024
        while True:
            client, addr = self.sock.accept()
            client.settimeout(60)
            e_for_client = str(e)
            n_for_client = str(n)
            client_ip, client_port = addr
            print('Connected from IP: {}, Port: {}'.format(client_ip, client_port))
            client.send(bytes(e_for_client.encode('utf8')))
            client.send(bytes(n_for_client.encode('utf8')))
            threading.Thread(target=self.listenToClient, args=(client, addr)).start()

if __name__ == '__main__':
    while True:
        try:
            port = int(port)
            break
        except ValueError:
            pass
    Server('', port).listen()
