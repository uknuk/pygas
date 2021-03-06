from os import path, listdir
import re
from .view import View
from . import util


class Tracks:
    files = []
    shown = []
    num = 0

    @classmethod
    def inject(cls, arts, next_album):
        cls.arts = arts
        cls.next_album = next_album

    @classmethod
    def show(cls, alb, num, shown_albums):
        cls.arts.selected()
        alb_dir = path.join(cls.arts.played_directory(), alb)
        cls.files = sorted([alb_dir] if path.isfile(alb_dir) else cls.load(alb_dir))
        cls.shown = [util.cut_base(f, View.NAME_MAX["track"]) for f in cls.files]
        cls.arts.restore()

        View.set_items_font('tracks', [cls.shown, shown_albums])
        View.add_buttons('tracks', cls.shown, cls.clicked)
        cls.play(num)

    @staticmethod
    def load(alb):
        tracks = []
        # exp = re.compile('\.mp3$|\.mp4a$|\.mpc$|\.ogg$') doesn't work
        exp = re.compile('.*mp3|.*mp4a|.*mpc|.*ogg')
        for entry in list(map(lambda f: path.join(alb, f), listdir(alb))):
            if path.isfile(entry):
                if exp.match(entry):
                    tracks.append(entry)
            else:
                tracks += Tracks.load(entry)
        return tracks

    @classmethod
    def clicked(cls, _, num):
        cls.play(num)

    @classmethod
    def play(cls, num):
        View.change_colors('tracks', cls.num, num)
        View.scroll('Up')
        cls.num = num
        track = cls.files[num]
        cls.set_info(path.basename(track))
        cls.play_track(track)  # Player.play
        cls.save()

    @classmethod
    def set_info(cls, track):
        art, alb = cls.arts.get_played()
        View.set_font('info', max(len(alb), len(track)))
        View.header.set_title(art)
        View.write_label('alb', alb)
        View.write_label('track', track)

    @classmethod
    def save(cls):
        art, alb = cls.arts.get_played()
        with util.open_file(cls.LAST_FILE, 'w') as f:
            f.write("\n".join([art, alb, str(cls.num)]))

    @classmethod
    def next(cls):
        next_num = cls.num + 1
        if next_num == len(cls.files):
            cls.next_album()
        else:
            cls.play(next_num)
