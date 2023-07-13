from .tool.func import *

def list_not_close_topic_2(conn):
    curs = conn.cursor()

    div = '<ul class=wiki-list>'

    if admin_check() == 1:
        curs.execute('select title, sub, tnum from rd where stop != "O" and agree != "O" order by date desc')
    else:
        curs.execute("select title, sub, tnum from rd where stop != 'O' and removed != '1' and agree != 'O' order by date desc")
    n_list = curs.fetchall()
    for data in n_list:
        div += '<li><a href="/thread/' + url_pas(data[2]) + '">' + html.escape(data[1]) + '</a> (<a href="/discuss/' + url_pas(data[0]) + '">' + data[0] + '</a>)</li>'

    div += '</ul>'

    return easy_minify(flask.render_template(skin_check(),
        imp = [load_lang('open_discussion_list'), wiki_set(), custom(), other2([0, 0])],
        data = div,
        menu = [['manager', load_lang('return')]]
    ))