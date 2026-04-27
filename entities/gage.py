import pygame
from pygame.locals import *
import config

class Gage(pygame.sprite.Sprite):

    def __init__(self, status):
        super().__init__(self.containers)

        self.width = 50
        self.max_height = config.SCREEN.height - 100

        # ベースサーフェス
        self.image = pygame.Surface((self.width, self.max_height), pygame.SRCALPHA)
        
        self.rect = self.image.get_rect()
        self.rect.center = (config.SCREEN.width - 100, config.SCREEN.centery)
        
        self.time_limit = status.get_timelimit()
        self.count = 0
        self.finished = False

    def hit_penalty(self, n):
        self.update(n)
        
    def get_exp(self):
        return self.time_limit - 0.7 * self.count

    def update(self, dt):
        self.count += dt

        if self.count >= self.time_limit:
            self.finished = True
            return

        ratio = 1 - (self.count / self.time_limit)
        current_height = int(self.max_height * ratio)

        # クリア
        self.image.fill((0, 0, 0, 0))

        # ゲージ描画（下から伸びる）
        pygame.draw.rect(
            self.image,
            (0, 255, 0),  # 緑ゲージ
            (0, self.max_height - current_height,
             self.width, current_height)
        )
        pygame.draw.rect(self.image, (255, 255, 255), self.image.get_rect(), 2)
