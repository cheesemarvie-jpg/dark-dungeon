import pygame
from pygame.locals import *
import config

class Dark(pygame.sprite.Sprite):
    def __init__(self, lights):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.size = config.SCREEN.height
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = Rect((config.SCREEN.width - config.SCREEN.height) / 2, 0, config.SCREEN.height, config.SCREEN.height)
        self.lights = lights
        
    def update(self, deltatime):
        self.image.fill((0, 0, 0, 250))
        for light in self.lights:
            self.image.blit(light.image, light.rect, special_flags=pygame.BLEND_RGBA_SUB)
