import socket
from _thread import *
import pickle

from game import Game

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

# store ip_addresses of connected players
connected = set()
games : dict[int, Game] = {}
id_count : int = 0

def threaded_client(conn:socket.socket, player_id:int, game_id:int):
    global id_count
    conn.send(str.encode(str(player_id)))

    reply = ""
    
    # string data: 3 opciones diferentes: (get, reset, move)
    #   get: server sends back the game
    #   reset: reset the game as the game is done
    #   move: (r, p, s): if player is allowed to make that move, servers sends game back to client
    while True:
        try:
            data = conn.recv(4096).decode()

            #check if the game still exists
            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset_went()
                    elif data != "get":
                        game.play(player_id, data)

                    reply = game
                    # send game status to both players
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break
    
    # close the game and delete it if we got out of the loop
    print("Lost connection")
    try:
        del games[game_id]
        print("Closing Game", game_id)
    except:
        pass
    id_count -= 1
    conn.close()


# Server listening starting
while True:
    print("\nEsperando conexión de un cliente...")
    conn, addr = s.accept()
    print("Connected to:", addr)

    id_count += 1
    player_id : int = 0
    game_id : int = (id_count - 1)//2  # keeps tracks of the game, 10players -> 5 games

    # si hay jugadores impares, crea juego nuevo
    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print("Creating a new game...")
    # si eres par, eres segudno jugador y prepara el juego
    else:
        games[game_id].ready = True
        player_id = 1


    start_new_thread(threaded_client, (conn, player_id, game_id))