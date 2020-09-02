import os
import pygame


class Card:
    def __init__(self, value, suit, game_display):
        self.value = value
        self.suit = suit
        self.face = pygame.image.load(os.path.join("assets", str(self.value) + self.suit + ".png"))
        self.face = pygame.transform.scale(self.face, (150, 250))
        self.back = pygame.image.load(os.path.join("assets", "Gray_back.jpg"))
        self.rect = self.face.get_rect()
        self.moving = False
        self.game_display = game_display
        self.is_visible = False
        self.is_flipped = False
        self.order = 0

    def __str__(self):
        return str(self.value) + " " + str(self.suit) + " " + str(self.rect.x) + " " + str(self.rect.y) + "\n"

    def draw(self):
        if self.is_visible:
            if self.is_flipped:
                self.game_display.blit(self.back, self.rect)
            else:
                self.game_display.blit(self.face, self.rect)

    def update(self, event):
        if self.is_visible:
            if event.type == pygame.MOUSEBUTTONDOWN and self.order == 1:
                if self.rect.collidepoint(event.pos):
                    self.moving = True
                    self.order = 0

            elif event.type == pygame.MOUSEBUTTONUP:
                self.moving = False
                self.order = 1

            elif event.type == pygame.MOUSEMOTION and self.moving:
                self.rect.move_ip(event.rel)
                return str(self)
