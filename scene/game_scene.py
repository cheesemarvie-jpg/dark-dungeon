import pygame
from pygame.locals import *
import math
import random
from .base_scene import Scene
from maze.maze import Maze
from scene.skill_select_scene import SkillSelect 
from systems.status import Status


class Game(Scene):
    #初期化
    def __init__(self, parent):
        super().__init__(parent)
        self.font = pygame.font.Font(None, 50)
        self.status = Status()
        self.set_maze()
        
    def set_maze(self):
        self.status.count_stage()
        self.scene = Maze(self, self.status)

    def set_skillselect(self):
        self.scene = SkillSelect(self, self.status)
    
    #表示の変更
    def print_screen(self, screen):
        screen.fill((30, 30, 30))
        self.scene.print_screen(screen)
        
    #入力の受付
    def input(self, event):
        self.scene.input(event)
                    
    #オブジェクトの更新
    def output(self, deltatime):
        self.status.count_time(deltatime)
        self.scene.output(deltatime)

