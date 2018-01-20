import gi
from gi.repository import Gst
import os


class Player:

    def __init__(self, app):
        Gst.init(None)
        self.app = app
        self.view = app.view
        self.tracks = []
        self.duration = 0
        self.bitrate = 0
        self.num = None

        self.bin = Gst.ElementFactory.make("playbin", "play")
        self.bus = self.bin.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_message)
       
    def on_message(self, bus, msg):
        if msg.type == Gst.MessageType.TAG:
            rate = msg.parse_tag().get_uint('bitrate')[1]  # [1]
            if rate != self.bitrate:
                self.bitrate = rate
                self.view.write_label('rate', "{} kbps".format(int(rate / 1e3)))

        if msg.type == Gst.MessageType.EOS:
            next = self.track_num + 1
            if next == self.tracks.length:
                self.app.next_album()
            else:
                self.play_track(next)

    def play_track(self, num):
        self.view.change_colors('tracks', self.track_num, num)
        self.num = num
        track = self.tracks[self.num]
        self.app.set_info(os.path.basename(track))
        bin.set_state(Gst.State.NULL)
        self.duration = 0
        bin.set_property('uri', "file://{}".format(track))
        bin.set_state(Gst.State.PLAYING);
        self.app.save(num)
