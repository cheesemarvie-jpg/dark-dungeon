class Status:#ゲーム中強化されていくステータスを保持する
    def __init__(self):
        self.level = 1
        self.stage_count = 0
        self.time = 0
        self.skills = []
        self.item = None
        
        self.moratorium = 0
        self.plight_level = 0
        self.glight_level = 0
        self.timelimit = 0
        self.agility = 0
        self.wisp_count = 0
        self.flash_stack = 0
        self.new_skill = False#新たなスキルを取得可能か判定
        
    def count_stage(self):
        self.stage_count += 1
        if self.stage_count // 3 + 1 > self.level:
            self.level = self.stage_count // 3 + 1
            self.new_skill = True
    def get_stagecount(self):
        return self.stage_count

    def level_up(self):
        self.level += 1

    def count_time(self, deltatime):
        self.time += deltatime

    def apply_skill(self, skill):
        skill.apply(self)
        self.skills.append(skill.name)

    def get_level(self):
        return self.level

    def get_size(self):
        return (self.level + 2) * 2 + 1

    def get_moratorium(self):
        return 100 + 100 * self.level + self.moratorium

    def get_plight_level(self):
        return self.plight_level

    def get_glight_level(self):
        return self.glight_level

    def get_timelimit(self):
        return 8000 + (self.level) * 3000 + self.timelimit

    def get_agility(self):
        return 400 + self.agility

    def get_wisp_count(self):
        return self.wisp_count