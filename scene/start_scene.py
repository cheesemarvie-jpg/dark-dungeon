import pygame
from pygame.locals import *
from .base_scene import Scene
import config
class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text, font, color, center):
        super().__init__()
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(center=center)


class Start(Scene):

    def __init__(self, parent):
        super().__init__(parent)

        self.group = pygame.sprite.Group()

        title_font = pygame.font.Font(None, 100)
        font = pygame.font.Font(None, 50)

        center_x = config.SCREEN.centerx
        center_y = config.SCREEN.centery

        # タイトル
        self.group.add(
            TextSprite(
                "Dark Dungeon",
                title_font,
                (128,128,128),
                (center_x, center_y - 120)
            )
        )

        # スタート案内
        self.group.add(
            TextSprite(
                "Press Enter to Start",
                font,
                (128,128,128),
                (center_x, center_y + 80)
            )
        )

    def print_screen(self, screen):
        screen.fill((0,0,0))
        self.group.draw(screen)

    def input(self, event):
        if event.type == KEYDOWN and event.key == K_RETURN:
            self.parent.set_game()
