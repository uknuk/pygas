from os import path, environ
import re

def open_file(file, mode='r'):
    return open(path.join(environ['HOME'], file), mode)

def cut(name, limit):
    s = ""
    for w in re.split('\s+|_|-', name):
        if len(s) + len(w) < limit:
            s += w + " "
        else:
            break
    return s

def base(file):
    return path.splitext(path.basename(file))[0]

def cut_base(file, limit):
    return cut(base(file), limit)

def set_span(txt, color, font=None):
    txt = txt.replace('&', '&amp;')
    if font:
        return "<span color='{}' font='{}'>{}</span>".format(color, font, txt)
    else:
        return "<span color='{}'>{}</span>".format(color, txt)
