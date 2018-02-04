import gi
from gi.repository import Gst
import math
from .view import View


class Player:

    duration = 0
    bitrate = 0
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
        from .albums import Albums
        from .tracks import Tracks

        if msg.type == Gst.MessageType.TAG:
            rate = msg.parse_tag().get_uint('bitrate')[1]  # [1]
            if rate != cls.bitrate:
                cls.bitrate = rate
                View.write_label('rate', "{} kbps".format(int(rate / 1e3)))

        if msg.type == Gst.MessageType.EOS:
            next_num = cls.track_num + 1
            if next_num == cls.tracks.length:
                Albums.next()
            else:
                Tracks.play(next_num)

    @classmethod
    def play(cls, track):
        cls.stop()
        bin.set_property('uri', "file://{}".format(track))
        bin.set_state(Gst.State.PLAYING)

    @classmethod
    def update_position(cls):
        if not cls.is_state(Gst.State.PLAYING):
            return True

        if cls.duration == 0:
            cls.duration = cls.bin.query_duration(Gst.Format.TIME)[1]

        pos = bin.query_position(Gst.Format.TIME)[1]
        View.slider.fraction = pos / cls.duration
        View.slider.text = "{}/{}".format(cls.time(pos), cls.time(cls.duration))
        return True

    @classmethod
    def change_state(cls):
        if cls.is_state(Gst.State.PLAYING):
            cls.bin.set_state(Gst.State.PAUSED)
        elif cls.is_state(Gst.State.PAUSED):
            cls.bin.set_state(Gst.State.PLAYING)

    @classmethod
    def volume(cls, delta):
        db = math.log10(cls.bin.volume + delta)
        cls.bin.volume = min(math.pow(10, db/10), cls.bin.volume)
        View.switch_to('player')
        View.write_label('vol', "{} db".format(int(db)))

    @classmethod
    def stop(cls):
        cls.bin.set_state(Gst.State.NULL)
        cls.duration = 0

    @classmethod
    def is_state(cls, state):
        return cls.bin.get_state(1000)[1] == state







