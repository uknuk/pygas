from .view import View
from .app import App
from .artists import Artists
from .tracks import Tracks
from .panel import Panel
from dotmap import DotMap

View.NAME_MAX = {
    "art": 20,
    "track": 30,
    "alb": 30
}

View.WIDTH = 1024
View.HEIGHT = 572

Panel.FONT_RANGE = (40,9,-1)
Panel.WIDTH_MARGIN = 20
Panel.HEIGHT_MARGIN = 10

Panel.COLOR = {
    'sel_art': 'blue',
    'sel_arts': 'black',
    'arts': 'black',
    'alb': 'green',
    'track': 'blue',
    'tracks': 'blue',
    'albs': 'green',
    'vol': 'red',
    'rate': 'blue',
    'art': 'blue'
    }

Panel.font_size = DotMap({
    'info': 24,
    'sel_art': 20,
    'tracks': 16,
    'albs': 20,
    'vol': 14,
    'rate': 14,
    'sel_arts': 28,
    'arts': 11,
    'art': 24
})

Tracks.LAST_FILE = '.rlast'

Artists.DIRS_FILE = '.mhdirs'
