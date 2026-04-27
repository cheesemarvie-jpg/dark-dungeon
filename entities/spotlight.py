import pygame
from pygame.locals import *
import config

class SpotLight(pygame.sprite.Sprite):
    def __init__(self, brightness, target, size):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.target = target
        self.size = size
        self.set_brightness(brightness)
        
    def update(self, deltatime):
        self.rect.centerx = self.target.rect.centerx - (config.SCREEN.width - config.SCREEN.height) / 2
        self.rect.centery = self.target.rect.centery

    def set_brightness(self, brightness):#明るさ(半径)を指定する
        radius = int(brightness / self.size) * 10
        self.brightness = int(brightness / self.size) * 10

        #円を作る
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 0, 0), (radius, radius), radius)

        #ふちをぼやかす
        for r in range(radius, 0, -1):
            alpha = int(255 - 255 * (r / radius))
            pygame.draw.circle(self.image, (0, 0, 0, alpha), (radius, radius), r)

        w = self.image.get_width()
        h = self.image.get_height()
        self.rect = Rect(0, 0, w, h)
        self.rect.centerx = self.target.rect.centerx - (config.SCREEN.width - config.SCREEN.height) / 2
        self.rect.centery = self.target.rect.centery
        

    def get_brightness(self):
        return self.brightness