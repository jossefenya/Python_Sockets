from socket import *
import threading
from cryptography.fernet import Fernet

host = ''
port = 25000

class Server(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.clients_port = []
        self.clients = []
        self.cipher_key = Fernet.generate_key()

    def listenToClient(self, client, addr):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                key = Fernet(self.cipher_key)
                data_for_check = key.decrypt(data).decode('utf8')
                print(data_for_check)
                client_ip, client_port = addr
                if data_for_check:
                    if 'SENDTO' in data_for_check:
                        port_for_resend = int(client.recv(size).decode('utf8'))
                        msg = client.recv(size)
                        print('===================================================================================')
                        print('Message: "{}" for IP: {}, Port: {}, from IP: {}, Port: {}'.format(msg.decode(), client_ip, client_port, client_ip, port_for_resend))
                        for i in self.clients:
                            IP, PORT = i.getpeername()
                            if PORT == port_for_resend:
                                #msg = 'Message: "' + msg + '", From IP:' + client_ip + ' Port:' + str(client_port)
                                i.send(msg)
                        print('===================================================================================')
                    else:
                        print('======================================================')
                        print('From IP: {}, Port: {}\n'.format(client_ip, client_port))
                        print('Message: ', end='')
                        print(data)
                        #data = 'Message: "' + data + '", From IP:' + client_ip + ' Port:' + str(client_port)
                        for i in self.clients:
                            i.send(data)
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
            client.settimeout(200)
            client_ip, client_port = addr
            client.send(bytes((str(client_port)).encode('utf8')))
            client.send(self.cipher_key)
            print('Connected from IP: {}, Port: {}'.format(client_ip, client_port))
            threading.Thread(target=self.listenToClient, args=(client, addr)).start()
            self.clients.append(client)


if __name__ == '__main__':
    while True:
        try:
            port = int(port)
            break
        except ValueError:
            pass
    print('Server started work on {}:{}'.format('127.0.0.1', port))
    Server('', port).listen()
    """
    key = Fernet(Fernet.generate_key())
    print(key)
    msg = input('>')
    secret = key.encrypt(bytes(msg.encode('utf8')))
    print(secret.decode('utf8'))
    """