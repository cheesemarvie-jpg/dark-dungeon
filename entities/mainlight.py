import pygame
from pygame.locals import *
import config

class MainLight(pygame.sprite.Sprite):
    def __init__(self, moratorium):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.brightness = moratorium#明るさが大きければ暗くなるまでの時間が長くなる→猶予時間が伸びる
        self.image = pygame.Surface((config.SCREEN.height, config.SCREEN.height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 255))

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def set_brightness(self, brightness):
        self.brightness += brightness
    
    def update(self, deltatime):
        if self.brightness > 10:
            self.brightness -= 10
        elif self.brightness < 10:
            self.brightness = 0
        if self.brightness > 255:
            brightness = 255
        else:
            brightness = self.brightness
        self.image.fill((0, 0, 0, brightness))