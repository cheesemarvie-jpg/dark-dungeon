import pygame
from pygame.locals import *
from .base_scene import Scene
import config
from systems.text_sprite import TextSprite


class Start(Scene):

    def __init__(self, parent):
        super().__init__(parent)
        self.cursor = pygame.sprite.Group()
        self.selected_index = 0
        self.se_move = pygame.mixer.Sound("assets/sounds/SE_SELECT.wav")
        self.se_select = pygame.mixer.Sound("assets/sounds/SE_PICK.wav")
        self.group = pygame.sprite.Group()
        
        title_font = config.title_font
        font = config.font

        center_x = config.SCREEN.centerx
        center_y = config.SCREEN.centery

        # タイトル
        self.group.add(
            TextSprite(
                "Ｄａｒｋ　Ｄｕｎｇｅｏｎ",
                title_font,
                (128,128,128),
                (center_x, center_y - 120)
            )
        )

        # スタート案内
        
        texts = [
            "始める",
            "チュートリアル",
            "終了"
            ]
        j = 0
        for i in texts:
            self.group.add(
                TextSprite(
                    i,
                    font,
                    (128, 128, 128),
                    (center_x, center_y + 80 + 80 * j) 
                )
            )
            j += 1
            
        self.update_cursor()
        
    def print_screen(self, screen):
        screen.fill((0,0,0))
        self.group.draw(screen)
        self.cursor.draw(screen)
    def update_cursor(self):
        self.cursor.empty()
        self.cursor.add(
            TextSprite(
                "●",
                config.font,
                (128,128,128),
                (config.SCREEN.centerx - 160, config.SCREEN.centery + 80 + 80 * self.selected_index)
            )
        )

    def input(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                self.se_select.play()
                if self.selected_index == 0:
                    self.parent.set_game()
                elif self.selected_index == 1:
                    self.parent.set_tutorial()   
                elif self.selected_index == 2:
                    self.parent.set_false()
            elif event.key == K_w:
                self.selected_index = (self.selected_index - 1) % 3
                self.se_move.play()
                self.update_cursor()
            elif event.key == K_s:
                self.selected_index = (self.selected_index + 1) % 3
                self.se_move.play()
                self.update_cursor()

