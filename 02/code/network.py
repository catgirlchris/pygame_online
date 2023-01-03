import socket
import pickle

from game import Game

class Network:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.100.59"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_p(self):
        '''Get player_id'''
        return self.p

    
    def connect(self):
        '''Conecta con el socket, recibiendo de vuelta su player_id.'''
        try:
            self.client_socket.connect(self.addr)
            return self.client_socket.recv(2048).decode()
        except:
            #print(e)
            pass

    def send(self, data) -> Game:
        '''Manda string data y recibe object data de vuelta'''
        try:
            self.client_socket.send(str.encode(data))
            return pickle.loads(self.client_socket.recv(2048))
        except socket.error as e:
            print(e)
