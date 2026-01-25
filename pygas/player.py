import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import math
import os
from .view import View


class Player:
    def __init__(self, tracks):
        self.duration = 0
        self.bitrate = 0
        self.current_track = None
        Gst.init(None)
        self.bin = Gst.ElementFactory.make("playbin", "player")
        self.bus = self.bin.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_message)
        tracks.play_track = self.play
        self.tracks = tracks
        
    def on_message(self, _, msg):
        if msg.type == Gst.MessageType.TAG:
            tags = msg.parse_tag()
            success, rate = tags.get_uint('bitrate')
            if not success:
                success, rate = tags.get_uint('nominal-bitrate')
            if success and rate != self.bitrate:
                self.bitrate = rate
                View.panel.write_label('rate', "{} kbps".format(int(rate / 1e3)))
        if msg.type == Gst.MessageType.EOS:
            self.tracks.next()

    def play(self, track):
        self.stop()
        self.current_track = track
        self.bin.set_property('uri', "file://{}".format(track))
        self.bin.set_state(Gst.State.PLAYING)
        
        # Reset bitrate for new track, will be calculated or read from tags
        self.bitrate = 0
        
        # Schedule bitrate calculation from file size if tags don't provide it
        try:
            filesize = os.path.getsize(track)
            GLib.timeout_add(500, self.calculate_bitrate_from_file, filesize)
        except:
            pass
    
    def calculate_bitrate_from_file(self, filesize):
        """Calculate bitrate from file size and duration if not available from tags"""
        # Only calculate if we don't have bitrate from tags
        if self.bitrate != 0:
            return False
            
        if self.duration == 0:
            success, duration = self.bin.query_duration(Gst.Format.TIME)
            if success:
                self.duration = duration
        
        if self.duration > 0:
            # bitrate = (filesize * 8) / (duration_in_seconds)
            duration_sec = self.duration / Gst.SECOND
            bitrate_bps = (filesize * 8) / duration_sec
            self.bitrate = int(bitrate_bps)
            View.panel.write_label('rate', "{} kbps".format(int(bitrate_bps / 1e3)))
            return False  # Done
        
        # Try again if duration not yet available
        return True

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
