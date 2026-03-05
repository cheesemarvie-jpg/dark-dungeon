class Scene:
    #初期化
    def __init__(self, parent):
        self.parent = parent
    #表示の変更
    def print_screen(self):
        pass
    #入力の受付
    def input(self, event):
        pass
    #オブジェクトの更新
    def output(self, deltatime):
        pass
