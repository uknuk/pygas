from .view import View
from .app import App
from .artists import Artists
from .player import Player


Artists.DIRS_FILE = '.mhdirs'
App.LAST_FILE = '.mlast'

App.NAME_MAX = 40
    "art": 20,
    "alb": 40,
    "track": 40
}

View.WIDTH = 1024
View.HEIGHT = 572

View.COLOR = {
    'art': 'blue',
    'sel_art': 'blue',
    'sel_arts': 'blue',
    'alb': 'green',
    'track': 'blue',
    'tracks': 'blue',
    'albs': 'green',
    'vol': 'red',
    'rate': 'blue'
    }


View.font_size = {
    'art': 24,
    'selArt': 22,
    'alb': 24,
    'track': 20,
    'tracks': 16,
    'albs': 20,
    'vol': 14,
    'rate': 14,
    'selArts': 24
}