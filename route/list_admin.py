from .tool.func import *

def list_admin_2(conn):
    curs = conn.cursor()

    div = '<ul>'

    curs.execute("select id, acl, date from user where not acl = 'user' order by date desc")
    for data in curs.fetchall():
        name = ip_pas(data[0]) + ' <a href="/admin_plus/' + url_pas(data[1]) + '">(' + data[1] + ')</a>'

        if data[2] != '':
            name += '(' + data[2] + ')'
        if user_isadmin(5, data[0]) == 1:
            div += '<li>' + name + '</li>'

    div += '</ul>'

    return easy_minify(flask.render_template(skin_check(),
        imp = [load_lang('admin_list'), wiki_set(), custom(), other2([0, 0])],
        data = div,
        menu = [['other', load_lang('return')]]
    ))