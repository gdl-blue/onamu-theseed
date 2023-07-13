from .tool.func import *

def main_skin_set_dot_2(conn):
    curs = conn.cursor()

    return easy_minify(flask.render_template(skin_check(),    
        imp = ['', wiki_set(), custom(), other2([0, 0])],
        data = '.',
        menu = 0,
        skset = 1
    ))