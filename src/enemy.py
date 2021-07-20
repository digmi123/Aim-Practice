import pygame


class Enemy:
    def __init__(self, width, height, pos_x, pos_y):
        self.image = pygame.transform.scale(pygame.image.load("../assets/godfather.png"), (width, height))
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.timer = 0
        self.center = (pos_x + width / 2, pos_y + height / 2)
        self.radius = width / 2
