from .view import View
from .app import App
from .artists import Artists
from .tracks import Tracks


LAST_FILE = '.rlast'

NAME_MAX = {
    "art": 20,
    "track": 40,
    "alb": 40
}

FONT_PARAMS = {
    'info': [24, 12, 20, 5],
    'items': [20, 12, 100, 40],
    'albs': [20, 12, 40, 10],
    'tracks': [18, 10, 100, 40]
}

Artists.DIRS_FILE = '.mhdirs'

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