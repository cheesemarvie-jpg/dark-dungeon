from pygame.locals import *
from .base_scene import Scene
from maze.maze import Maze
from scene.skill_select_scene import SkillSelect 
from scene.waiting_scene import Waiting
from systems.status import Status
from scene.pause_scene import Pause

class Game(Scene):
    #初期化
    def __init__(self, parent):
        super().__init__(parent)
        self.status = Status()
        self.scene_tmp = None#ポーズ時に使用中のSceneオブジェクトを退避させる
        self.pausing = False
        self.set_waiting()
    
    def set_waiting(self):
        self.scene = Waiting(self)
    
    def set_maze(self):
        self.status.count_stage()
        self.scene = Maze(self, self.status)

    def set_skillselect(self):
        self.scene = SkillSelect(self, self.status)
    
    def set_pause(self):
        self.scene_tmp = self.scene
        self.pausing = True
        self.scene = Pause(self, self.status)
        
    def restart_scene(self):
        self.pausing = False
        self.scene = self.scene_tmp
        
    #表示の変更
    def print_screen(self, screen):
        screen.fill((30, 30, 30))
        self.scene.print_screen(screen)
        
    #入力の受付
    def input(self, event):
        if event.type == KEYDOWN and event.key == K_TAB and not self.pausing:
            self.set_pause()
        else: 
            self.scene.input(event)
                    
    #オブジェクトの更新
    def output(self, deltatime):
        
        self.scene.output(deltatime)

