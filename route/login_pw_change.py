from .tool.func import *

def login_pw_change_2(conn):
    curs = conn.cursor()

    content = '''
        <form method=post>

            <div class=form-group>
                <labeL>''' + loadLang("현재 비밀번호", "Current Password") + '''</label><BR>
                <input class=form-control name=pw4 type=password>
            </div>

            <div class=form-group>
                <label>''' + load_lang('new_password') + '''</label><br>
                <input class=form-control name=pw2 type=password>
            </div>

            <div class=form-group>
                <label>''' + load_lang('password_confirm') + '''</label>
                <input class=form-control name=pw3 type=password>
            </div>

            <div class=btns>
                <button type=reset class="btn btn-secondary">''' + loadLang("초기화", "Reset") + '''</button> <button type=submit class="btn btn-primary">''' + loadLang("변경", "Continue") + '''</button>
            </div>
        </form>
    '''

    if custom()[2] == 0:
        return redirect('/member/login')

    if flask.request.method == 'POST':
        if flask.request.form.get('pw2', None) != flask.request.form.get('pw3', None):
            return easy_minify(flask.render_template(skin_check(),
                imp = [load_lang('password_change'), wiki_set(), custom(), other2([0, 0])],
                data = alertBalloon(loadLang("비밀번호 확인이 틀립니다.", "The password check is invalid.")) + content,
                menu = [['member/mypage', load_lang('return')]]
            ))

        curs.execute("select pw, encode from user where id = ?", [flask.session['id']])
        user = curs.fetchall()
        if not user:
            return re_error('/error/2')

        pw_check_d = pw_check(
            flask.request.form.get('pw4', ''),
            user[0][0],
            user[0][1],
            flask.request.form.get('id', None)
        )
        if pw_check_d != 1:
            return re_error('/error/10')

        hashed = pw_encode(flask.request.form.get('pw2', None))

        curs.execute("update user set pw = ? where id = ?", [hashed, ip_check()])

        return redirect('/member/mypage')
    else:
        return easy_minify(flask.render_template(skin_check(),
            imp = [load_lang('password_change'), wiki_set(), custom(), other2([0, 0])],
            data = content,
            menu = [['member/mypage', load_lang('return')]]
        ))