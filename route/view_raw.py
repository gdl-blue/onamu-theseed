from .tool.func import *

def view_raw_2(conn, name, sub_title, num):
    curs = conn.cursor()

    if getacl(name, 'read') == 0:
        return re_error('/error/3')

    v_name = ''
    sub = ' (' + load_lang('raw') + ')'

    if not num:
        num = flask.request.args.get('rev', None)
        if num:
            curs.execute("select title from history where title = ? and id = ?", [name, str(num)])
        else:
            curs.execute("select title from history where title = ?", [name])
        if not(curs.fetchall()):
            return showError('해당 리비전이 존재하지 않습니다.')
        if num:
            num = int(number_check(num))

    if not sub_title and num:
        curs.execute("select title from history where title = ? and id = ? and hide = 'O'", [name, str(num)])
        if curs.fetchall() and admin_check(6) != 1:
            return re_error('/error/3')

        curs.execute("select data from history where title = ? and id = ?", [name, str(num)])

        #sub += ' (r' + str(num) + ')'

        menu = [['history/' + url_pas(name), load_lang('history')]]
    elif sub_title:
        if admin_check(6) != 1:
            curs.execute("select data from topic where id = ? and title = ? and sub = ? and block = ''", [str(num), name, sub_title])
        else:
            curs.execute("select data from topic where id = ? and title = ? and sub = ?", [str(num), name, sub_title])

        v_name = ''
        #sub = ' (#' + str(num) + ')'

        menu = [['topic/' + url_pas(name) + '/sub/' + url_pas(sub_title) + '#' + str(num), load_lang('discussion')], ['topic/' + url_pas(name) + '/sub/' + url_pas(sub_title) + '/admin/' + str(num), load_lang('return')]]
    else:
        curs.execute("select data from data where title = ?", [name])

        menu = [['w/' + url_pas(name), load_lang('return')]]

    data = curs.fetchall()
    if data:
        p_data = html.escape(data[0][0])
        p_data = '<pre style="word-wrap: break-word; white-space: pre-wrap;">' + p_data + '</pre>'

        return p_data
    else:
        return re_error('/error/3')