import pygame
from pygame.locals import *
import config
import random
from systems.item import ItemManager

class Chest(pygame.sprite.Sprite):
    def __init__(self, i, j, size):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.size = size
        side = config.SCREEN.height // size
        rate = 0.8

        tmp_rect = Rect(
            (config.SCREEN.width - config.SCREEN.height) / 2 + j * side,
            i * side,
            side,
            side
        )
        self.item = random.choice(ItemManager().item_pool)
        # 閉じた宝箱
        self.closed_image = pygame.transform.scale(
            pygame.image.load("assets/images/Chest_closed.bmp"),
            (side * rate, side * rate)
        ).convert()
        self.closed_image.set_colorkey((0, 0, 0), RLEACCEL)

        # 開いた宝箱
        self.open_image = pygame.transform.scale(
            pygame.image.load("assets/images/Chest_open.bmp"),
            (side * rate, side * rate)
        ).convert()
        self.open_image.set_colorkey((0, 0, 0), RLEACCEL)

        self.image = self.closed_image
        self.rect = self.image.get_rect()
        self.rect.center = tmp_rect.center

        self.opened = False

    def open(self):
        if not self.opened:
            self.image = self.open_image
            self.opened = True