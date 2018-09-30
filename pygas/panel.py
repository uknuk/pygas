from dotmap import DotMap
from datetime import datetime
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Pango', '1.0')
from gi.repository import Pango

def time(usecs):
    return datetime.fromtimestamp(usecs/1e9).isoformat()[-12:-7]  # min:sec

class Panel:

    def __init__(self, frames):
        self.css = Gtk.CssProvider()
        self.css.load_from_data(
            bytes("GtkTextView { font-size: 16px; font-weight: bold; color: #a00; }".encode()))

        self.buffer = Gtk.TextBuffer()
        self.text = Gtk.TextView(buffer=self.buffer, wrap_mode=Gtk.WrapMode.WORD)
        self.text.get_style_context().add_provider(self.css, 0)

        self.desc = Pango.FontDescription(string = 'Ubuntu')
        self.layout = Gtk.Label().get_layout()

        self.labels = DotMap({'tracks': [], 'albs': [], 'sel_arts': [], 'sel_art': Gtk.Label()})

        self.panes = DotMap({
            "song": Gtk.FlowBox(selection_mode=0),  # NONE
            'info': Gtk.Box(),
            'sep1': Gtk.HSeparator(),
            'sel_art': self.labels.sel_art,
            'albs': Gtk.FlowBox(),
            'sep2': Gtk.HSeparator(),
            'tracks': Gtk.FlowBox(),
            'sel_arts': Gtk.Box(orientation=Gtk.Orientation.VERTICAL),
            'arts': Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        })

        self.pack_start(frames.arts, self.panes.sel_arts)
        self.pack_start(frames.arts, self.panes.arts)

        pane_keys = ["song", "info", "sel_art", "albs", "tracks"]
        [self.pack_start(frames.player, self.panes[k]) for k in pane_keys]

        for l in ['alb', 'track']:
            self.labels[l] = Gtk.Label()
            self.panes.song.add(self.labels[l])

        for l in ['vol', 'rate']:
            self.labels[l] = Gtk.Label()
            self.panes.info.pack_end(self.labels[l], False, False, 1)

        self.slider = Gtk.ProgressBar(show_text=True)
        self.pack_start(self.panes.info, self.slider, True)

    def change_color(self, kind, n, fro, to):
        lbl = self.labels[kind][n]
        if lbl:
            lbl.set_markup(lbl.get_label().replace(fro, to))

    def change_colors(self, kind, prev, curr):
        if prev != curr:
            self.change_color(kind, prev, "'red'", "'{}'".format(Panel.COLOR[kind]))

        self.change_color(kind, curr, "'{}'".format(Panel.COLOR[kind]), "'red'")

    @staticmethod
    def pack_start(container, item, flag=False):
        container.pack_start(item, flag, flag, 1)

    def write_label(self, kind, txt):
        font_size = self.font_size.get(kind) or self.font_size.info
        return self.write(self.labels[kind], txt, font_size, Panel.COLOR[kind])

    def add_button(self, kind, txt, fun, n, active=False):
        lbl = Gtk.Label()
        # list of labels needed to change color by index
        try:
            self.labels[kind][n] = lbl
        except IndexError:
            self.labels[kind].append(lbl)

        color = 'red' if active else Panel.COLOR[kind]
        self.write(lbl, txt, Panel.font_size[kind], color)
        btn = Gtk.Button()
        btn.connect("clicked", fun, n)
        btn.add(lbl)
        self.panes[kind].add(btn)

    def add_artists(self, kind, names, fun):
        self.desc.set_size(int(round(int(Panel.font_size[kind] * Pango.SCALE))))
        if kind == 'arts':
            self.arts = []
        else:
            self.clear(kind)

        n = 0
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        length = 0
        for name in names:
            lbl = Gtk.Label()
            lbl.modify_font(self.desc)
            lbl.set_markup(name.replace('&', '&amp;'))
            size = lbl.get_layout().get_pixel_size()
            btn = Gtk.Button()
            btn.connect("clicked", fun, n)
            n = n + 1
            btn.set_size_request(size[0], size[1])
            btn.add(lbl)
            if kind == 'arts':
                self.arts.append(btn)

            align = Gtk.Alignment()
            align.add(btn)
            length = length + size[0] + 20
            if length > 1024:
                self.pack_start(self.panes[kind], row)
                row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
                length = size[0]

            self.pack_start(row, align)

        self.pack_start(self.panes[kind], row)

    def show_artists(self, visible):
        if visible:
            self.clear('sel_arts')
        [btn.set_sensitive(visible) for btn in self.arts]

    @staticmethod
    def write(lbl, txt, size, color):
        return lbl.set_markup(
            "<span color='{}' font='{}'>{}</span>".format(color, size, txt.replace('&', '&amp;')))

    def clear(self, kind):
        [child.destroy() for child in self.panes[kind].get_children()]

    @classmethod
    def get_font(cls, kind, length):
        fp = Panel.FONT_PARAMS[kind]
        diff = max(length - fp[2], 0)
        fs = int(max(fp[0] - diff / fp[3], fp[1]))
        return fs

    def update_slider(self, pos, duration):
        self.slider.set_fraction(pos / duration)
        self.slider.set_text("{}/{}".format(time(pos), time(duration)))

    def set_info(self, info):
        for key, val in info.items():
            for i in range (40,10,-1):
                self.desc.set_size(int(round(int(i) * Pango.SCALE)))
                self.layout.set_font_description(self.desc)
                self.layout.set_markup(val)
                size = self.layout.get_pixel_size()
                if size[0] < 1024:
                    break

            self.labels[key].modify_font(self.desc)
            self.labels[key].set_markup(
                "<span color='{}'>{}</span>".format(Panel.COLOR[key], val.replace('&', '&amp;')))
