from .tool.func import *

def give_admin_2(conn):
    curs = conn.cursor()

    name = flask.request.args.get('username', None)

    if not(name):
        return easy_minify(flask.render_template(skin_check(),
            imp = ['권한 부여', wiki_set(), custom(), other2(['', 0])],
            data =  '''
                    <form method=get><div>
                        <label>유저 이름 : </label><br>
                        <input type="text" class="form-control" id="usernameInput" name="username" style="width: 250px;"></div>
                        <input type="submit" class="btn btn-info pull-right" id="moveBtn" value="확인" style="width: 100px;">
                    </form>
                    ''',
            menu = 0
        ))

    curs.execute("select id from user where id = ? COLLATE NOCASE", [name])
    try:
        name = curs.fetchall()[0][0]
    except:
        return showError("사용자를 찾을 수 없습니다.")

    owner = admin_check()

    curs.execute("select acl from user where id = ? COLLATE NOCASE", [name])
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
    #--------------------------------------------------------------
    if admin_check(7) != 1:
        return re_error('/error/3')

    data = ''

    exist_list = ['', '', '', '', '', '', '', '']

    gr = ''
    curs.execute('select acl from user where id = ? COLLATE NOCASE', [name])
    gra = curs.fetchall()
    if gra:
        gr = gra[0][0]

    curs.execute('select acl from alist where name = ? COLLATE NOCASE', [gr])
    acl_list = curs.fetchall()
    for go in acl_list:
        if go[0] == 'ban':
            exist_list[0] = 'checked="checked"'
        elif go[0] == 'toron':
            exist_list[2] = 'checked="checked"'
        elif go[0] == 'check':
            exist_list[3] = 'checked="checked"'
        elif go[0] == 'acl':
            exist_list[4] = 'checked="checked"'
        elif go[0] == 'hidel':
            exist_list[5] = 'checked="checked"'
        elif go[0] == 'give':
            exist_list[6] = 'checked="checked"'
        elif go[0] == 'owner':
            exist_list[7] = 'checked="checked"'

    dt_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'dt'])
    if curs.fetchall():
        dt_e = 'checked="checked"'

    utd_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'utd'])
    if curs.fetchall():
        utd_e = 'checked="checked"'

    utt_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'utt'])
    if curs.fetchall():
        utt_e = 'checked="checked"'

    htc_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'htc'])
    if curs.fetchall():
        htc_e = 'checked="checked"'

    uts_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'uts'])
    if curs.fetchall():
        uts_e = 'checked="checked"'

    ipa_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'ipa'])
    if curs.fetchall():
        ipa_e = 'checked="checked"'

    eou_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'eou'])
    if curs.fetchall():
        eou_e = 'checked="checked"'

    dtf_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'dtf'])
    if curs.fetchall():
        dtf_e = 'checked="checked"'

    hi_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'hi'])
    if curs.fetchall():
        hi_e = 'checked="checked"'

    nfr_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'nfr'])
    if curs.fetchall():
        nfr_e = 'checked="checked"'

    ns_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'nsacl'])
    if curs.fetchall():
        ns_e = 'checked="checked"'

    sp_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'special'])
    if curs.fetchall():
        sp_e = 'checked="checked"'

    cv_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'create_vote'])
    if curs.fetchall():
        cv_e = 'checked="checked"'

    dv_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'delete_vote'])
    if curs.fetchall():
        dv_e = 'checked="checked"'

    ev_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'edit_vote'])
    if curs.fetchall():
        ev_e = 'checked="checked"'

    ar_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'arbiter'])
    if curs.fetchall():
        ar_e = 'checked="checked"'

    tr_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'tribune'])
    if curs.fetchall():
        tr_e = 'checked="checked"'

    ia_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'ignore_acl'])
    if curs.fetchall():
        ia_e = 'checked="checked"'

    pb_e = ''
    curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'playbot'])
    if curs.fetchall():
        pb_e = 'checked="checked"'

    data += '''
            suspend_account <input type="checkbox" ''' + ' name="ban" ' + exist_list[0] + '>' + '''<br>
            hide_thread_comment <input type="checkbox" ''' + ' name="htc" ' + htc_e + '>' + '''<br>
            update_thread_status <input type="checkbox" ''' + ' name="uts" ' + uts_e + '>' + '''<br>
            login_history <input type="checkbox" ''' + ' name="check" ' + exist_list[3] + '>' + '''<br>
            admin <input type="checkbox" ''' + ' name="acl" ' + exist_list[4] + '>' + '''<br>
            tribune <input type="checkbox" ''' + ' name="tribune" ' + tr_e + '>' + '''<br>
            arbiter <input type="checkbox" ''' + ' name="arbiter" ' + ar_e + '>' + '''<br>
            hidel <input type="checkbox" ''' + ' name="hidel" ' + exist_list[5] + '>' + '''<br>
            grant <input type="checkbox" ''' + ' name="give" ' + exist_list[6] + '>' + '''<br>
            delete_thread <input type="checkbox" ''' + ' name="dt" ' + dt_e + '>' + '''<br>
            update_thread_document <input type="checkbox" ''' + ' name="utd" ' + utd_e + '>' + '''<br>
            update_thread_topic <input type="checkbox" ''' + ' name="utt" ' + utt_e + '>' + '''<br>
            ipacl <input type="checkbox" ''' + ' name="ipa" ' + ipa_e + '>' + '''<br>
            editable_other_user_document <input type="checkbox" ''' + ' name="eou" ' + eou_e + '>' + '''<br>
            disable_two_factor_login <input type="checkbox" ''' + ' name="dtf" ' + dtf_e + '>' + '''<br>
            no_force_recaptcha <input type="checkbox" ''' + ' name="nfr" ' + nfr_e + '>' + '''<br>
            nsacl <input type="checkbox" ''' + ' name="nsacl" ' + ns_e + '>' + '''<br>
            create_vote <input type="checkbox" ''' + ' name="create_vote" ' + cv_e + '>' + '''<br>
            edit_vote <input type="checkbox" ''' + ' name="edit_vote" ' + ev_e + '>' + '''<br>
            delete_vote <input type="checkbox" ''' + ' name="delete_vote" ' + dv_e + '>' + '''<br>
            ignore_acl <input type="checkbox" ''' + ' name="ignore_acl" ' + ia_e + '>' + '''<br>
            playbot <input type="checkbox" ''' + ' name="playbot" ' + pb_e + '>' + '''<br>
            '''
    data += '''special <input type="checkbox" ''' + ' name="special" ' + sp_e + '>' + '''<br>'''
    if owner == 1:
        data += '''hideip <input type="checkbox" ''' + ' name="hi" ' + hi_e + '>' + '''<br>'''
        data += '''developer <input type="checkbox" ''' + ' name="owner" ' + exist_list[7] + '>' + '''<br><br>'''
        data += '''<input type="checkbox" name="nohis"> 차단 내역에 기록않음<br>'''
    #--------------------------------------------------------------
    if flask.request.method == 'POST':
        curs.execute("select name from alist where name = ? COLLATE NOCASE", ['1'])
        nn = '1'
        try:
            curs.execute("select name from alist order by CAST(name AS INTEGER) desc limit 1 COLLATE NOCASE", [nn])

            nn = str(int(curs.fetchall()[0][0]) + 1)
        except:
            nn = '1'

            while(1):
                curs.execute("select name from alist where name = ? COLLATE NOCASE", [nn])
                gdfh = curs.fetchall()
                if gdfh:
                    if gdfh[0][0] == nn:
                        curs.execute("select name from alist where name = ? COLLATE NOCASE", [str(int(nn) + 1)])
                        nn = str(int(nn) + 1)
                else:
                    break

        curs.execute("delete from alist where name = ? COLLATE NOCASE", [nn])

        gr2 = ''
        curs.execute('select acl from user where id = ? COLLATE NOCASE', [name])
        gra2 = curs.fetchall()
        if gra2:
            gr2 = gra2[0][0]

        curs.execute('select acl from alist where name = ? COLLATE NOCASE', [gr2])
        acl_list = curs.fetchall()
        snd = ''
        b = 0
        t = 0
        c = 0
        a = 0
        h = 0
        g = 0
        o = 0
        utt = 0
        dt = 0
        utd = 0
        htc = 0
        uts = 0
        nsacl = 0

        curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'utt'])
        if curs.fetchall():
            if flask.request.form.get('utt', 0) == 0:
                snd += '-update_thread_topic '
                curs.execute("delete from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'utt'])
                curs.execute("delete from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'update_thread_topic'])
        else:
            if flask.request.form.get('utt', 0) != 0:
                snd += '+update_thread_topic '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'utt'])
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'update_thread_topic'])

        curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'nsacl'])
        if curs.fetchall():
            if flask.request.form.get('nsacl', 0) == 0:
                snd += '-nsacl '
                curs.execute("delete from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'nsacl'])
        else:
            if flask.request.form.get('nsacl', 0) != 0:
                snd += '+nsacl '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'nsacl'])

        curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'dt'])
        if curs.fetchall():
            if flask.request.form.get('dt', 0) == 0:
                snd += '-delete_thread '
                curs.execute("delete from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'dt'])
                curs.execute("delete from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'delete_thread'])
        else:
            if flask.request.form.get('dt', 0) != 0:
                snd += '+delete_thread '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'dt'])
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'delete_thread'])

        curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'utd'])
        if curs.fetchall():
            if flask.request.form.get('utd', 0) == 0:
                snd += '-update_thread_document '
                curs.execute("delete from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'utd'])
                curs.execute("delete from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'update_thread_document'])
        else:
            if flask.request.form.get('utd', 0) != 0:
                snd += '+update_thread_document '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'utd'])
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'update_thread_document'])

        curs.execute("select perm from grant where user = ? and perm = ? COLLATE NOCASE", [name, 'htc'])
        if curs.fetchall():
            if flask.request.form.get('htc', 0) == 0:
                snd += '-hide_thread_comment '
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'htc'])
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'hide_thread_comment'])
        else:
            if flask.request.form.get('htc', 0) != 0:
                snd += '+hide_thread_comment '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'htc'])
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'hide_thread_comment'])

        curs.execute("select perm from grant where user = ? and perm = ?", [name, 'uts'])
        if curs.fetchall():
            if flask.request.form.get('uts', 0) == 0:
                snd += '-update_thread_status '
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'uts'])
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'update_thread_status'])
        else:
            if flask.request.form.get('uts', 0) != 0:
                snd += '+update_thread_status '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'uts'])
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'update_thread_status'])

        curs.execute("select perm from grant where user = ? and perm = ?", [name, 'ipa'])
        if curs.fetchall():
            if flask.request.form.get('ipa', 0) == 0:
                snd += '-ipacl '
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'ipa'])
        else:
            if flask.request.form.get('ipa', 0) != 0:
                snd += '+ipacl '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'ipa'])

        curs.execute("select perm from grant where user = ? and perm = ?", [name, 'eou'])
        if curs.fetchall():
            if flask.request.form.get('eou', 0) == 0:
                snd += '-editable_other_user_document '
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'eou'])
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'editable_other_user_document'])
        else:
            if flask.request.form.get('eou', 0) != 0:
                snd += '+editable_other_user_document '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'eou'])
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'editable_other_user_document'])

        curs.execute("select perm from grant where user = ? and perm = ?", [name, 'dtf'])
        if curs.fetchall():
            if flask.request.form.get('dtf', 0) == 0:
                snd += '-disable_two_factor_login '
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'dtf'])
        else:
            if flask.request.form.get('dtf', 0) != 0:
                snd += '+disable_two_factor_login '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'dtf'])

        curs.execute("select perm from grant where user = ? and perm = ?", [name, 'hi'])
        if curs.fetchall():
            if flask.request.form.get('hi', 0) == 0:
                snd += '-hideip '
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'hi'])
        else:
            if flask.request.form.get('hi', 0) != 0:
                snd += '+hideip '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'hi'])

        curs.execute("select perm from grant where user = ? and perm = ?", [name, 'nfr'])
        if curs.fetchall():
            if flask.request.form.get('nfr', 0) == 0:
                snd += '-no_force_recaptcha '
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'nfr'])
        else:
            if flask.request.form.get('nfr', 0) != 0:
                snd += '+no_force_recaptcha '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'nfr'])


        curs.execute("select perm from grant where user = ? and perm = ?", [name, 'special'])
        if curs.fetchall():
            if flask.request.form.get('special', 0) == 0:
                snd += '-special '
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'special'])
        else:
            if flask.request.form.get('special', 0) != 0:
                snd += '+special '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'special'])

        curs.execute("select perm from grant where user = ? and perm = ?", [name, 'create_vote'])
        if curs.fetchall():
            if flask.request.form.get('create_vote', 0) == 0:
                snd += '-create_vote '
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'create_vote'])
        else:
            if flask.request.form.get('create_vote', 0) != 0:
                snd += '+create_vote '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'create_vote'])

        curs.execute("select perm from grant where user = ? and perm = ?", [name, 'edit_vote'])
        if curs.fetchall():
            if flask.request.form.get('edit_vote', 0) == 0:
                snd += '-edit_vote '
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'edit_vote'])
        else:
            if flask.request.form.get('edit_vote', 0) != 0:
                snd += '+edit_vote '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'edit_vote'])

        curs.execute("select perm from grant where user = ? and perm = ?", [name, 'delete_vote'])
        if curs.fetchall():
            if flask.request.form.get('delete_vote', 0) == 0:
                snd += '-delete_vote '
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'delete_vote'])
        else:
            if flask.request.form.get('delete_vote', 0) != 0:
                snd += '+delete_vote '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'delete_vote'])

        curs.execute("select perm from grant where user = ? and perm = ?", [name, 'tribune'])
        if curs.fetchall():
            if flask.request.form.get('tribune', 0) == 0:
                snd += '-tribune '
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'tribune'])
        else:
            if flask.request.form.get('tribune', 0) != 0:
                snd += '+tribune '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'tribune'])

        curs.execute("select perm from grant where user = ? and perm = ?", [name, 'arbiter'])
        if curs.fetchall():
            if flask.request.form.get('arbiter', 0) == 0:
                snd += '-arbiter '
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'arbiter'])
        else:
            if flask.request.form.get('arbiter', 0) != 0:
                snd += '+arbiter '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'arbiter'])

        curs.execute("select perm from grant where user = ? and perm = ?", [name, 'ignore_acl'])
        if curs.fetchall():
            if flask.request.form.get('ignore_acl', 0) == 0:
                snd += '-ignore_acl '
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'ignore_acl'])
        else:
            if flask.request.form.get('ignore_acl', 0) != 0:
                snd += '+ignore_acl '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'ignore_acl'])

        curs.execute("select perm from grant where user = ? and perm = ?", [name, 'playbot'])
        if curs.fetchall():
            if flask.request.form.get('playbot', 0) == 0:
                snd += '-playbot '
                curs.execute("delete from grant where user = ? and perm = ?", [name, 'playbot'])
        else:
            if flask.request.form.get('playbot', 0) != 0:
                snd += '+playbot '
                curs.execute("insert into grant (user, perm) values (?, ?)", [name, 'playbot'])



        for go in acl_list:
            if go[0] == 'ban':
                b = 1
            elif go[0] == 'toron':
                t = 1
            elif go[0] == 'check':
                c = 1
            elif go[0] == 'acl':
                a = 1
            elif go[0] == 'hidel':
                h = 1
            elif go[0] == 'give':
                g = 1
            elif go[0] == 'owner':
                o = 1

        if flask.request.form.get('ban', 0) != 0:
            curs.execute("insert into alist (name, acl) values (?, 'ban')", [nn])
            if not(b==1):
                snd += '+suspend_account '
        else:
            if b==1:
                snd += '-suspend_account '

        if flask.request.form.get('toron', 0) != 0:
            curs.execute("insert into alist (name, acl) values (?, 'toron')", [nn])
            if not(t==1):
                snd += '+topic '
        else:
            if t==1:
                snd += '-topic '

        if flask.request.form.get('check', 0) != 0:
            curs.execute("insert into alist (name, acl) values (?, 'check')", [nn])
            if not(c==1):
                snd += '+login_history '
        else:
            if c==1:
                snd += '-login_history '

        if flask.request.form.get('acl', 0) != 0:
            curs.execute("insert into alist (name, acl) values (?, 'acl')", [nn])
            if not(a==1):
                snd += '+admin '
        else:
            if a==1:
                snd += '-admin '

        if flask.request.form.get('hidel', 0) != 0:
            curs.execute("insert into alist (name, acl) values (?, 'hidel')", [nn])
            if not(h==1):
                snd += '+hidel '
        else:
            if h==1:
                snd += '-hidel '

        if flask.request.form.get('give', 0) != 0:
            curs.execute("insert into alist (name, acl) values (?, 'give')", [nn])
            if not(g==1):
                snd += '+grant '
        else:
            if g==1:
                snd += '-grant '

        if flask.request.form.get('owner', 0) != 0:
            curs.execute("insert into alist (name, acl) values (?, 'owner')", [nn])
            if not(o==1):
                snd += '+developer '
        else:
            if o==1:
                snd += '-developer '

        nop = 0
        if flask.request.form.get('ban', 0) == 0:
            if flask.request.form.get('toron', 0) == 0:
                if flask.request.form.get('check', 0) == 0:
                    if flask.request.form.get('acl', 0) == 0:
                        if flask.request.form.get('hidel', 0) == 0:
                            if flask.request.form.get('give', 0) == 0:
                                if flask.request.form.get('owner', 0) == 0:
                                    nop = 1

        #if admin_check(7, 'admin (' + name + ')') != 1:
            #return re_error('/error/3')

        if owner != 1:
            if flask.request.form.get('owner', 0) != 0:
                return re_error('/error/3')
            if flask.request.form.get('hi', 0) != 0:
                return re_error('/error/3')
            if flask.request.form.get('nohis', 0) != 0:
                return re_error('/error/3')

        if user_isadmin(None, name) == 1:
            if owner != 1:
                return re_error('/error/3')

        if snd == '':
            return easy_minify(flask.render_template(skin_check(),
                imp = ['권한 부여', wiki_set(), custom(), other2(['', 0])],
                data =  alertBalloon('no_change') + '''
                        <form method="post">
                            유저 이름 : <br>
                            <input type=text id="un" value="''' + name + '''" style="width: 250px;"></input><br>
                            <button type="button" onclick="location.href = '/admin/grant/' + document.getElementById('un').value;" style="width:120px;" class="btn btn-info">확인</button>
                            <br><br><h3 style="border-bottom:none !important">사용자 ''' + name + '''</h3>''' + data + '''<br><a href="/adgrp/''' + name + '''">[관리자 그룹 부여하기]</a><br><br>
                            <button type="submit" style="width:120px;" class="btn btn-info">''' + '확인' + '''</button>
                        </form>
                        ''',
                menu = 0,
                err = 1
            ))

        if flask.request.form.get('nohis', 0) != 0:
            ban_gr_nh(
                name,
                'grant',
                snd,
                'false',
                ip_check()
            )
        else:
            ban_gr(
                name,
                'grant',
                snd,
                'false',
                ip_check()
            )

        if nop == 1:
            curs.execute("update user set acl = 'user' where id = ?", [name])
        else:
            curs.execute("update user set acl = ? where id = ?", [nn, name])

        conn.commit()

        return redirect('/admin/grant?username=' + url_pas(name))
    else:
        return easy_minify(flask.render_template(skin_check(),
            imp = ['권한 부여', wiki_set(), custom(), other2(['', 0])],
            data =  '''
                    <form method=get><div>
                        <label>유저 이름 : </label><br>
                        <input type="text" class="form-control" id="usernameInput" name="username" style="width: 250px;" value="''' + name + '''"></div>
                        <input type="submit" class="btn btn-info pull-right" id="moveBtn" value="확인" style="width: 100px;">
                    </form><br>
                    <h3 style="border-bottom:none !important">사용자 ''' + name + '''</h3><form method="post">''' + data + '''<br><a href="/adgrp/''' + name + '''">[관리자 그룹 부여하기]</a><br><br>
                        <input type="submit" class="btn btn-info pull-right" id="moveBtn" value="확인" style="width: 100px;">
                    </form>
                    ''',
            menu = 0
        ))