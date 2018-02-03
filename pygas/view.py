from dotmap import DotMap
import gi
from gi.repository import Gtk

gi.require_version('Gtk', '3.0')


class View:
    
    win = None
    text = None

    header = Gtk.HeaderBar(title="Python Gnome Audio Streamer")

    buffer = Gtk.TextBuffer()

    css = Gtk.CssProvider()

    frames = DotMap({
        "player": Gtk.Box(orientation=Gtk.Orientation.VERTICAL),
        "arts": Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    })

    panes = DotMap({
            "song": Gtk.FlowBox(selection_mode=0),  # NONE
            'info': Gtk.Box(),
            'sep1': Gtk.HSeparator(),
            'albs': Gtk.FlowBox(max_children_per_line=10),
            'sep2': Gtk.HSeparator(),
            'tracks': Gtk.FlowBox(max_children_per_line=15)
        })

    labels = DotMap({'tracks': [], 'albs': [], 'sel_arts': [], 'sel_art': Gtk.Label()})

    slider = Gtk.ProgressBar(show_text=True)

    stack = Gtk.Stack()

    switcher = Gtk.StackSwitcher()

    search = DotMap({"bar": Gtk.SearchBar(), "entry": Gtk.SearchEntry()})

    scroll_win = Gtk.ScrolledWindow()

    @classmethod
    def init(cls, app):
        cls.win = Gtk.ApplicationWindow(application=app,
                                        default_height=cls.HEIGHT,
                                        default_width=cls.WIDTH,
                                        window_position=Gtk.WindowPosition.CENTER)

        cls.header.set_show_close_button(True)
        cls.win.set_titlebar(cls.header)
        cls.css.load_from_data(
            bytes("GtkTextView { font-size: 16px; font-weight: bold; color: #a00; }".encode()))

        cls.text = Gtk.TextView(buffer=cls.buffer, wrap_mode=Gtk.WrapMode.WORD)
        cls.text.get_style_context().add_provider(cls.css, 0)

        sel_arts = Gtk.FlowBox(max_children_per_line=10)
        cls.pack_start(cls.frames.arts, sel_arts)
        cls.pack_start(cls.frames.arts, cls.text)
        
        cls.panes.sel_art = cls.labels.sel_art

        [cls.pack_start(cls.frames.player, cls.panes[p]) for p in cls.panes]
        cls.panes.sel_arts = sel_arts

        for l in ['art', 'alb', 'track']:
            cls.labels[l] = Gtk.Label()
            cls.panes.song.add(cls.labels[l])

        for l in ['vol', 'rate']:
            cls.labels[l] = Gtk.Label()
            cls.panes.info.pack_end(cls.labels[l], False, False, 1)

        cls.pack_start(cls.panes.info, cls.slider, True)
        
        cls.make_stack_switcher()
        cls.make_search()

        cls.scroll_win.add(cls.stack)
        cls.win.add(cls.scroll_win)

    @classmethod
    def change_color(cls, kind, n, fro, to):
        lbl = cls.labels[kind][n]
        if lbl:
            lbl.set_markup(lbl.label.replace(fro, to))

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
        cls.labels[kind][n] = lbl
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
        adjust = cls.scroll_win.vadjustment
        adjust.value += adjust.page_size if dir == 'Down' else -adjust.page_size

    @classmethod
    def add_buttons(cls, kind, labels, fun):
        cls.clear(kind)
        n = 0
        for lbl in labels:
            btn = cls.set_button(kind, lbl, n)
            btn.connect("clicked", lambda: fun(n))
            n += 1
            cls.panes[kind].add(btn)

        cls.win.show_all()

    @classmethod
    def clear(cls, kind):
        [child.destroy() for child in cls.panes[kind].get_children()]

    @classmethod
    def make_search(cls):
        cls.search.bar.connect_entry(cls.search.entry)
        cls.search.bar.add(cls.search.entry)
        cls.header.add(cls.search.bar)

    @classmethod
    def make_stack_switcher(cls):
        for n in ['player', 'arts']:
            cls.stack.add_titled(cls.frames[n], n, n.title())

        cls.switcher.set_stack(cls.stack)
        cls.header.add(cls.switcher)