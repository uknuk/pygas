from os import path, environ


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
    return path.splitext(path.basename(file))

