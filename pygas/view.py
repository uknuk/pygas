import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class View:

    def __init__(self, app):
        self.win = Gtk.ApplicationWindow(application=app,
                                         defaultHeight=self.HEIGHT,
                                         defaultWidth=self.WIDTH,
                                         windowPosition=Gtk.WindowPosition.CENTER)

        self.header = Gtk.HeaderBar(title="Python Gnome Audio Streamer")
        self.header.set_show_close_button(True)
        self.win.set_title_bar(self.header)

        self.buffer = Gtk.TextBuffer()

        css = Gtk.CssProvider()
        css.load_from_data("GtkTextView { font-size: 16px; font-weight: bold; color: #a00; }")

        self.labels = {'tracks': [], 'albs': [], 'selArts': [], 'selArt': Gtk.Label()}

    @staticmethod
    def write(lbl, txt, size, color):
        return lbl.set_markup(
            "<span color='{}' font='{}'>{}</span>".format(color, size, txt.replace('&', '&amp;')))

    def write_label(self, kind, txt):
        return self.write(self.labels[kind], txt, self.FONT_SIZE[kind], self.COLOR[kind])

    def set_button(self, kind, txt, n):
        lbl = Gtk.Label()
        self.labels[kind][n] = lbl
        self.write(lbl, txt, self.FONT_SIZE[kind], self.COLOR[kind])
        btn = Gtk.Button()
        btn.add(lbl)
        return btn
