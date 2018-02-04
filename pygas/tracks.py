from os import path, listdir

from .view import View
from . import util
from .artists import Artists


class Tracks:
    files = []
    shown = []
    num = 0

    @classmethod
    def show(cls, alb, num):
        from .albums import Albums
        from . import NAME_MAX

        Artists.selected()
        alb_dir = path.join(Artists.played_directory(), alb)
        cls.files = sorted([alb_dir] if path.isfile(alb_dir) else cls.load(alb_dir))
        cls.shown = [util.cut_base(f, NAME_MAX["track"]) for f in cls.files]

        View.font_size.tracks = util.items_font_size([cls.shown, Albums.shown])
        View.add_buttons('tracks', cls.shown, cls.clicked)
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
    def clicked(cls, _, num):
        cls.play(num)

    @classmethod
    def play(cls, num):
        from .player import Player

        View.change_colors('tracks', cls.num, num)
        cls.num = num
        track = cls.files[cls.num]
        Tracks.set_info(path.basename(track))
        Player.play(track)
        Tracks.save()

    @staticmethod
    def set_info(track):
        art, alb = Tracks.get_played()
        name_size = len(art + alb + track)
        View.font_size.info = util.font_size(name_size, 'info')
        View.write_label('art', art)
        View.write_label('alb', alb)
        View.write_label('track', track)

    @staticmethod
    def get_played():
        from .albums import Albums
        return Artists.played, Albums.played

    @classmethod
    def save(cls):
        from . import LAST_FILE

        art, alb = Tracks.get_played()
        with util.open_file(LAST_FILE, 'w') as f:
            f.write("\n".join([art, alb, str(cls.num)]))
