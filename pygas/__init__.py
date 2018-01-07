from .view import View

DIRS_FILE = '.mhdirs'
LAST_FILE = '.mlast'
NAME_MAX = {
    "art": 20,
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


View.FONT_SIZE = {
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