from socket import *
import threading

host = ''
port = 7778

class Server(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.clients_port = []
        self.clients = []

    def listenToClient(self, client, addr):
        size = 1024
        while True:
            try:
                data = client.recv(size).decode('utf8')
                client_ip, client_port = addr
                if data:
                    if 'SENDTO' in data:
                        port_for_resend = int(client.recv(size).decode('utf8'))
                        msg = client.recv(size).decode('utf8')
                        print('===================================================================================')
                        print('Message: "{}" for IP: {}, Port: {}, from IP: {}, Port: {}'.format(msg, client_ip, client_port, client_ip, port_for_resend))
                        for i in self.clients:
                            IP, PORT = i.getpeername()
                            if PORT == port_for_resend:
                                msg = 'Message: "' + msg + '", From IP:' + client_ip + ' Port:' + str(client_port)
                                i.send(bytes(msg.encode('utf8')))
                        print('===================================================================================')
                    else:
                        print('======================================================')
                        print('From IP: {}, Port: {}\n'.format(client_ip, client_port))
                        print('Message: ', end='')
                        print(data)
                        data = 'Message: "' + data + '", From IP:' + client_ip + ' Port:' + str(client_port)
                        for i in self.clients:
                            i.send(bytes(data.encode('utf8')))
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