import pygame
from pygame.locals import *
import config
class Broken_Wall(pygame.sprite.Sprite):
    def __init__(self, i, j, size):
        pygame.sprite.Sprite.__init__(self, self.containers)
        side = config.SCREEN.height // size#割り切れないと1ピクセル分線が出たりするので商を求める
        self.image = pygame.transform.scale(pygame.image.load("assets/images/Broken_Wall.bmp"), (side, side)).convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)

        # 矩形オブジェクトの作成
        self.rect = Rect((config.SCREEN.width - config.SCREEN.height) / 2 + j * side, i * side, side, side)
