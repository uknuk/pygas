from os import path, listdir

from .view import View
from . import util
from .artists import Artists


class Tracks:
    names = []
    num = 0

    @classmethod
    def show(cls, alb, num):
        from .albums import Albums

        Artists.selected()
        alb_dir = path.join(Artists.played_directory(), alb)
        cls.names = [alb_dir] if path.isfile(alb_dir) else cls.load(alb_dir)

        View.font_size.tracks = util.items_font_size([cls.names, Albums.names])
        View.add_buttons('tracks', cls.names, cls.play)
        cls.play(num)

    @staticmethod
    def load(alb):
        tracks = []
        for entry in list(map(lambda f: path.join(alb, f), listdir(alb))):
            if path.isfile(entry):
                tracks.append(entry)  # add regular exp
            else:
                tracks += Tracks.load(entry)
        return tracks

    @classmethod
    def play(cls, num):
        from .player import Player

        View.change_colors('tracks', cls.num, num)
        cls.num = num
        track = cls.names[cls.num]
        Tracks.set_info(path.basename(track))
        Player.play(track)
        bin.set_state(Gst.State.NULL)
        cls.duration = 0
        bin.set_property('uri', "file://{}".format(track))
        bin.set_state(Gst.State.PLAYING)
        Tracks.save(num)

    @staticmethod
    def set_info(track):
        art, alb = Tracks.get_payed()
        name_size = len(art + alb + track)
        View.font_size.info = util.font_size(name_size, 'info')
        View.write_label('art', art)
        View.write_label('alb', alb)
        View.write_label('track', track)

    @staticmethod
    def get_played():
        from .albums import Albums
        return Artists.played, Albums.played

    @staticmethod
    def save(track_num):
        from . import LAST_FILE

        art, alb = Tracks.get_played()
        with util.open_file(LAST_FILE) as f:
            f.write_lines("\n".join([art, alb, track_num]))
