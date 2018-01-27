from os import path, listdir

from .view import View
from .albums import Albums
from .artists import Artists
from .player import Player
from . import util


class Tracks:
    names = []
    num = 0

    @classmethod
    def show(cls, art_dir, alb):
        alb_dir = path.join(art_dir, alb)
        cls.names = [alb_dir] if path.isfile(alb_dir) else cls.load(alb_dir)

        View.set_font('tracks', cls.get_font(None, cls.names))
        View.add_buttons('tracks', cls.names, cls.play)

    @staticmethod
    def load(alb):
        tracks = []
        for entry in list.map(lambda f: path.join(alb, f), listdir(alb)):
            if path.isfile(entry):
                tracks.append(entry)  # add regular exp
            else:
                tracks += Tracks.load(entry)
        return tracks

    @classmethod
    def play(cls, num):
        View.change_colors('tracks', cls.num, num)
        cls.num = num
        track = cls.names[cls.num]
        cls.set_info(path.basename(track))
        Player.play(track)
        bin.set_state(Gst.State.NULL)
        cls.duration = 0
        bin.set_property('uri', "file://{}".format(track))
        bin.set_state(Gst.State.PLAYING)
        cls.save(Artists.played, Albums.played, num)

    @classmethod
    def set_info(cls, track):
        name_size = len(Artists.played + Albums.played + track)
        View.set_font('info', util.font_size(name_size, 'info'))
        View.write_label('art', Artists.played)
        View.write_label('alb', Albums.played)
        View.write_label('track', track)
