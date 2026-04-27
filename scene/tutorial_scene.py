import pygame
from pygame.locals import *
from .base_scene import Scene 
import config
from systems.text_sprite import TextSprite

class Tutorial(Scene):
    def __init__(self, parent):
        super().__init__(parent)
        self.group = pygame.sprite.Group()

        title_font = config.title_font
        font = config.font
        self.title = title_font.render("チュートリアル", True, (255, 255, 255))
        self.texts = []
        self.texts.append(font.render("  概要", True, (0, 255, 255)))
        self.texts.append(font.render("・限られた視界、制限時間の中で迷路を記憶し、ゴール(水色の魔法陣)を目", True, (255, 255, 255)))
        self.texts.append(font.render("　指すゲームです。迷路はだんだん難しくなり、１５階層でクリアです。", True, (255, 255, 255)))
        self.texts.append(font.render("・壁に衝突するとスタンし、位置がわかる代わりに制限時間が減ります。", True, (255, 255, 255)))
        self.texts.append(font.render("・階層クリア時の残り時間に応じて経験値を獲得できて、一定以上たまると", True, (255, 255, 255)))
        self.texts.append(font.render("　様々な効果のスキルを獲得できます。", True, (255, 255, 255)))
        self.texts.append(font.render("・宝箱に触れると、攻略に有利なアイテムを入手できます。", True, (255, 255, 255)))
        
        self.texts.append(font.render("  操作方法", True, (0, 255, 255)))
        self.texts.append(font.render("Enter:決定、アイテムの使用　　　　TAB:一時停止", True, (255, 255, 255)))
        self.texts.append(font.render("W/A/S/D:移動　　　　　　　　　　　ESC:ゲームの終了", True, (255, 255, 255)))
        self.texts.append(font.render("", True, (255, 255, 255)))
        self.texts.append(font.render("", True, (255, 255, 255)))
    def print_screen(self, screen):
        screen.fill((0,0,0))
        
        center_x = config.SCREEN.centerx
        center_y = config.SCREEN.centery
        screen.blit(self.title, self.title.get_rect(center = (center_x, 90)))
        
        for i in range(len(self.texts)):
            screen.blit(self.texts[i], (center_x // 3, 150 + 70 * i))
    

    def input(self, event):
        if event.type == KEYDOWN and event.key == K_RETURN:
            self.parent.set_start()