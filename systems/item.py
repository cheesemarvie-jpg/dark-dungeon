import pygame
from pygame.locals import *
import random
from entities.wisp import Wisp
from entities.broken_wall import Broken_Wall

class Item:
    def __init__(self, name, description, effect_func):
        self.name = name
        self.description = description
        self.effect_func = effect_func

    def use(self, maze, status):
        self.effect_func(maze, status)

class ItemManager:
    def __init__(self):
        self.item_pool = self.create_item_pool()
        self.se_break = pygame.mixer.Sound("assets/sounds/SE_BREAK.wav")
        self.se_flash = pygame.mixer.Sound("assets/sounds/SE_FLASH.wav")
        self.se_release = pygame.mixer.Sound("assets/sounds/SE_RELEASE.wav")

    def create_item_pool(self):
        return [

            Item(
                "Wall Break",
                "Destroy the wall in front of you.",
                lambda maze, status: self.break_wall(maze)
            ),

            Item(
                "Teleport Flash",
                "Teleport randomly and illuminate the maze.",
                lambda maze, status: self.teleport_flash(maze)
            ),

            Item(
                "Wisp Burst",
                "Release 5 wisps.",
                lambda maze, status: self.spawn_wisps(maze)
            ),
        ]
    def break_wall(self, maze):
        px = maze.player.grid_x
        py = maze.player.grid_y
        dx, dy = maze.player.direct

        tx = px + dx
        ty = py + dy

        # ===== 境界チェック =====
        if tx <= 0 or ty <= 0 or tx >= maze.size - 1 or ty >= maze.size - 1:
            return  # 外周は壊せない
        if maze.map[tx][ty] != 1:            
            return  # 壁でない
        
        maze.map[tx][ty] = 0
        self.se_break.play()
        # 壁スプライト削除
        for wall in maze.tiles:
            if wall.grid_x == tx and wall.grid_y == ty:
                wall.kill()

        # 通路生成
        Broken_Wall(ty, tx, maze.size)

    def teleport_flash(self, maze):
        route_positions = []

        for y in range(maze.size):
            for x in range(maze.size):
                if maze.map[x][y] == 0:
                    route_positions.append((x, y))

        x, y = random.choice(route_positions)

        maze.player.grid_x = x
        maze.player.grid_y = y
        maze.player.rect.center = maze.player.get_tile_center(x, y)

        # 全体フラッシュ
        maze.a_light.set_brightness(1000)
        self.se_flash.play()
   
    def spawn_wisps(self, maze):
        self.se_release.play()
        for _ in range(5):
            maze.wisps.append(Wisp(maze, speed=300, light_power=200))



class ItemUI:
    def __init__(self, status, screen):
        self.status = status
        self.screen = screen

        self.slot_size = 72
        self.x = 60
        self.y = 120

        self.font = pygame.font.SysFont(None, 24)

        # 仮画像（あとで差し替え可能）
        self.images = {
            "Wall Break": pygame.transform.scale(pygame.image.load("assets/images/Break.bmp"), (56, 56)),
            "Teleport Flash": pygame.transform.scale(pygame.image.load("assets/images/Teleport.bmp"), (56, 56)),
            "Wisp Burst": pygame.transform.scale(pygame.image.load("assets/images/Wisp.bmp"), (56, 56)),
        }


    def draw(self):
        # 枠
        rect = pygame.Rect(self.x, self.y, self.slot_size, self.slot_size)

        pygame.draw.rect(self.screen, (180,180,180), rect, 3)

        
        item = self.status.item

        if item is None:
            # 空状態
            text = self.font.render("EMPTY", True, (120,120,120))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        else:
            # アイテム画像
            if item.name in self.images:
                img = self.images[item.name]
                img_rect = img.get_rect(center=rect.center)
                self.screen.blit(img, img_rect)
