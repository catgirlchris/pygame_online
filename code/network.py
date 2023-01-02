import socket

class Network:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.100.59"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def get_pos(self):
        '''Get player position'''
        return self.pos

    
    def connect(self):
        '''Conecta con el socket y recibe player_start_pos'''
        try:
            self.client_socket.connect(self.addr)
            return self.client_socket.recv(2048).decode()
        except:
            #print(e)
            pass

    def send(self, data):
        '''Manda datos y recibe otros de vuelta'''
        try:
            self.client_socket.send(str.encode(data))
            return self.client_socket.recv(2048).decode()
        except socket.error as e:
            print(e)
