import socket
from _thread import *
import sys

def threaded_client(conn:socket.socket):
    conn.send(str.encode("Connected"))
    reply = ""

    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Recieved: ", reply)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))

        except e:
            print(e)
            break

    print("Lost connection")
    conn.close()

server = "192.168.100.59"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binding the socket
try :
    s.bind((server,port))
except socket.error as e:
    str(e)

# max connections allowed, this only listen por a little while
s.listen(2)
print("Waiting for a connection, Server Started")

# Server listening starting
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))