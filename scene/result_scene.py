import pygame
from pygame.locals import *
from .base_scene import Scene
import config
from systems.text_sprite import TextSprite

class Result(Scene):

    def __init__(self, parent, status):
        super().__init__(parent)

        self.group = pygame.sprite.Group()

        title_font = config.title_font
        font = config.font

        center_x = config.SCREEN.centerx
        center_y = config.SCREEN.centery

        # タイトル
        self.group.add(
            TextSprite("Game Over!", title_font, (128,128,128),
                       (center_x, center_y - 150))
        )

        # リスタート案内
        self.group.add(
            TextSprite("Press Enter to Restart", font, (128,128,128),
                       (center_x, center_y + 300))
        )

        if status.get_stagecount() > status.get_maxstage() + 1:
            self.win_flag = True
            self.group.add(
                TextSprite("勝利", font, (128,128,128),
                           (center_x, center_y + 50))
            )

            
            # ステージ表示
            self.group.add(
            TextSprite("全ての階層を制覇した", font, (128,128,128),
                       (center_x, center_y + 120))
            )
            
            self.group.add(
                TextSprite(f"クリア時間: {status.time/1000:.2f}s",
                           font, (128,128,128),
                           (center_x, center_y + 200))
            )

        else:
            self.win_flag = False
            self.group.add(
                TextSprite("敗北", font, (128,128,128),
                           (center_x, center_y + 50))
            )
            # ステージ表示
            self.group.add(
            TextSprite(f"{status.get_stagecount() - 1}つの階層を制覇した", font, (128,128,128),
                       (center_x, center_y + 120))
            )


    def print_screen(self, screen):
        if self.win_flag:
            screen.fill((250, 250, 250))
        else:
            screen.fill((0,0,0))
        self.group.draw(screen)

    def input(self, event):
        if event.type == KEYDOWN and event.key == K_RETURN:
            self.parent.set_start()
