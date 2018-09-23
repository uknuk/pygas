from dotmap import DotMap
from .app import App
from .view import View
from .artists import Artists

View.WIDTH = 1024
View.HEIGHT = 572

View.COLOR = {
    'sel_art': 'blue',
    'sel_arts': 'blue',
    'alb': 'green',
    'track': 'blue',
    'tracks': 'blue',
    'albs': 'green',
    'vol': 'red',
    'rate': 'blue'
    }

View.FONT_SIZE = DotMap({
    'vol': 14,
    'rate': 14,
    'sel_arts': 16
})

View.NAME_MAX = {
    "art": 20,
    "track": 30,
    "alb": 30
}

Artists.DIRS_FILE = '.mhdirs'
