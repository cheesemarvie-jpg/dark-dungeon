import pygame
from pygame.locals import *
import config

class Player(pygame.sprite.Sprite):
    def __init__(self, i, j, size, tiles, status, gage):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.size = size
        self.walls = tiles
        self.status = status
        
        self.side = config.SCREEN.height // size
        self.offset_x = (config.SCREEN.width - config.SCREEN.height) / 2

        rate = 0.7
        
        self.original_image = pygame.transform.scale(
            pygame.image.load("assets/images/Player.bmp"),
            (int(self.side * rate), int(self.side * rate))
        ).convert()
        self.original_image.set_colorkey((0, 0, 0), RLEACCEL)

        self.image = self.original_image

        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect()

        #今の座標
        self.grid_x = j
        self.grid_y = i

        #目標の座標
        self.target_x = j
        self.target_y = i

        self.rect.center = self.get_tile_center(j, i)

        self.moving = False
        self.stun_flag = False
        self.move_timer = 0
        self.move_duration = self.status.get_agility() / size * 5

        self.start_pos = pygame.Vector2(self.rect.center)
        self.target_pos = pygame.Vector2(self.rect.center)
        self.direct = config.NEUTRAL

        self.gage = gage
    
        self.se_move = pygame.mixer.Sound("assets/sounds/SE_MOVE.wav")
        self.se_hit = pygame.mixer.Sound("assets/sounds/SE_HIT.wav")
        
    def set_light(self, light):
        self.light = light

    def get_tile_center(self, gx, gy):
        return (
            self.offset_x + gx * self.side + self.side / 2,
            gy * self.side + self.side / 2
        )

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[K_a]:
            self.direct =config.LEFT
            angle = 90    
        elif keys[K_d]:
            self.direct = config.RIGHT
            angle = -90
        elif keys[K_w]:
            self.direct = config.UP
            angle = 0
        elif keys[K_s]:
            self.direct = config.DOWN
            angle = 180
        else:
            return

        self.image = pygame.transform.rotate(self.original_image, angle)

        if not keys[K_RSHIFT]:#シフト押してあったら方向変えるだけ
            self.se_move.play()
            self.target_x = self.grid_x + self.direct[0]
            self.target_y = self.grid_y + self.direct[1]

            self.start_pos = pygame.Vector2(self.rect.center)
            self.target_pos = pygame.Vector2(
                self.get_tile_center(self.target_x, self.target_y)
            )

            self.move_timer = 0
            self.moving = True

    def update(self, dt):
        if self.moving is False:
            self.handle_input()
        else:
            self.move_timer += dt
            if self.stun_flag:
                t = self.move_timer / (self.move_duration * 2)
            else:
                t = self.move_timer / self.move_duration
            if t > 1:
                t = 1
            new_pos = self.start_pos.lerp(self.target_pos, t)
            self.rect.center = new_pos

            # 衝突判定
            if pygame.sprite.spritecollide(self, self.walls, False) and not self.stun_flag:
                self.se_hit.play()
                self.gage.hit_penalty(3000 + self.status.agility * 20)
                self.start_pos = pygame.Vector2(self.rect.center)
                self.target_pos = pygame.Vector2(
                    self.get_tile_center(self.grid_x, self.grid_y)
                )
                self.target_x, self.target_y = self.grid_x, self.grid_y
                self.move_timer = 0
                self.stun_flag = True
                self.light.set_brightness(self.status.get_plight_level() + 100)
                return

            # 到達
            if t >= 1:
                self.grid_x = self.target_x
                self.grid_y = self.target_y
                self.stun_flag = False
                self.light.set_brightness(self.status.get_plight_level())
                self.moving = False

    def input(self, event):
        pass