import pygame

class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text, font, color, center, blinking = False):
        super().__init__()
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(center=center)
        if blinking:
            self.blinking = True
            self.alpha = 255
            self.up = False
        else:
            self.blinking = False
    def update(self, deltatime):
        if self.blinking:
            if self.up:
                self.alpha += 3
            else:
                self.alpha -= 3
            if self.alpha > 255:
                self.alpha = 255
                self.up = False
            elif self.alpha < 0:
                self.alpha = 0
                self.up = True
            self.image.set_alpha(self.alpha)                
    