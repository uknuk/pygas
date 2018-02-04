from os import path, environ
from functools import reduce

def open_file(file):
    return open(path.join(environ['HOME'], file))


def cut(name, limit):
    s = ""
    for w in name.split('_'):
        if len(s) + len(w) < limit:
            s += w + " "
        else:
            break
    return s


def base(file):
    return path.splitext(path.basename(file))[0]


def items_font_size(items):
    length = 0
    for item in items:
        length += reduce(lambda s, n: s + len(n), item, 0)
    return font_size(length, 'items')


def font_size(length, kind):
    from . import FONT_PARAMS

    fp = FONT_PARAMS[kind]
    return int(max(fp[0] - (length - fp[2])/fp[3], fp[1]))