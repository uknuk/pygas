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
    def show(cls, art_dir):
        from .tracks import Tracks

        albs = os.listdir(art_dir)
        cls.shown = cls.get_names(albs)
        cls.chosen = [os.path.join(art_dir, a) for a in albs]
        View.font_size.albs = util.items_font_size([cls.shown, Tracks.shown])
        View.add_buttons('albs', cls.shown, cls.clicked)
        View.switch_to('player')
        View.win.show_all()

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
        from .tracks import Tracks

        View.change_colors('albs', cls.num, a_num)
        cls.num = a_num
        # cls.played = cls.shown[cls.num]
        cls.dir = cls.dirs[cls.num]
        cls.played = os.path.basename(cls.dir)
        Tracks.show(cls.dir, t_num)

    @classmethod
    def get_names(cls, alb_dirs):
        from . import NAME_MAX
        return [util.cut_base(d, NAME_MAX["alb"]) for d in alb_dirs]

