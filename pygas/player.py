import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import math
from .view import View


class Player:
    def __init__(self, tracks):
        self.duration = 0
        self.bitrate = 0
        Gst.init(None)
        self.bin = Gst.ElementFactory.make("playbin", "player")
        self.bus = self.bin.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_message)
        tracks.play_track = self.play
        self.tracks = tracks
        
    def on_message(self, _, msg):
        if msg.type == Gst.MessageType.TAG:
            rate = msg.parse_tag().get_uint('bitrate')[1]  # [1]
            if rate != self.bitrate:
                self.bitrate = rate
                View.panel.write_label('rate', "{} kbps".format(int(rate / 1e3)))

        if msg.type == Gst.MessageType.EOS:
            self.tracks.next()

    def play(self, track):
        self.stop()
        self.bin.set_property('uri', "file://{}".format(track))
        self.bin.set_state(Gst.State.PLAYING)

    def update_position(self):
        if not self.is_state(Gst.State.PLAYING):
            return True

        if self.duration == 0:
            self.duration = self.bin.query_duration(Gst.Format.TIME)[1]

        if self.duration != 0:
            View.panel.update_slider(self.bin.query_position(Gst.Format.TIME)[1], self.duration)

        return True

    def change_state(self):
        if self.is_state(Gst.State.PLAYING):
            self.bin.set_state(Gst.State.PAUSED)
        elif self.is_state(Gst.State.PAUSED):
            self.bin.set_state(Gst.State.PLAYING)

    def volume(self, delta):
        vol = self.bin.get_property('volume')
        db = 10*math.log10(vol) + delta
        vol = math.pow(10, db/10)
        if vol < 10:
            self.bin.set_property('volume', vol)
            View.switch_to('player')
            View.panel.write_label('vol', "{} db".format(int(db)))

    def stop(self):
        self.bin.set_state(Gst.State.NULL)
        self.duration = 0

    def is_state(self, state):
        return self.bin.get_state(1000)[1] == state
