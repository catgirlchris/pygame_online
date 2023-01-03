import socket
import pickle

class Network:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.100.59"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_p(self):
        '''Get player'''
        return self.p

    
    def connect(self):
        '''Conecta con el socket y recibe player'''
        try:
            self.client_socket.connect(self.addr)
            return pickle.loads(self.client_socket.recv(2048))
        except:
            #print(e)
            pass

    def send(self, data):
        '''Manda datos y recibe otros de vuelta'''
        try:
            self.client_socket.send(pickle.dumps(data))
            return pickle.loads(self.client_socket.recv(2048))
        except socket.error as e:
            print(e)
