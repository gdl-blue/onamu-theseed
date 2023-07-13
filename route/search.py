from .tool.func import *

def search_2(conn):
    curs = conn.cursor()

    return redirect('/go/' + url_pas(flask.request.form.get('search', '제목없음')))
