

import gi
from gi.repository import Gst


class Player:

    def __init__(self, app):
        self.app = app
        self.bin = Gst.ElementFactory.make("playbin", "play")
        self.bus = bin.get_bus()
        self.tracks = []
        self.duration = 0
        self.bitrate = 0
        self.track_num = None
        self.view = None
        Gst.init(None, 0)

    def init(self, view):
        self.view = view
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_message)

    def on_message(self, bus, msg):
        if msg.type == Gst.MessageType.TAG:
            rate = msg.parse_tag().get_uint('bitrate')[1] #[1]
            if rate != self.bitrate:
                bitrate = rate
                self.view.write_label('rate', "{} kbps".format(int(bitrate/1e3)))

        if msg.type == Gst.MessageType.EOS:
            next = self.track_num + 1
            if next == self.tracks.length:
                self.app.next_album()
            else:
                self.play_track(next)
