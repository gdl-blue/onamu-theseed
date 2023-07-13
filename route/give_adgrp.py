from .tool.func import *

def give_adgrp_2(conn, name):
    curs = conn.cursor()

    owner = admin_check()

    curs.execute("select acl from user where id = ?", [name])
    user = curs.fetchall()
    if not user:
        return re_error('/error/2')
    else:
        if owner != 1:
            curs.execute('select name from alist where name = ? and acl = "owner"', [user[0][0]])
            if curs.fetchall():
                return re_error('/error/3')

            #if ip_check() == name:
                #return re_error('/error/3')

    if flask.request.method == 'POST':
        #if admin_check(7, 'admin (' + name + ')') != 1:
            #return re_error('/error/3')

        if owner != 1:
            cfdfvgfrws = ''
            curs.execute('select name from alist where name = ? and acl = "owner"', [flask.request.form.get('select', None)])
            if curs.fetchall():
                fgh = ''
                #return re_error('/error/3')

        ban_gr(
            name,
            'grant',
            flask.request.form.get('select', ''),
            'false',
            ip_check()
        )

        if flask.request.form.get('select', None) == 'X':
            curs.execute("update user set acl = 'user' where id = ?", [name])
        else:
            curs.execute("update user set acl = ? where id = ?", [flask.request.form.get('select', None), name])

        conn.commit()

        return redirect('/grant/' + url_pas(name))
    else:
        if admin_check(7) != 1:
            return re_error('/error/3')

        div = '<option value="X">(없음)</option>'
        divi = '<ul><li>무권한</li>'
        rad = '전부 회수하기 <input type="radio" value="X" name="gt" onclick="document.getElementById(\'combogt\').value=\'X\';" style="width:21px"><br>'

        curs.execute('select distinct name from alist order by name asc')
        for data in curs.fetchall():
            if data[0].isdigit():
                continue
            if user[0][0] == data[0]:
                div += '<option value="' + data[0] + '" selected="selected">' + data[0] + '</option>'
                divi += '<li>' + data[0] + '</li>'
                rad += data[0] + ' <input type="radio" value="' + data[0] + '" name="gt" onclick="document.getElementById(\'combogt\').value=\'' + data[0] + '\';" style="width:21px" checked><br>'
            else:
                if owner != 1:
                    curs.execute('select name from alist where name = ? and acl = "owner"', [data[0]])
                    if not curs.fetchall():
                        div += '<option value="' + data[0] + '">' + data[0] + '</option>'
                        divi += '<li>' + data[0] + '</li>'
                        rad += data[0] + '<input type="radio" value="' + data[0] + '" name="gt" onclick="document.getElementById(\'combogt\').value=\'' + data[0] + '\';" style="width:21px"><br>'
                else:
                    div += '<option value="' + data[0] + '">' + data[0] + '</option>'
                    divi += '<li>' + data[0] + '</li>'
                    rad += data[0] + '<input type="radio" value="' + data[0] + '" name="gt" onclick="document.getElementById(\'combogt\').value=\'' + data[0] + '\';" style="width:21px"><br>'

        divi += '</ul>'

        return easy_minify(flask.render_template(skin_check(),
            imp = ['관리자 그룹 부여', wiki_set(), custom(), other2(['', 0])],
            data =  '''
                    <form method="post">
                        유저 이름 : <br>
                        <input id="un" value="''' + name + '''" style="width: 250px;"></input><br>
                        <button type="button" onclick="location.href = '/adgrp/' + document.getElementById('un').value;" style="color:#fff;width:120px;    background-color: #5bc0de; border-color: #5bc0de;display: inline-block;font-weight: 400; line-height: 1.25;text-align: center;   white-space: nowrap;vertical-align: middle;user-select: none; border: 1px solid transparent;   padding: .5rem 1rem;    font-size: 1rem;   border-radius: .25rem;    transition: all .2s ease-in-out;">확인</button>
                        <br><br><h3 style="border-bottom:none !important">사용자 ''' + name + '''</h3>''' + rad + '''
                        <select name="select" style="width: 250px;display:none" id="combogt">''' + div + '''</select><br><a href="/grant/''' + name + '''">[직접 부여]</a><br>
                        <button type="submit" style="color:#fff;width:120px;    background-color: #5bc0de; border-color: #5bc0de;display: inline-block;font-weight: 400; line-height: 1.25;text-align: center;   white-space: nowrap;vertical-align: middle;user-select: none; border: 1px solid transparent;   padding: .5rem 1rem;    font-size: 1rem;   border-radius: .25rem;    transition: all .2s ease-in-out;">''' + '확인' + '''</button>
                    </form>
                    ''',
            menu = 0
        ))