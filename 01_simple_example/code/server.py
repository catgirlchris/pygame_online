import socket
from _thread import *
import pickle

from player import Player

server = "192.168.100.59"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binding the socket
try:
    print("Haciendo bind socket con socket")
    s.bind((server,port))
    print("Socket bind completado")
except socket.error as e:
    print("Error al hacer bind socket")
    str(e)

# max connections allowed, this only listen por a little while
s.listen(2)
print("Waiting for a connection, Server Started")



# an element for each player
players = [Player(0,0,50,50,(255,0,0)), Player(100,100,50,50,(0,0,255))]

def threaded_client(conn:socket.socket, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            #print("hilo#"+str(player)+": data recibida:"+str(data))

            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                #print("Recieved: ", data)
                #print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))

        except error as e:
            print(e)
            print(" + hilo de player#"+current_player+" recibió error inesperado y se cerrará.")
            break

    print("Lost connection")
    conn.close()

current_player = 0
# Server listening starting
while True:
    print("Esperando conexión de un cliente...")
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, current_player))
    # players id so the thread knows to what player it's comunicating
    current_player += 1