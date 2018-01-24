import os
from . import util
from .view import View
from .artists import Artists
from .player import Player

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
        View.add_buttons('albs', names, lambda a,t: cls.select(a,t))

    # t_num - last played track
    @classmethod
    def select(cls, a_num, t_num):
        cls.app.artists.selected()
        cls.chosen = cls.shown
        cls.play(a_num, t_num)

    @classmethod
    def play(cls, a_num, t_num = 0):
        View.change_colors('albs', cls.num, a_num)
        cls.num = a_num
        cls.played = cls.chosen[cls..num]
        Player.load_album(Artists.played_directory(), cls.played)
        # move adding track buttons to Player

    @classmethod
    def get_names(cls):
        return list(map(lambda name: util.cut(name, cls.app.NAME_MAX["alb"])))

