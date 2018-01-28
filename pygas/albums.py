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
        albs = os.listdir(art_dir)
        names = cls.get_names
        cls.shown = list(map(lambda d: os.path.join(art_dir, d), albs))
        View.set_font('albs', cls.get_font([names, None]))
        View.add_buttons('albs', names, lambda a: cls.select(a))

    # t_num - last played track
    @classmethod
    def select(cls, a_num, t_num=0):
        cls.app.artists.selected()
        cls.chosen = cls.shown
        cls.play(a_num, t_num)

    @classmethod
    def play(cls, a_num, t_num=0):
        from .tracks import Tracks

        View.change_colors('albs', cls.num, a_num)
        cls.num = a_num
        cls.played = cls.chosen[cls.num]
        from .artists import Artists
        Tracks.show(os.path.join(Artists.played_directory(), cls.played), t_num)

    @classmethod
    def get_names(cls):
        return list(map(lambda name: util.cut(name, cls.app.NAME_MAX["alb"])))

