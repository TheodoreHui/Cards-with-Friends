import socket
import threading
import pickle
from card import Card
from deck import Deck
import pygame

# setting up constants for socket
HEADER = 64
PORT = 5555
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# initializing socket/pygame, also creates common deck for all clients
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
connections = {}
display_dim = (800, 600)
game_display = pygame.display.set_mode(display_dim)
d = Deck(game_display)
d.shuffle_deck()


# Main method for client threads
def handle_client(conn, addr):
    # protocol for handling new connection
    print(f"[NEW CONNECTION] {addr} connected.")
    print(connections)
    connected = True

    # Main listening loop for incoming data
    while connected:
        # Decomposes data from pickle object into data length header and string data, string data format "[DATATYPE]:<content>"
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = pickle.loads(conn.recv(msg_length))

            print(f"[{addr}] {msg}")

            # further decomposes data string into string array where index 0 is datatype, index 1 data
            split_msg = msg.split(":")
            print(split_msg)

            # header/code for changing server deck
            if split_msg[0] == "[UPDATE DECK]":
                print("[UPDATE DECK] Updating deck...")
                d.cards = []
                split_msg.pop(0)
                card_data = split_msg[0].split("\n")
                # print(card_data)
                for i in range(len(card_data)-1):
                    data = card_data[i].split()
                    # print(data)
                    value = data[0]
                    suit = data[1]
                    d.cards.append(Card(value, suit, game_display))

            # header/code for retrieving server deck from client (used in client initialization)
            elif split_msg[0] == "[GET DECK]":
                print(f"[GET DECK] sending deck to {addr}...")
                send("[GET DECK]:" + str(d), conn)

            # header/code for updating card positions from client
            elif split_msg[0] == "[UPDATE CARD]":

                # updates server version of card to client
                split_msg.pop(0)
                split_msg = split_msg[0].split()
                for card in d.cards:
                    try:
                        if int(split_msg[0]) == int(card.value) and str(split_msg[1]) == str(card.suit):
                            if card.is_visible:
                                card.rect.move_ip(int(split_msg[2]) - card.rect.x, int(split_msg[3]) - card.rect.y)
                            break
                    except:
                        pass

                # checks all clients, sends update to all clients but original source of update
                for address in connections:
                    if connections[address] is conn:
                        pass
                    else:
                        send(msg, connections[address])
                        print(f"sent {msg} to {address}")
            else:
                # kills thread if client closes gracefully, skips to conn.close
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    connections.pop(addr)
                else:
                    # catches rest of client messages
                    print(msg[0] + " not recognized as header")

    conn.close()
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    print(connections)


def send(msg, conn):
    # takes message string (format "[DATATYPE]<data>") and wraps it in pickle object, then sends to client
    message = pickle.dumps(msg)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def start():

    # start listening for connections
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        # main loop for starting thread, listens for new client connections, starts new handle_client thread for
        conn, addr = server.accept()
        connections[addr] = conn
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        #send("[CONNECTION #]: " + str(threading.activeCount() - 1), conn)


print("[STARTING] server is starting...")
start()
