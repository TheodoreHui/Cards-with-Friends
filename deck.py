import random
from card import Card
#Wrapper class for an array of cards, has a shuffle function

class Deck:
    def __init__(self, game_display):
        self.cards = []
        self.game_display = game_display
        for _ in range(1):
            for val in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13):
                for suit in ("H", "S", "C", "D"):
                    self.cards.append(Card(val, suit, self.game_display))

    def shuffle_deck(self):
        random.shuffle(self.cards)
        print("shuffling cards...")

    def __str__(self):
        deck_string = ""
        deck = self.cards
        for card in deck:
            deck_string += str(card)
        return deck_string
