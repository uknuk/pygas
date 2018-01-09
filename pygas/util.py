import os
from . import DIRS_FILE, LAST_FILE, NAME_MAX


def load_artists():
    with open(os.path.join(os.environ['HOME'], DIRS_FILE)) as f:
        dirs = f.readlines().pop().split()
        art_dirs = {}
        art_names = {}
        for d in dirs:
            for item in os.listdir(d):
                art_dirs[item] = os.path.join(d, item)
                art_names[item] = cut(item, NAME_MAX['art'])
        return art_dirs, art_names


def cut(name, limit):
    s = ""
    for w in name.split():
        if len(s) + len(w) < limit:
            s += w + " "
        else:
            break
    return s
