import pygame
from pygame.locals import *
from .base_scene import Scene
import config
from systems.text_sprite import TextSprite

class Pause(Scene):
    def __init__(self, parent, status):
        super().__init__(parent)
        self.status = status
        self.group = pygame.sprite.Group()
        self.se_move = pygame.mixer.Sound("assets/sounds/SE_SELECT.wav")
        self.se_select = pygame.mixer.Sound("assets/sounds/SE_PICK.wav")
        self.font_title = config.title_font
        self.font = config.font
        self.description_font = config.skill_font

        self.cursor = pygame.sprite.Group()

        self.selected_index = 0
        self.se_select.play()
        self.build_ui()

    def build_ui(self):
        center_x = config.SCREEN.centerx
        self.group.add(
            TextSprite(
                "ＰＡＵＳＥ",
                self.font_title,
                (255, 255, 255),
                (center_x, 120)
            )
        )
        self.group.add(
            TextSprite(
                "再開",
                self.font,
                (255, 255, 255),
                (center_x - 100, 250)
            )
        )
        self.group.add(
            TextSprite(
                "中断",
                self.font,
                (255, 255, 255),
                (center_x + 100, 250)
            )
        )
        
        self.update_cursor()
        
        width = (config.SCREEN.width - 50 * 4 ) / 3
        height = config.SCREEN.height - 400
        infomation_frame = FrameSprite(
            50 + (width + 50) * 0, 350, width, height
        )
        item_frame = FrameSprite(
            50 + (width + 50) * 1, 350, width, height
        ) 
        skill_frame = FrameSprite(
            50 + (width + 50) * 2, 350, width, height
        )
        
        
        self.group.add(infomation_frame)
        self.group.add(item_frame)
        self.group.add(skill_frame)
        
        infomation_texts = [
            "情報",
            f"経過時間:{self.status.time/1000:.2f}s",
            f"階層: {self.status.get_stagecount() - 1} / {self.status.get_maxstage()}",
            f"経験値: {self.status.exp / self.status.get_exp_require() * 100:.1f} %"    
        ]
        j = 0
        for i in infomation_texts:
            self.group.add(
                TextSprite(
                    i,
                    self.font,
                    (255, 255, 255),
                    (infomation_frame.rect.centerx, infomation_frame.rect.centery - 200 + 100 * j) 
                )
            )
            j += 1
        if self.status.item is None:
            item_texts = ["所持アイテム", "無し"]
        else:
            item_texts = ["所持アイテム", f"{self.status.item.name}",self.status.item.description]
        j = 0
        for i in item_texts:
            self.group.add(
                TextSprite(
                    i,
                    self.font,
                    (255, 255, 255),
                    (item_frame.rect.centerx, item_frame.rect.centery - 200 + 100 * j) 
                )
            )
            j += 1
        skill_texts = ["所持スキル", ""]
        skill_list = ["速度増加", "制限時間増加", "発光", "ゴール発光", "猶予時間増加", "閃光", "精霊使い"]
        skill_counts = [0, 0, 0, 0, 0, 0, 0]
        for i in self.status.skills:
            
            for j in range(len(skill_list)):
                if i == skill_list[j]:
                    skill_counts[j]+= 1
        for i in range(len(skill_counts)):
            if skill_counts[i] > 1:
                skill_texts.append(f"{skill_list[i]} × {skill_counts[i]}")
            elif skill_counts[i] > 0:
                    skill_texts.append(f"{skill_list[i]}")
        j = 0
        for i in skill_texts:
            self.group.add(
                     TextSprite(
                         i,
                         self.font,
                         (255, 255, 255),
                         (skill_frame.rect.centerx , skill_frame.rect.centery - 200 + 50 * j) 
                         )
                     )
            j += 1
    def update_cursor(self):
        self.cursor.empty()
        self.cursor.add(
            TextSprite(
                "●",
                self.font,
                (255, 255, 255),
                (config.SCREEN.centerx - 160 + 200 * self.selected_index, 250)
            )
        )

    def print_screen(self, screen):
        screen.fill((0, 0, 0))
        self.group.draw(screen)
        self.cursor.draw(screen)
        
        

   
    def input(self, event):
        if event.type == KEYDOWN:
            if event.key == K_a:
                self.selected_index = (self.selected_index - 1) % 2
                self.se_move.play()
                self.update_cursor()

            elif event.key == K_d:
                self.selected_index = (self.selected_index + 1) % 2
                self.se_move.play()
                self.update_cursor()

            elif event.key == K_RETURN:
                self.se_select.play()
                
                if self.selected_index == 0:
                    self.parent.restart_scene()
                elif self.selected_index == 1:
                    self.parent.parent.set_start()
            elif event.key == K_TAB:
                self.se_select.play()
                self.parent.restart_scene()
    def output(self, dt):
        pass


class FrameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        pygame.draw.rect(
            self.image,
            (255, 255, 255),
            (0, 0, width, height),
            3
        )
        