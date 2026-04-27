import pygame
import sys
from pygame.locals import *
from scene.start_scene import Start
from scene.game_scene import Game
from scene.result_scene import Result
from scene.tutorial_scene import Tutorial
import config

class Main:
    def __init__(self):
        global SCREEN
        # Pygameの初期化
        pygame.init()
        pygame.mixer.init()
        
        info = pygame.display.Info()
        w, h = info.current_w,info.current_h
        
        config.SCREEN = pygame.Rect(0, 0, w, h)
        config.title_font = pygame.font.Font("./assets/font/k8x12.ttf", 100)
        config.font = pygame.font.Font("./assets/font/k8x12.ttf", 50)
        config.skill_font = pygame.font.Font("./assets/font/k8x12.ttf", 30)
        # 画面設定
        self.screen = pygame.display.set_mode((w, h))
        # タイトルバーに表示する文字
        pygame.display.set_caption("Dark Dungeons")
        #場面を管理する変数
        self.scene = False
        self.clock = pygame.time.Clock()
        
        self.set_start()

    def main(self):
        while self.scene:
            deltatime = self.clock.tick(60)
            
            #オブジェクトの更新
            self.scene.output(deltatime)

            self.screen.fill((255, 255, 255))

            #場面を描画
            self.scene.print_screen(self.screen)
        
            # 画面を更新
            pygame.display.update()

            # イベント処理
            for event in pygame.event.get():
                # 閉じるボタンが押されたら終了
                if event.type == QUIT:
                    self.scene = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.scene = False
                else:
                    self.scene.input(event)

        pygame.quit()
        sys.exit()

    def set_start(self):
        self.scene = Start(self)

    def set_game(self):
        self.scene = Game(self)

    def set_result(self, status):
        self.scene = Result(self, status)
        
    def set_tutorial(self):
        self.scene = Tutorial(self)
    def set_false(self):
        self.scene = False
if __name__ == "__main__":
    Main().main()

