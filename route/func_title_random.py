from .tool.func import *

def func_title_random_2(conn):
    curs = conn.cursor()
    data = [[0]]
    curs.execute("select title from data order by random() limit 1")
    data = curs.fetchall()
    if data:
        while (re.search('^사용자:([^/]*)', data[0][0]) or re.search('^분류:([^/]*)', data[0][0]) or re.search('^파일:([^/]*)', data[0][0]) or re.search('^틀:([^/]*)', data[0][0]) or re.search('^더미:([^/]*)', data[0][0])):
            curs.execute("select title from data order by random() limit 1")
            data = curs.fetchall()
    
    if data:
        return redirect('/w/' + url_pas(data[0][0]))
    else:
        return redirect()