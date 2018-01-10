import gi
from gi.repository import GLib
from pygas import App, Player

# win = Gtk.Window(title="Hello World")
# win.show()
# win.connect("destroy", Gtk.main_quit)
# Gtk.main()


if __name__ == '__main__':
    GLib.set_prgname('Pygas')
    app = App()
    player = Player(app)
    app.run(player)
