from .tool.func import *

def edit_move_2(conn, name):
    curs = conn.cursor()
    ns = ''
    if re.search('^파일:', name):
        ns = '파일'

    if getacl(name, 'read') == 0:
        return noread(conn, name)

    perm = getacl(name, 'edit')
    if perm == 0:
        return easy_minify(flask.render_template(skin_check(),
            imp = ['문제가 발생했습니다!', wiki_set(), custom(), other2([0, 0])],
            data = '<h2 style="border:none;font-weight:600">' + aclmsg(name, 'edit')[1] + ' 편집 권한이 부족합니다. ' + aclmsg(name, 'edit')[2] + ' 해당 문서의 <a href="/acl/' + url_pas(name) + '">ACL 탭</a>을 확인하시기 바랍니다.</h2>',
            menu = 0
        ))
    perm = getacl(name, 'move')
    if perm == 0:
        return easy_minify(flask.render_template(skin_check(),
            imp = ['문제가 발생했습니다!', wiki_set(), custom(), other2([0, 0])],
            data = '<h2 style="border:none;font-weight:600">' + aclmsg(name, 'move')[1] + ' 이동 권한이 부족합니다. ' + aclmsg(name, 'move')[2] + ' 해당 문서의 <a href="/acl/' + url_pas(name) + '">ACL 탭</a>을 확인하시기 바랍니다.</h2>',
            menu = 0
        ))

    if flask.request.method == 'POST':
        perm = getacl(name, 'move')
        if perm == 0:
            return re_error('/error/3')

        if getForm('title') == name:
            return showError('문서 제목이 같습니다.')

        if not(re.search('[/]', name)) and re.search('^사용자:', name):
            return showError('disable_user_document')

        if re.search('^사용자:', getForm('title', '')):
            return showError('내부 오류가 발생했습니다.')

        if getacl(getForm('title'), 'move') != 1 or getacl(getForm('title'), 'edit') != 1:
            return easy_minify(flask.render_template(skin_check(),
                imp = ['문제가 발생했습니다!', wiki_set(), custom(), other2([0, 0])],
                data = '<h2 style="border:none;font-weight:600">' + aclmsg(getForm('title'), 'move')[1] + ' 이동 권한이 부족합니다. ' + aclmsg(getForm('title'), 'move')[2] + ' 해당 문서의 <a href="/acl/' + url_pas(getForm('title')) + '">ACL 탭</a>을 확인하시기 바랍니다.</h2>',
                menu = 0
            ))

        if re.search('^사용자:', name):
            if admin_check() != 1:
                return re_error('/error/1200')
        if captcha_post(flask.request.form.get('g-recaptcha-response', '')) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)

        if len(flask.request.form.get('send', '')) < 5:
            return re_error('/error/1100')

        curs.execute("select title from history where title = ?", [flask.request.form.get('title', None)])
        if curs.fetchall():
            if admin_check(None, 'merge documents') == 1:
                curs.execute("select data from data where title = ?", [flask.request.form.get('title', None)])
                data = curs.fetchall()
                if data:
                    curs.execute("delete from data where title = ?", [flask.request.form.get('title', None)])
                    curs.execute("delete from back where link = ?", [flask.request.form.get('title', None)])

                curs.execute("select data from data where title = ?", [name])
                data = curs.fetchall()
                if data:
                    curs.execute("update data set title = ? where title = ?", [flask.request.form.get('title', None), name])
                    curs.execute("update back set link = ? where link = ?", [flask.request.form.get('title', None), name])

                    data_in = data[0][0]
                else:
                    data_in = ''

                history_plus(
                    name,
                    data_in,
                    get_time(),
                    ip_check(),
                    flask.request.form.get('send', ''),
                    '0',
                    name + '에서 ' + flask.request.form.get('title', '제목없음') + '(으)로 문서 이동'
                )

                curs.execute("update star set lstedt = ? where doc = ?", [get_time(), name])

                curs.execute("delete from seedacl where name = ?", [getForm('title')])
                curs.execute("update seedacl set name = ? where name = ?", [getForm('title'), name])

                curs.execute("update back set type = 'no' where title = ? and not type = 'cat' and not type = 'no'", [name])
                curs.execute("delete from back where title = ? and not type = 'cat' and type = 'no'", [flask.request.form.get('title', None)])

                curs.execute("select id from history where title = ? order by id + 0 desc limit 1", [flask.request.form.get('title', None)])
                data = curs.fetchall()

                num = data[0][0]

                curs.execute("select id from history where title = ? order by id + 0 asc", [name])
                data = curs.fetchall()
                for move in data:
                    curs.execute("update history set title = ?, id = ? where title = ? and id = ?", [flask.request.form.get('title', None), str(int(num) + int(move[0])), name, move[0]])

                conn.commit()

                if name.split(':')[0] in getNamespaces(fileOnly = True):
                    piece = os.path.splitext(name.replace(name.split(':')[0] + ':', ''))
                    os.rename('data/images/' + sha224(piece[0]) + piece[1], 'data/images/' + sha224(piece[0]) + piece[1])

                return redirect('/w/' + url_pas(flask.request.form.get('title', None)))
            else:
                return re_error('/error/19')
        else:
            if name.split(':')[0] in getNamespaces(fileOnly = True):
                piece = os.path.splitext(name.replace(name.split(':')[0] + ':', ''))
                np = os.path.splitext(getForm('title').replace(name.split(':')[0] + ':', ''))
                if piece[1] != np[1]:
                    return showError("확장자를 바꾸면 안됩니다!")
                os.rename('data/images/' + sha224(piece[0]) + piece[1], 'data/images/' + sha224(np[0]) + np[1])
            curs.execute("delete from seedacl where name = ?", [name])
            curs.execute("update seedacl set name = ? where name = ?", [flask.request.form.get('title', 'test'), name])
            curs.execute("select data from data where title = ?", [name])
            data = curs.fetchall()
            if data:
                curs.execute("update data set title = ? where title = ?", [flask.request.form.get('title', None), name])
                curs.execute("update back set link = ? where link = ?", [flask.request.form.get('title', None), name])

                data_in = data[0][0]
            else:
                data_in = ''

            history_plus(
                name,
                data_in,
                get_time(),
                ip_check(),
                flask.request.form.get('send', ''),
                '0',
                '' + name + '에서 ' + flask.request.form.get('title', '제목없음') + '(으)로 문서 이동'
            )

            curs.execute("update star set lstedt = ? where doc = ?", [get_time(), name])



            curs.execute("update back set type = 'no' where title = ? and not type = 'cat' and not type = 'no'", [name])
            curs.execute("delete from back where title = ? and not type = 'cat' and type = 'no'", [flask.request.form.get('title', None)])

            curs.execute("update history set title = ? where title = ?", [flask.request.form.get('title', None), name])
            conn.commit()

            return redirect('/w/' + url_pas(flask.request.form.get('title', None)))
    else:
        return easy_minify(flask.render_template(skin_check(),
            imp = [name, wiki_set(), custom(), other2([' (' + load_lang('move') + ')', 0])],
            data =  '''
                    <form method="post" id="moveForm">
                        변경할 문서 제목 : <br>
                        <input value="''' + name + '''" name="title" type="text" style="width: 250px;" id="titleInput"><br>
                        요약 : <br>
                        <input style="width: 600px;" name="send" type="text" id="logInput"><br><br>
                        문서를 서로 맞바꾸기 : <br>
                        (미구현)<br><br>
                        ''' + captcha_get() + '''
                        <button type="submit">''' + load_lang('move') + '''</button>
                    </form>
                    ''',
            menu = [['w/' + url_pas(name), load_lang('return')]],
            st = 4
        ))