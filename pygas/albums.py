import os
from .util import util

class Albums:

    def __init__(self, app):
        self.app = app
        self.view = self.app.view
        self.shown = []
        self.chosen = []
        self.played = None
        self.num = 0

    def show(self, art_dir):
        albs = os.listdir(art_dir)
        names = self.get_names
        self.shown = list(map(lambda dir: os.path.join(art_dir, dir)), albs)
        self.view.set_font('albs', self.get_font([names, None]))
        self.view.add_buttons('albs', names, lambda a,t: self.select(a,t))

    # t_num - last played track
    def select(self, a_num, t_num):
        self.app.artists.selected()
        self.chosen = self.shown
        self.play(a_num, t_num)

    def play(self, a_num, t_num = 0):
        self.view.change_colors('albs', self.num, a_num)
        self.num = a_num
        self.app.set_info_font(self.played)



    def get_names(self):
        return list(map(lambda name: util.cut(name, self.app.NAME_MAX["alb"])))

