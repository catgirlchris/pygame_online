import socket
from _thread import *
import string
import typing
import sys

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup:typing.Tuple):
    return str(tup[0]) + "," + str(tup[1])


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
players_start_pos = [(0,0), (100,100)]
players_pos = players_start_pos

def threaded_client(conn:socket.socket, player):
    conn.send(str.encode(make_pos(players_start_pos[player])))
    reply = ""

    while True:
        try:
            data = conn.recv(2048).decode()
            print("hilo#"+str(player)+": data recibida:"+str(data))
            data = read_pos(data)

            players_pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players_pos[0]
                else:
                    reply = players_pos[1]

                print("Recieved: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))

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