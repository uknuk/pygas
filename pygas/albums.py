import os
from . import util
from .view import View


class Albums:
    
    shown = []
    chosen = []
    dirs = []
    dir = None
    played = None
    num = 0
       
    @classmethod
    def show(cls, art_dir, shown_tracks):
        albs = os.listdir(art_dir)
        cls.shown = cls.get_names(albs)
        cls.chosen = [os.path.join(art_dir, a) for a in albs]
        View.set_items_font('albs', [cls.shown, shown_tracks])
        View.add_buttons('albs', cls.shown, cls.clicked)
        View.switch_to('player')

    @classmethod
    def clicked(cls, _, a_num):
        cls.select(a_num)

    @classmethod
    def select(cls, a_num, t_num=0):
        cls.dirs = cls.chosen
        cls.play_number(a_num, t_num)

    @classmethod
    def play_name(cls, alb_dir, t_num):
        cls.select(cls.chosen.index(alb_dir), t_num)

    @classmethod
    def play_number(cls, a_num, t_num):
        View.change_colors('albs', cls.num, a_num)
        cls.num = a_num
        cls.dir = cls.dirs[cls.num]
        cls.played = os.path.basename(cls.dir)
        cls.show_tracks(cls.dir, t_num, cls.shown)

    @classmethod
    def get_names(cls, alb_dirs):
        return [util.cut_base(d, View.NAME_MAX["alb"]) for d in alb_dirs]

    @classmethod
    def next(cls):
        print("not implemented")

