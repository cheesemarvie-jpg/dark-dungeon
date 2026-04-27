import pygame
from pygame.locals import *
from .base_scene import Scene 
import config
from systems.text_sprite import TextSprite

class Waiting(Scene):
    def __init__(self, parent):
        super().__init__(parent)
        self.group = pygame.sprite.Group()

        title_font =config.title_font
        font = config.font

        center_x = config.SCREEN.centerx
        center_y = config.SCREEN.centery

        self.group.add(
            TextSprite(
                "Ｒｅａｄｙ？",
                title_font,
                (128,128,128),
                (center_x, center_y - 120)
            )
        )
        
        self.group.add(
            TextSprite(
                "Press Enter",
                font,
                (128,128,128),
                (center_x, center_y + 300),
                blinking = True
            )
        )
    def print_screen(self, screen):
        screen.fill((0,0,0))
        self.group.draw(screen)

    def input(self, event):
        if event.type == KEYDOWN and event.key == K_RETURN:
            self.parent.set_maze()
            
    def output(self, deltatime):
        self.group.update(deltatime)

