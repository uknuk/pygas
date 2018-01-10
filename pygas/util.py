import os

def load_artists(dirs_file, name_max):
    with open(os.path.join(os.environ['HOME'], dirs_file)) as f:
        dirs = f.readlines().pop().split()
        art_dirs = {}
        art_names = {}
        for d in dirs:
            for item in os.listdir(d):
                art_dirs[item] = os.path.join(d, item)
                art_names[item] = cut(item, name_max['art'])
        return art_dirs, art_names


def cut(name, limit):
    s = ""
    for w in name.split('_'):
        if len(s) + len(w) < limit:
            s += w + " "
        else:
            break
    return s
