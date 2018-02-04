import os
from . import util
from .view import View


class Albums:
    
    shown = []
    chosen = []
    played = None
    num = 0
       
    @classmethod
    def show(cls, art_dir):
        from .tracks import Tracks

        albs = os.listdir(art_dir)
        names = cls.get_names(albs)
        cls.shown = list(map(lambda d: os.path.join(art_dir, d), albs))
        View.font_size.albs = util.items_font_size([names, Tracks.names])
        View.add_buttons('albs', names, lambda a: cls.select(a))

    @classmethod
    def select(cls, a_num):
        cls.chosen = cls.shown
        cls.play_number(a_num, 0)

    @classmethod
    def play_name(cls, alb, t_num):
        cls.chosen = alb
        a_num = cls.chosen.index(alb)
        cls.play_number(a_num, t_num)

    @classmethod
    def play_number(cls, a_num, t_num):
        from .tracks import Tracks

        View.change_colors('albs', cls.num, a_num)
        cls.num = a_num
        cls.played = cls.chosen[cls.num]
        Tracks.show(cls.played, t_num)

    @classmethod
    def get_names(cls, albs):
        from . import NAME_MAX
        return list(map(lambda name: util.cut(util.base(name), NAME_MAX["alb"]), albs))

