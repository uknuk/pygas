from dotmap import DotMap
from datetime import datetime
#from functools import reduce
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Pango', '1.0')
from gi.repository import Pango
from . import util


def time(usecs):
    return datetime.fromtimestamp(usecs/1e9).isoformat()[-12:-7]  # min:sec


class Panel:

    def __init__(self, win, tabs, width, height):
        self.win = win
        self.max_width = width
        self.max_height = height/2

        self.desc = Pango.FontDescription(string='Ubuntu')
        self.layout = Gtk.Label().get_layout()

        self.labels = DotMap({'tracks': [], 'albs': [], 'sel_arts': [], 'sel_art': Gtk.Label()})

        self.panes = DotMap({
            "song": Gtk.FlowBox(selection_mode=0),  # NONE
            'info': Gtk.Box(),
            'sep1': Gtk.HSeparator(),
            'sel_art': self.labels.sel_art,
            'albs': Gtk.Box(orientation=Gtk.Orientation.VERTICAL),
            'sep2': Gtk.HSeparator(),
            'tracks': Gtk.Box(orientation=Gtk.Orientation.VERTICAL),
            'sel_arts': Gtk.Box(orientation=Gtk.Orientation.VERTICAL),
            'arts': Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        })

        self.pack_start(tabs.arts, self.panes.sel_arts)
        self.pack_start(tabs.arts, self.panes.arts)

        [self.pack_start(tabs.player, self.panes[k]) for k in ["song", "info", "sel_art"]]
        [self.pack_start(tabs.player, self.framed(self.panes[k])) for k in ["albs", "tracks"]]

        for l in ['alb', 'track']:
            self.labels[l] = Gtk.Label()
            self.panes.song.add(self.labels[l])

        for l in ['vol', 'rate']:
            self.labels[l] = Gtk.Label()
            self.panes.info.pack_end(self.labels[l], False, False, 1)

        self.slider = Gtk.ProgressBar(show_text=True)
        self.pack_start(self.panes.info, self.slider, True)
        #self.arts = None

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
        # font_size = self.font_size[kind] # or self.font_size.info
        self.write(self.labels[kind], txt, self.font_size[kind], Panel.COLOR[kind])

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

    def set_button(self, kind, txt, fun, n, active=False):
        lbl = Gtk.Label()
        # list of labels needed to change color by index
        try:
            self.labels[kind][n] = lbl
        except IndexError:
            self.labels[kind].append(lbl)

        color = 'red' if active else Panel.COLOR[kind]
        lbl.modify_font(self.desc)
        lbl.set_markup(util.set_span(txt, color))
        size = lbl.get_layout().get_pixel_size()
        btn = Gtk.Button()
        btn.connect("clicked", fun, n)
        btn.add(lbl)
        # if kind == 'arts':
        #     self.arts.append(btn)

        btn.set_size_request(size[0], size[1])
        align = Gtk.Alignment()
        align.add(btn)
        return align, size[0]

    def add_buttons(self, kind, names, fun, played=None):
        self.desc.set_size(int(round(int(Panel.font_size[kind] * Pango.SCALE))))
        # if kind == 'arts':
        #     self.arts = []
        # else:
        self.clear(kind)

        n = 0
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        length = 0
        for name in names:
            (align, width) = self.set_button(kind, name, fun, n, n == played)
            n += 1
            length += width + 20
            if length >= self.max_width:
                self.pack_start(self.panes[kind], row)
                row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
                length = width

            self.pack_start(row, align)

        self.pack_start(self.panes[kind], row)
        self.win.show_all()

    def select_font(self, items):
        for s in range(*Panel.FONT_RANGE):
            self.desc.set_size(int(round(int(s) * Pango.SCALE)))
            self.layout.set_font_description(self.desc)
            width = height = 0
            for item in items:
                self.layout.set_markup(item.replace('&', '&amp;'))
                size = self.layout.get_pixel_size()
                width += size[0] + Panel.WIDTH_MARGIN
                if width > self.max_width:
                    height += size[1] + Panel.HEIGHT_MARGIN
                    if height >= self.max_height:
                        break
                    else:
                        width = size[0]

            if height < self.max_height:
                break

        Panel.font_size.tracks = Panel.font_size.albs = s

    #def show_artists(self):
        # if visible:
        #     self.clear('sel_arts')
        # [btn.set_sensitive(visible) for btn in self.arts]


    def clear(self, kind):
        [child.destroy() for child in self.panes[kind].get_children()]

    def update_slider(self, pos, duration):
        self.slider.set_fraction(pos / duration)
        self.slider.set_text("{}/{}".format(time(pos), time(duration)))

    def set_info(self, info):
        for key, val in info.items():
            for i in range(40, 10, -1):
                self.desc.set_size(int(round(int(i) * Pango.SCALE)))
                self.layout.set_font_description(self.desc)
                self.layout.set_markup(val)
                size = self.layout.get_pixel_size()
                if size[0] < 1024:
                    break

            self.labels[key].modify_font(self.desc)
            self.labels[key].set_markup(util.set_span(val, Panel.COLOR[key]))

    @staticmethod
    def write(lbl, txt, size, color):
        lbl.set_markup(util.set_span(txt, color, size))

    @staticmethod
    def framed(pane):
        frame = Gtk.Frame()
        frame.add(pane)
        return frame

