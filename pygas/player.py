import gi
from gi.repository import Gst
import os
from .view import View
from .albums import Albums
from .artists import Artists
from . import util


class Player:
    
    tracks = []
    duration = 0
    bitrate = 0
    num = None
    bin = None
    bus = None

    @classmethod
    def init(cls):
        Gst.init(None)
        cls.bin = Gst.ElementFactory.make("playbin", "play")
        cls.bus = cls.bin.get_bus()
        cls.bus.add_signal_watch()
        cls.bus.connect('message', cls.on_message)

    @classmethod
    def on_message(cls, _, msg):
        if msg.type == Gst.MessageType.TAG:
            rate = msg.parse_tag().get_uint('bitrate')[1]  # [1]
            if rate != cls.bitrate:
                cls.bitrate = rate
                View.write_label('rate', "{} kbps".format(int(rate / 1e3)))

        if msg.type == Gst.MessageType.EOS:
            next_num = cls.track_num + 1
            if next_num == cls.tracks.length:
                Albums.next_track()
            else:
                cls.play_track(next_num)

    @classmethod
    def play_track(cls, num):
        cls.view.change_colors('tracks', cls.track_num, num)
        cls.num = num
        track = cls.tracks[cls.num]
        cls.set_info(os.path.basename(track))
        bin.set_state(Gst.State.NULL)
        cls.duration = 0
        bin.set_property('uri', "file://{}".format(track))
        bin.set_state(Gst.State.PLAYING);
        util.save(Artists.played, Albums.played, num)

    @classmethod
    def set_info(cls, track):
        name_size = len(Artists.played + Albums.played + track)
        View.set_font('info', util.font_size(name_size, 'info'))
        View.write_label('art', Artists.played)
        View.write_label('alb', Albums.played)
        View.write_label('track', track)