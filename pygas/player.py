import gi
from gi.repository import Gst
import math
from .view import View
from .tracks import Tracks


class Player:

    duration = 0
    bitrate = 0
    bin = None
    bus = None

    @classmethod
    def init(cls):
        Tracks.play_track = cls.play
        Gst.init(None)
        cls.bin = Gst.ElementFactory.make("playbin", "player")
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
            Tracks.next()

    @classmethod
    def play(cls, track):
        cls.stop()
        cls.bin.set_property('uri', "file://{}".format(track))
        cls.bin.set_state(Gst.State.PLAYING)

    @classmethod
    def update_position(cls):
        if not cls.is_state(Gst.State.PLAYING):
            return True

        if cls.duration == 0:
            cls.duration = cls.bin.query_duration(Gst.Format.TIME)[1]

        View.update_slider(cls.bin.query_position(Gst.Format.TIME)[1], cls.duration)
        return True

    @classmethod
    def change_state(cls):
        if cls.is_state(Gst.State.PLAYING):
            cls.bin.set_state(Gst.State.PAUSED)
        elif cls.is_state(Gst.State.PAUSED):
            cls.bin.set_state(Gst.State.PLAYING)

    @classmethod
    def volume(cls, delta):
        vol = cls.bin.get_property('volume')
        db = 10*math.log10(vol) + delta
        vol = math.pow(10, db/10)
        if vol < 10:
            cls.bin.set_property('volume', vol)
            View.switch_to('player')
            View.write_label('vol', "{} db".format(int(db)))

    @classmethod
    def stop(cls):
        cls.bin.set_state(Gst.State.NULL)
        cls.duration = 0

    @classmethod
    def is_state(cls, state):
        return cls.bin.get_state(1000)[1] == state







