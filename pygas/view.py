from dotmap import DotMap
import gi
from gi.repository import Gtk
from datetime import datetime
from functools import reduce

gi.require_version('Gtk', '3.0')


def time(usecs):
    return datetime.fromtimestamp(usecs/1e9).isoformat()[-12:-7]  # min:sec


class View:

    @classmethod
    def init(cls, app):
        cls.win = Gtk.ApplicationWindow(application=app,
                                        default_height=cls.HEIGHT,
                                        default_width=cls.WIDTH,
                                        window_position=Gtk.WindowPosition.CENTER)

        cls.header = Gtk.HeaderBar()
        cls.header.set_show_close_button(True)
        cls.win.set_titlebar(cls.header)

        cls.css = Gtk.CssProvider()
        cls.css.load_from_data(
            bytes("GtkTextView { font-size: 16px; font-weight: bold; color: #a00; }".encode()))

        cls.buffer = Gtk.TextBuffer()
        cls.text = Gtk.TextView(buffer=cls.buffer, wrap_mode=Gtk.WrapMode.WORD)
        cls.text.get_style_context().add_provider(cls.css, 0)

        cls.frames = DotMap({
            "player": Gtk.Box(orientation=Gtk.Orientation.VERTICAL),
            "arts": Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        })
        sel_arts = Gtk.FlowBox()
        h = sel_arts.get_homogeneous()
        cls.pack_start(cls.frames.arts, sel_arts)
        cls.pack_start(cls.frames.arts, cls.text)

        cls.labels = DotMap({'tracks': [], 'albs': [], 'sel_arts': [], 'sel_art': Gtk.Label()})
        cls.panes = DotMap({
            "song": Gtk.FlowBox(selection_mode=0),  # NONE
            'info': Gtk.Box(),
            'sep1': Gtk.HSeparator(),
            'sel_art': cls.labels.sel_art,
            'albs': Gtk.FlowBox(min_children_per_line=3),
            'sep2': Gtk.HSeparator(),
            'tracks': Gtk.FlowBox(min_children_per_line=3)
        })
        cls.panes.sel_arts = sel_arts

        pane_keys = ["song", "info", "sep1", "sel_art", "albs", "sep2", "tracks"]
        [cls.pack_start(cls.frames.player, cls.panes[k]) for k in pane_keys]

        for l in ['alb', 'track']:
            cls.labels[l] = Gtk.Label()
            cls.panes.song.add(cls.labels[l])

        for l in ['vol', 'rate']:
            cls.labels[l] = Gtk.Label()
            cls.panes.info.pack_end(cls.labels[l], False, False, 1)

        cls.slider = Gtk.ProgressBar(show_text=True)
        cls.pack_start(cls.panes.info, cls.slider, True)
        
        cls.make_stack_switcher()
        cls.make_search()
        cls.make_scrolled()



    @classmethod
    def change_color(cls, kind, n, fro, to):
        lbl = cls.labels[kind][n]
        if lbl:
            lbl.set_markup(lbl.get_label().replace(fro, to))

    @classmethod
    def change_colors(cls, kind, prev, next):
        if prev != next:
            cls.change_color(kind, prev, "'red'", "'{}'".format(cls.COLOR[kind]))

        cls.change_color(kind, next, "'{}'".format(cls.COLOR[kind]), "'red'")

    @staticmethod
    def pack_start(container, item, flag=False):
        container.pack_start(item, flag, flag, 1)

    @classmethod
    def write_label(cls, kind, txt):
        font_size = cls.font_size.get(kind) or cls.font_size.info
        return cls.write(cls.labels[kind], txt, font_size, cls.COLOR[kind])

    @classmethod
    def set_button(cls, kind, txt, n):
        lbl = Gtk.Label()
        # list of labels needed to change color by index
        try:
            cls.labels[kind][n] = lbl
        except IndexError:
            cls.labels[kind].append(lbl)

        cls.write(lbl, txt, cls.font_size[kind], cls.COLOR[kind])
        btn = Gtk.Button()
        btn.add(lbl)
        return btn

    @staticmethod
    def write(lbl, txt, size, color):
        return lbl.set_markup(
            "<span color='{}' font='{}'>{}</span>".format(color, size, txt.replace('&', '&amp;')))

    @classmethod
    def switch_to(cls, name):
        cls.stack.set_visible_child_name(name)
        cls.search.bar.set_search_mode(name == 'arts')

    @classmethod
    def scroll(cls, dir):
        adjust = cls.scroll_win.get_vadjustment()
        page_size = adjust.get_page_size()
        adjust.set_value(adjust.get_value() + page_size if dir == 'Down' else -page_size)
        cls.scroll_win.set_vadjustment(adjust)

    @classmethod
    def add_buttons(cls, kind, labels, fun):
        cls.clear(kind)
        n = 0
        for lbl in labels:
            btn = cls.set_button(kind, lbl, n)
            btn.connect("clicked", fun, n)
            n += 1
            cls.panes[kind].add(btn)

        cls.win.show_all()

    @classmethod
    def clear(cls, kind):
        [child.destroy() for child in cls.panes[kind].get_children()]

    @classmethod
    def make_search(cls):
        cls.search = DotMap({"bar": Gtk.SearchBar(), "entry": Gtk.SearchEntry()})
        cls.search.bar.connect_entry(cls.search.entry)
        cls.search.bar.add(cls.search.entry)
        cls.header.add(cls.search.bar)

    @classmethod
    def make_stack_switcher(cls):
        cls.stack = Gtk.Stack()
        for n in ['player', 'arts']:
            cls.stack.add_titled(cls.frames[n], n, n.title())

        cls.switcher = Gtk.StackSwitcher()
        cls.switcher.set_stack(cls.stack)
        cls.header.add(cls.switcher)

    @classmethod
    def make_scrolled(cls):
        cls.scroll_win = Gtk.ScrolledWindow()
        cls.scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        cls.scroll_win.add(cls.stack)
        cls.win.add(cls.scroll_win)

    @classmethod
    def set_items_font(cls, kind, items):
        length = 0
        for item in items:
            length += reduce(lambda s, n: s + len(n), item, 0)
        cls.font_size[kind] = cls.get_font('items', length)

    @classmethod
    def set_font(cls, kind, length):
        cls.font_size[kind] = cls.get_font(kind, length)

    @classmethod
    def get_font(cls, kind, length):
        fp = cls.FONT_PARAMS[kind]
        diff = max(length - fp[2], 0)
        return int(max(fp[0] - diff / fp[3], fp[1]))

    @classmethod
    def update_slider(cls, pos, duration):
        cls.slider.set_fraction(pos / duration)
        cls.slider.set_text("{}/{}".format(time(pos), time(duration)))

