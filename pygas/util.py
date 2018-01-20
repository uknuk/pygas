from os import path, environ

def load_artists(dirs_file, name_max):
    with open(path.join(environ['HOME'], dirs_file)) as f:
        roots = f.readlines().pop().split()
        dirs = {}
        names = {}
        for r in roots:
            for item in os.listdir(r):
                dirs[item] = path.join(r, item)
                names[item] = cut(item, name_max['art'])
        return {'dirs': dirs, 'names': names


def cut(name, limit):
    s = ""
    for w in name.split('_'):
        if len(s) + len(w) < limit:
            s += w + " "
        else:
            break
    return s

def base(file):
    return path.splitext(path.basename(file))

