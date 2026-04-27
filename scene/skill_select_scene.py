import pygame
from pygame.locals import *
from .base_scene import Scene
import config
from systems.text_sprite import TextSprite
from systems.skill import SkillManager, SkillCardSprite

class SkillSelect(Scene):
    def __init__(self, parent, status):
        super().__init__(parent)
        self.status = status
        self.status.new_skill -= 1        
        self.se_move = pygame.mixer.Sound("assets/sounds/SE_SELECT.wav")
        self.se_select = pygame.mixer.Sound("assets/sounds/SE_PICK.wav")
        self.group = pygame.sprite.Group()
        self.font_title = config.title_font
        self.font = config.font
        self.description_font = config.skill_font
        self.manager = SkillManager()
        self.choices = self.manager.get_random_skills(3)

        self.selected_index = 0

        self.build_ui()

    def build_ui(self):
        self.group.empty()
        
        center_x = config.SCREEN.centerx
        self.group.add(
            TextSprite(
                "スキル獲得",
                self.font_title,
                (255, 255, 255),
                (center_x, 120)
            )
        )

        self.cards = []

        for i, skill in enumerate(self.choices):

            card_center = (center_x, 300 + i * 150)

            selected = (i == self.selected_index)

            card = SkillCardSprite(card_center, 500, 120, selected)
            self.group.add(card)
            self.cards.append(card)

            # スキル名
            self.group.add(
                TextSprite(
                    skill.name,
                    self.font,
                    (255, 255, 255),
                    (card_center[0], card_center[1] - 20)
                )
            )

            # 説明
            self.group.add(
                TextSprite(
                    skill.description,
                    self.description_font,
                    (180, 180, 180),
                    (card_center[0], card_center[1] + 20)
                )
            )

    def print_screen(self, screen):
        screen.fill((0, 0, 0))
        self.group.draw(screen)

   
    def input(self, event):
        if event.type == KEYDOWN:
            if event.key == K_w:
                self.selected_index = (self.selected_index - 1) % 3
                self.se_move.play()
                self.build_ui()

            elif event.key == K_s:
                self.selected_index = (self.selected_index + 1) % 3
                self.se_move.play()
                self.build_ui()

            elif event.key == K_RETURN:
                self.se_select.play()

                chosen = self.choices[self.selected_index]
                self.status.apply_skill(chosen)
                
                if self.status.new_skill > 0:
                    self.parent.set_skillselect()
                else:
                    self.parent.set_waiting()
    def output(self, dt):
        pass
