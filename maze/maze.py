import pygame
from pygame.locals import *
from maze.maze_generater import Maze_generater
from entities.wall import Wall
from entities.route import Route 
from entities.broken_wall import Broken_Wall 
from entities.player import Player 
from entities.goal import Goal
from entities.gage import Gage
from entities.chest import Chest
from entities.dark import Dark
from entities.spotlight import SpotLight
from entities.mainlight import MainLight
from entities.wisp import Wisp
from systems.item import ItemUI
import random
from scene.base_scene import Scene
import config
from systems.text_sprite import TextSprite


class Maze(Scene):    
    def __init__(self, parent, status):
        super().__init__(parent)
        self.status = status
        self.size = self.status.get_size()
        self.maze_generater = Maze_generater(self.status)
        self.map = self.maze_generater.get_maze()
        self.px, self.py, self.gx, self.gy, self.cx, self.cy = self.maze_generater.get_coordinates()
        self.group = pygame.sprite.LayeredUpdates()
        self.tiles = pygame.sprite.Group()
        self.lights = pygame.sprite.Group()
        Wall.containers = self.group, self.tiles
        Route.containers = self.group
        Broken_Wall.containers = self.group
        Player.containers = self.group
        Goal.containers = self.group
        Gage.containers = self.group
        Chest.containers = self.group
        Dark.containers = self.group
        SpotLight.containers = self.lights
        MainLight.containers = self.lights
        self.generate_sprites()
        self.finished = False
        self.win_flag = False
        self.once = True#クリア後に画面を明るくするために一度だけupdateをするための変数
        self.se_clear = pygame.mixer.Sound("assets/sounds/SE_CLEAR.wav")
        self.se_flash = pygame.mixer.Sound("assets/sounds/SE_FLASH.wav")
        self.se_open = pygame.mixer.Sound("assets/sounds/SE_OPEN.wav")

        self.item_ui = ItemUI(self.status, self.parent.parent.screen)
        
   
    def generate_sprites(self):#迷路の描画に必要なスプライト群を生成する
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j] == 0:
                    Route(j, i, self.size)
                elif self.map[i][j] == 1:
                    Wall(j, i, self.size)

        
        self.goal = Goal(self.gx, self.gy, self.size)
        self.gage = Gage(self.status)
        self.player = Player(self.px, self.py, self.size, self.tiles, self.status, self.gage)

        self.chest = Chest(self.cx, self.cy, self.size)
        
        self.dark = Dark(self.lights)

        self.p_light = SpotLight(self.status.get_plight_level(), self.player, self.size)
        self.player.set_light(self.p_light)
        self.g_light = SpotLight(self.status.get_glight_level(), self.goal, self.size)
        self.a_light = MainLight(self.status.get_moratorium())

        self.wisps = []
        for i in range(self.status.get_wisp_count()):
            self.wisps.append(Wisp(self, speed=300, light_power=100))

        center_x = config.SCREEN.centerx
        center_y = config.SCREEN.centery

        # スタート案内
        self.guide_text= TextSprite(
                "Press Enter",
                config.font,
                (128,128,128),
                (center_x, center_y),
                blinking = True
            )
        
        for sprite in self.tiles:
            self.group.change_layer(sprite, 0)  # 壁・床

        self.group.change_layer(self.goal, 1)
        self.group.change_layer(self.player, 3)
        self.group.change_layer(self.dark, 4)

        self.group.change_layer(self.chest, 2)

    def print_all(self):#迷路の形を表示(デバッグ用)
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                if i == self.py and j == self.px:
                    print("p", end = "")
                elif i == self.gy and j == self.gx:
                    print("g", end = "")
                elif self.map[i][j] == 0:
                    print(".", end = "")
                elif self.map[i][j] == 1:
                    print("*", end = "")
                else:
                    print(" ", end = "")
            print()
            
    def print_screen(self, screen):#画面描画
        self.group.draw(screen)
        self.item_ui.draw()
    
    def input(self, event):#入力受付(イベントベース)
        if not self.finished:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if self.status.item is not None:
                        self.status.item.use(self, self.status)
                        self.status.item = None
            else:
                self.player.input(event)
        else:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if self.win_flag:
                        if self.status.get_stagecount() <= self.status.get_maxstage():
                            if self.status.new_skill > 0:
                                self.parent.set_skillselect()
                            else:
                                self.parent.set_waiting()
                        else:
                            self.parent.status.count_stage()
                            self.parent.parent.set_result(self.status)
                    else:
                        self.parent.parent.set_result(self.status)
                
    
    def output(self, deltatime):#フレームごとの処理
        if self.player.rect.colliderect(self.goal.rect)  and not self.finished:#ゴールに触れてクリア
            self.finished = True
            self.win_flag = True
        if self.gage.finished:#時間切れで負け
            self.finished = True
            self.win_flag = False
        if self.finished:#終わったとき迷路全体が見えるようにする
            self.a_light.set_brightness(255)
            self.guide_text.update(deltatime)
            if self.once:
                if self.win_flag:
                    self.se_clear.play()
                self.status.set_exp(self.gage.get_exp())
                self.group.add(self.guide_text)
                self.group.update(deltatime)
                self.lights.update(deltatime)
                self.dark.update(deltatime)
                self.once = False
        else:
            rate = 0.002 * self.status.flash_stack#スキルの発生
            if random.random() < rate:
                self.a_light.set_brightness(300)
                self.se_flash.play()
            if not self.chest.opened and self.player.rect.colliderect(self.chest.rect):
                self.chest.open()
                self.se_open.play()
                if self.status.item is None:
                    self.status.item = self.chest.item
            
            self.group.update(deltatime)
            self.lights.update(deltatime)
            self.dark.update(deltatime)
            self.status.count_time(deltatime)