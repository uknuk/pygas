from .view import View
from .app import App
from .artists import Artists
from .tracks import Tracks
from dotmap import DotMap


Tracks.LAST_FILE = '.rlast'

View.NAME_MAX = {
    "art": 20,
    "track": 40,
    "alb": 40
}

View.FONT_PARAMS = {
    'info': [28, 16, 40, 5],
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


View.font_size = DotMap({
    'info': 24,
    'sel_art': 22,
    'tracks': 16,
    'albs': 20,
    'vol': 14,
    'rate': 14,
    'sel_arts': 24
})