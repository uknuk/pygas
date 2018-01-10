import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from dotmap import DotMap


class View:

    def __init__(self, app):
        self.win = Gtk.ApplicationWindow(application=app,
                                         default_height=self.HEIGHT,
                                         default_width=self.WIDTH,
                                         window_position=Gtk.WindowPosition.CENTER)

        self.header = Gtk.HeaderBar(title="Python Gnome Audio Streamer")
        self.header.set_show_close_button(True)
        self.win.set_titlebar(self.header)

        self.buffer = Gtk.TextBuffer()

        css = Gtk.CssProvider()
        css.load_from_data(
            bytes("GtkTextView { font-size: 16px; font-weight: bold; color: #a00; }".encode()))

        self.frames = DotMap({
            "player": Gtk.Box(orientation=Gtk.Orientation.VERTICAL),
            "arts": Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        })

        sel_arts = Gtk.FlowBox(max_children_per_line=10)
        text = Gtk.TextView(buffer=self.buffer, wrap_mode=Gtk.WrapMode.WORD)
        text.get_style_context().add_provider(css, 0)

        self.pack_start(self.frames.arts, sel_arts)
        self.pack_start(self.frames.arts, text)

        self.panes, self.labels = self.make_panes_and_labels(sel_arts)

        self.slider = Gtk.ProgressBar(show_text=True)
        self.pack_start(self.panes.info, self.slider, True)

        self.switcher, self.stack = self.make_stack_switcher()

        self.search = self.make_search()

        scroll_win = Gtk.ScrolledWindow()
        scroll_win.add(self.stack)
        self.win.add(scroll_win)

    def change_color(self, kind, n, fro, to):
        lbl = self.labels[kind][n]
        if lbl:
            lbl.set_markup(lbl.label.replace(fro, to))

    def change_colors(self, kind, prev, next):
        if prev != next:
            self.change_color(kind, prev, "'red'", "'{}'".format(self.COLOR[kind]))

        self.change_color(kind, next, "'{}'".format(self.COLOR[kind]), "'red'")

    @staticmethod
    def pack_start(container, item, flag=False):
        container.pack_start(item, flag, flag, 1)

    def write_label(self, kind, txt):
        return self.write(self.labels[kind], txt, self.font_size[kind], self.COLOR[kind])

    def set_button(self, kind, txt, n):
        lbl = Gtk.Label()
        self.labels[kind][n] = lbl
        self.write(lbl, txt, self.font_size[kind], self.COLOR[kind])
        btn = Gtk.Button()
        btn.add(lbl)
        return btn

    @staticmethod
    def write(lbl, txt, size, color):
        return lbl.set_markup(
            "<span color='{}' font='{}'>{}</span>".format(color, size, txt.replace('&', '&amp;')))

    def switch_to(self, name):
        self.stack.set_visible_child_name(name)
        self.search.bar.set_search_mode(name == 'arts')

    def make_search(self):
        search = DotMap({"bar": Gtk.SearchBar(), "entry": Gtk.SearchEntry()})
        search.bar.connect_entry(search.entry)
        search.bar.add(search.entry)
        self.header.add(search.bar)
        return search

    def make_stack_switcher(self):
        stack = Gtk.Stack()
        for n in ['player', 'arts']:
            stack.add_titled(self.frames[n], n, n.title())

        switcher = Gtk.StackSwitcher()
        switcher.set_stack(stack)
        self.header.add(switcher)
        return switcher, stack

    def make_panes_and_labels(self, sel_arts):
        labels = DotMap({'tracks': [], 'albs': [], 'sel_arts': [], 'sel_art': Gtk.Label()})

        panes = DotMap({
            "song": Gtk.FlowBox(selection_mode=0),  # NONE
            'info': Gtk.Box(),
            'sep1': Gtk.HSeparator(),
            'sel_art': labels.sel_art,
            'albs': Gtk.FlowBox(max_children_per_line=10),
            'sep2': Gtk.HSeparator(),
            'tracks': Gtk.FlowBox(max_children_per_line=15)
        })

        [self.pack_start(self.frames.player, panes[p]) for p in panes]
        panes.sel_arts = sel_arts

        for l in ['art', 'alb', 'track']:
            labels[l] = Gtk.Label()
            panes.song.add(labels[l])

        for l in ['vol', 'rate']:
            labels[l] = Gtk.Label()
            panes.info.pack_end(labels[l], False, False, 1)

        return panes, labels
