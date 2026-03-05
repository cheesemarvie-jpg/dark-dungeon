import pygame

class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text, font, color, center):
        super().__init__()
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(center=center)