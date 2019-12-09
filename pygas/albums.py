import os
import re
from . import util
from .view import View


class Albums:
    def __init__(self):
        self.shown = []
        self.chosen = []
        self.dirs = []
        self.dir = None
        self.played = None
        self.num = 0

    def show(self, art_dir, shown_tracks, new=True):
        albs = sorted(os.listdir(art_dir), key=lambda d: self.convert(d))
        self.shown = self.get_names(albs)
        self.chosen = [os.path.join(art_dir, a) for a in albs]
        played = None if new else self.num
        View.panel.select_font(self.shown + shown_tracks)
        View.panel.add_buttons('albs', self.shown, self.clicked, played)
        View.switch_to('player')
        if new and len(self.shown) == 1:
            self.select(0)

    def clicked(self, _, a_num):
        self.select(a_num)

    def select(self, a_num, t_num=0):
        self.dirs = self.chosen
        self.play_number(a_num, t_num)

    def play_name(self, alb_dir, t_num):
        self.select(self.chosen.index(alb_dir), t_num)

    def play_number(self, a_num, t_num):
        View.panel.change_colors('albs', self.num, a_num)
        self.num = a_num if a_num < len(self.dirs) else 0
        self.dir = self.dirs[self.num]
        self.played = os.path.basename(self.dir)
        self.show_tracks(self.dir, t_num, self.shown)
        # =Tracks.show, set in Artists.load

    @staticmethod
    def get_names(alb_dirs):
        return [util.cut_base(d, View.NAME_MAX["alb"]) for d in alb_dirs]

    def next(self):
        a_num = self.num + 1
        if a_num < len(self.dirs):
            self.play_number(a_num, 0)

    @staticmethod
    def convert(name):
        if name[:2] == 'M0':
            return name.replace('M0', '200')

        if name[:2] == 'Op':
            return name.replace('Op', '')

        if re.compile('^\d{2}[\s+|_|-]').match(name):
            return '20' + name if int(name[:2]) < 30 else '19' + name

        return name
