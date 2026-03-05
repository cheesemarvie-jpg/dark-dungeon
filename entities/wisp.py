import pygame
from pygame.locals import *
import config
import random
import math
from entities.spotlight import SpotLight

class Wisp(pygame.sprite.Sprite):
    def __init__(self, maze, speed=250, light_power=100):
        super().__init__(maze.group)

        self.maze = maze
        self.size = maze.size

        self.side = config.SCREEN.height // self.size
        self.radius = int(self.side * 0.25)

        # 透明に近い見た目
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255, 5),
                           (self.radius, self.radius),
                           self.radius)

        self.rect = self.image.get_rect()

        # 初期位置（プレイヤー位置）
        self.rect.center = maze.player.rect.center

        # ランダム方向
        angle = random.uniform(0, math.pi * 2)
        self.velocity = pygame.Vector2(
            math.cos(angle),
            math.sin(angle)
        ) * speed

        # スポットライトを持たせる
        self.light = SpotLight(light_power, self, self.size)
        maze.lights.add(self.light)

    def update(self, dt):
        dt_sec = dt / 1000

        # 移動
        self.rect.x += self.velocity.x * dt_sec
        self.rect.y += self.velocity.y * dt_sec

        # 画面内の迷路表示範囲を取得
        left = (config.SCREEN.width - config.SCREEN.height) / 2
        right = left + config.SCREEN.height
        top = 0
        bottom = config.SCREEN.height

        # 左右反射
        if self.rect.left <= left:
            self.rect.left = left
            self.velocity.x *= -1

        elif self.rect.right >= right:
            self.rect.right = right
            self.velocity.x *= -1

        # 上下反射
        if self.rect.top <= top:
            self.rect.top = top
            self.velocity.y *= -1

        elif self.rect.bottom >= bottom:
            self.rect.bottom = bottom
            self.velocity.y *= -1
