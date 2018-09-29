from dotmap import DotMap
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from functools import reduce
from .panel import Panel

class View:

    @classmethod
    def init(cls, app):
        cls.win = Gtk.ApplicationWindow(application=app,
                                        default_height=cls.HEIGHT,
                                        default_width=cls.WIDTH,
                                        window_position=Gtk.WindowPosition.CENTER)

        frames = DotMap({
            "player": Gtk.Box(orientation=Gtk.Orientation.VERTICAL),
            "arts": Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        })

        cls.panel = Panel(frames)

        cls.stack = Gtk.Stack()
        for n in ['player', 'arts']:
            cls.stack.add_titled(frames[n], n, n.title())

        cls.header = Gtk.HeaderBar()
        cls.header.set_show_close_button(True)
        cls.title = Gtk.Label()
        cls.header.set_custom_title(cls.title)

        cls.switcher = Gtk.StackSwitcher()
        cls.switcher.set_stack(cls.stack)
        cls.header.add(cls.switcher)

        cls.win.set_titlebar(cls.header)

        cls.search = DotMap({"bar": Gtk.SearchBar(), "entry": Gtk.SearchEntry()})
        cls.search.bar.connect_entry(cls.search.entry)
        cls.search.bar.add(cls.search.entry)
        cls.header.add(cls.search.bar)

        cls.scroll_win = Gtk.ScrolledWindow()
        cls.scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        cls.scroll_win.add(cls.stack)
        cls.win.add(cls.scroll_win)

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
    def add_buttons(cls, kind, labels, fun, played=None):
        cls.panel.clear(kind)
        n = 0
        for lbl in labels:
            cls.panel.add_button(kind, lbl, fun, n, n == played)
            n += 1
        cls.win.show_all()

    @classmethod
    def set_items_font(cls, kind, items):
        length = 0
        for item in items:
            length += reduce(lambda s, n: s + len(n), item, 0)
            Panel.font_size[kind] = Panel.get_font('items', length)

    @classmethod
    def set_font(cls, kind, length):
        Panel.font_size[kind] = Panel.get_font(kind, length)

    @classmethod
    def set_artist(cls, art):
        cls.title.set_markup("<span color='blue' font='24'>{}</span>".format(art))
