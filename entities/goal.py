import pygame
from pygame.locals import *
import config

class Goal(pygame.sprite.Sprite):
    def __init__(self, i, j, size):
        pygame.sprite.Sprite.__init__(self, self.containers)
        side = config.SCREEN.height // size#割り切れないと1ピクセル分線が出たりするので商を求める
        rate = 0.7
        tmp_rect =  Rect((config.SCREEN.width - config.SCREEN.height) / 2 + j * side, i * side, side, side)
        self.image = pygame.transform.scale(pygame.image.load("assets/images/Goal.bmp"), (side * rate, side * rate)).convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)

        # 矩形オブジェクトの作成
        self.rect = Rect(0, 0, side * rate, side * rate)
        self.rect.center = tmp_rect.center
