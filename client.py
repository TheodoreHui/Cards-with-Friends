import pygame
import socket
import threading
import pickle
from card import Card
from deck import Deck

# setting up constants for socket
HEADER = 64
PORT = 5555
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.0.0.142"
ADDR = (SERVER, PORT)

# setting up pygame/deck of cards
display_dim = (800, 600)
game_display = pygame.display.set_mode(display_dim)
d = Deck(game_display)


def send(msg, client):
    # takes message string (format "[DATATYPE]<data>") and wraps it in pickle object, then sends to server
    message = pickle.dumps(msg)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def receive(client):
    # Decomposes received data from pickle object into data length header and string data, string data format "[DATATYPE]:<content>"
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = pickle.loads(client.recv(msg_length))
        print("Received: " + str(msg))

        # further decomposes data string into string array where index 0 is datatype, index 1 data
        split_msg = msg.split(":")
        print(split_msg)

        # header/code for retrieving server deck from client (used in client initialization)
        if split_msg[0] == "[GET DECK]":
            d.cards = []
            print("[GET DECK] Updating deck...")
            split_msg.pop(0)
            card_data = split_msg[0].split("\n")
            # print(card_data)
            for i in range(len(card_data) - 1):
                data = card_data[i].split()
                value = data[0]
                suit = data[1]
                d.cards.append(Card(value, suit, game_display))

        # header/code for updating card positions from client
        elif split_msg[0] == '[UPDATE CARD]':
            # decomposes data string even further into card attributes
            split_msg.pop(0)
            card_data = split_msg[0].split()
            updated_value = int(card_data[0])
            updated_suit = str(card_data[1])
            updated_x = int(card_data[2])
            updated_y = int(card_data[3])
            print(card_data)

            # finds updated card in own deck, updates x,y pos accordingly
            for card in d.cards:
                if updated_value == int(card.value) and updated_suit == str(card.suit):
                    card.rect.move_ip(updated_x - card.rect.x, updated_y - card.rect.y)
                    print(f"moved {card.value} of {card.suit} to {updated_x}, {updated_y}")
        return msg


def quit_client(client):
    # closes pygame, disconnects connection, closes thread listening thread, then quits program
    pygame.quit()
    send(DISCONNECT_MESSAGE, client)
    client.close()
    quit()


def main():
    # initialization code
    clock = pygame.time.Clock()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    send("[GET DECK]:", client)
    receive(client)
    print(str(d))

    # draws 5 cards from deck
    x = 0
    for i in range(5):
        d.cards[i].is_visible = True
        d.cards[i].rect = d.cards[i].rect.move((x, 0))
        x += 150
        d.cards[i].draw()

    def listen():
        while run:
            print("listening...")
            receive(client)

    run = True
    thread = threading.Thread(target=listen, args=())
    thread.start()

    print("displaying window...")
    # main game loop
    while run:
        # redraws all cards @60 fps
        game_display.fill((255, 255, 255))
        for c in d.cards:
            c.draw()

        # checks for card pos updates, sends to server if applicable
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit_client(client)
            for card in d.cards:
                update = card.update(event)
                if update:
                    send("[UPDATE CARD]:" + str(card), client)
                    print(f"sent update of {card}")

        clock.tick(60)
        pygame.display.update()


if __name__ == "__main__":
    main()
