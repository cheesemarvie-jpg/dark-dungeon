import pygame
import random

class Skill:
    def __init__(self, name, description, effect_func):
        self.name = name
        self.description = description
        self.effect_func = effect_func  # Statusを受け取って変更する関数

    def apply(self, status):
        self.effect_func(status)

class SkillManager:
    def __init__(self):
        self.skill_pool = self.create_skill_pool()

    def create_skill_pool(self):
        return [
            Skill(
                "速度増加",
                "移動速度が上がる",
                lambda status: setattr(status, "agility", status.agility - 50)
            ),
            Skill(
                "制限時間増加",
                "制限時間が増える",
                lambda status: setattr(status, "timelimit", status.timelimit + 5000)
            ),
            Skill(
                "発光",
                "プレイヤーの周囲を照らす",
                lambda status: setattr(status, "plight_level", status.plight_level + 50)
            ),
            Skill(
                "ゴール発光",
                "ゴールの周囲を照らす",
                lambda status: setattr(status, "glight_level", status.glight_level + 200)
            ),
            Skill(
                "猶予時間増加",
                "開始時の発光時間が増える",
                lambda status: setattr(status, "moratorium", status.moratorium + 200)
            ),
            Skill(
                "精霊使い",
                "光の玉が現れる",
                lambda status: setattr(status, "wisp_count", status.wisp_count + 3)
            ),
            Skill(
                "閃光",
                "時々ステージ全体が照らされる",
                lambda status: setattr(status, "flash_stack", status.flash_stack + 1)
            ),
        ]

    def get_random_skills(self, count=3):
        return random.sample(self.skill_pool, count)

class SkillCardSprite(pygame.sprite.Sprite):
    def __init__(self, center, width, height, selected=False):
        super().__init__()

        self.width = width
        self.height = height
        self.center = center
        self.selected = selected

        self.build()

    def build(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # 背景
        self.image.fill((30, 30, 30))

        # 枠色
        if self.selected:
            border_color = (255, 215, 0)  # 金色
            border_width = 5
        else:
            border_color = (120, 120, 120)
            border_width = 2

        pygame.draw.rect(
            self.image,
            border_color,
            (0, 0, self.width, self.height),
            border_width
        )

        self.rect = self.image.get_rect(center=self.center)

    def set_selected(self, selected):
        self.selected = selected
        self.build()
