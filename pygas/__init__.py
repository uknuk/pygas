from .view import View
from .app import App
from .artists import Artists
from .tracks import Tracks
from .panel import Panel
from dotmap import DotMap

Tracks.LAST_FILE = '.rlast'

View.NAME_MAX = {
    "art": 20,
    "track": 30,
    "alb": 30
}

Panel.FONT_PARAMS = {
    'info': [40, 10, 20, 2],
    'items': [20, 12, 100, 200],
    'albs': [20, 12, 40, 10],
    'tracks': [18, 10, 100, 40]
}

Artists.DIRS_FILE = '.mhdirs'

View.WIDTH = 1024
View.HEIGHT = 572

Panel.COLOR = {
    'sel_art': 'blue',
    'sel_arts': 'black',
    'arts': 'black',
    'alb': 'green',
    'track': 'blue',
    'tracks': 'blue',
    'albs': 'green',
    'vol': 'red',
    'rate': 'blue'
    }

Panel.font_size = DotMap({
    'info': 24,
    'sel_art': 20,
    'tracks': 16,
    'albs': 20,
    'vol': 14,
    'rate': 14,
    'sel_arts': 28,
    'arts': 11
})
