from os import path, listdir
import re
from .view import View
from . import util


class Tracks:
    def __init__(self):
        self.files = []
        self.shown = []
        self.num = 0
        self.arts = None
        self.next_album = None

    def inject(self, arts, next_album):
        self.arts = arts
        self.next_album = next_album

    def show(self, alb, num, shown_albums):
        self.arts.selected()
        alb_dir = path.join(self.arts.played_directory(), alb)
        self.files = sorted([alb_dir] if path.isfile(alb_dir) else self.load(alb_dir))
        self.shown = [util.cut_base(f, View.NAME_MAX["track"]) for f in self.files]
        self.arts.restore()

        View.panel.select_font(self.shown + shown_albums)
        View.panel.add_buttons('tracks', self.shown, self.clicked)
        self.play(num)

    @staticmethod
    def load(alb):
        tracks = []
        # exp = re.compile('\.mp3$|\.mp4a$|\.mpc$|\.ogg$') doesn't work
        exp = re.compile('.*mp3|.*mp4a|.*mpc|.*ogg|.*webm')
        for entry in list(map(lambda f: path.join(alb, f), listdir(alb))):
            if path.isfile(entry):
                if exp.match(entry):
                    tracks.append(entry)
            else:
                tracks += Tracks.load(entry)
        return tracks

    def clicked(self, _, num):
        self.play(num)

    def play(self, num):
        View.panel.change_colors('tracks', self.num, num)
        View.scroll('Up')
        self.num = num
        track = self.files[num]
        self.set_info(path.basename(track))
        self.play_track(track)  # Player.play
        self.save()

    def set_info(self, track):
        art, alb = self.arts.get_played()
        View.panel.set_info({'alb': alb, 'track': track})
        View.set_artist(art)

    def save(self):
        art, alb = self.arts.get_played()
        # track = f"{path.splitext(path.basename(self.files[self.num]))[0]}\n"
        track = "{}\n".format(path.splitext(path.basename(self.files[self.num]))[0])
        with util.open_file(self.LAST_FILE, 'w') as f:
            f.write("\n".join([art, alb, str(self.num), track]))

    def next(self):
        next_num = self.num + 1
        if next_num == len(self.files):
            self.next_album()
        else:
            self.play(next_num)
