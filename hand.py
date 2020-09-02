from deck import Deck
from card import Card

class Hand:

    def __init__(self, size, deck):
        self.hand = []
        self.game_display = deck.game_display
        for _ in range(size):
            self.hand.append(deck.cards[0])
            deck.cards.pop(0)
        x = 0
        for card in self.hand:
            card.rect = card.rect.move(x, card.rect.y)
            card.draw()
            x += 150

    def __str__(self):
        hand_string = ""
        for card in self.hand:
            hand_string += str(card)
        return hand_string

    def draw(self):
        for card in self.hand:
            card.draw()