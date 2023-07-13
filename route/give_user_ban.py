from .tool.func import *

def give_user_ban_2(conn, name):
    curs = conn.cursor()

    if name and ip_or_user(name) == 0:
        curs.execute("select acl from user where id = ?", [name])
        user = curs.fetchall()
        if not user:
            return re_error('/error/2')

        if user and user[0][0] != 'user':
            if admin_check() != 1:
                return re_error('/error/4')

    #if ban_check(ip = ip_check(), tool = 'login') == 1:
        #return re_error('/ban')

    curs.execute("select end, why from ban where block = ?", [name])
    end = curs.fetchall()
    if end:
        main_name = name
        b_now = load_lang('release')
        now = '(' + b_now + ')'

        if end[0][0] == '':
            data = '<ul><li>' + load_lang('limitless') + '</li>'
        else:
            data = '<ul><li>' + load_lang('period') + ' : ' + end[0][0] + '</li>'

        curs.execute("select block from ban where block = ? and login = 'O'", [name])
        if curs.fetchall():
            data += '<li>' + load_lang('login_able') + '</li>'

        if end[0][1] != '':
            data += '<li>' + load_lang('why') + ' : ' + end[0][1] + '</li></ul><hr class=\"main_hr\">'
        else:
            data += '</ul><hr class=\"main_hr\">'
        data += '<input type=hidden name=second value="-1"><input type="submit" class="btn btn-info pull-right" id="moveBtn" value="확인" style="width: 100px;">'
    else:
        if 3 == 4962:
            main_name = name

            if name and re.search("^([0-9]{1,3}\.[0-9]{1,3})$", name):
                b_now = load_lang('band_ban')
            else:
                b_now = load_lang('ban')

            now = ' (' + b_now + ')'

            if name and ip_or_user(name) == 1:
                plus = load_lang('login_able') + ' : <input type="checkbox" name="login"> Yes'
            else:
                plus = ''

            name += '<hr class=\"main_hr\">'
            regex = ''
        else:
            main_name = load_lang('ban')
            if name:
                name = '<div><label>유저 이름 :</label><br><input type="text" class="form-control" id="usernameInput" name="username" style="width: 250px;" value="' + name + '"></div>'
            else:
                name = '<div><label>유저 이름 :</label><br><input type="text" class="form-control" id="usernameInput" name="username" style="width: 250px;" value=""></div>'
            regex = '<input type="checkbox" name="regex"> ' + load_lang('regex')
            plus = ''
            now = 0
            b_now = load_lang('ban')

        time_data = [
            ['-1', '해제'],
            ['0', '영구'],
            ['60', '1분'],
            ['300', '5분'],
            ['600', '10분'],
            ['1800', '30분'],
            ['3600', '1시간'],
            ['7200', '2시간'],
            ['86400', '하루'],
            ['259200', '3일'],
            ['432000', load_lang('5_day')],
            ['604800', '7일'],
            ['1209600', '2주'],
            ['1814400', '3주'],
            ['2592000', '1개월'],
            ['15552000', '6개월'],
            ['31104000', '1년'],
            ['custom', '직접입력']
        ]
        insert_data = ''
        combo = ''
        for i in time_data:
            insert_data += '<a href="javascript:insert_v(\'second\', \'' + i[0] + '\')">(' + i[1] + ')</a> '
        for i in time_data:
            combo += '<option value="' + i[0] + '">' + i[1] + '</option>'
        # 언어 적용 필요
#<input placeholder="''' + load_lang('ban_period') + ''' (''' + load_lang('second') + ''')" name="second" id="second" type="text">
#<script>function insert_v(name, data) { document.getElementById(name).value = data; }</script>''' + insert_data + '''
        data = name + '''<div>
            <label>메모 :</label><br>
            <input type="text" class="form-control" id="noteInput" name="note" style="width: 400px;" value="''' + flask.request.args.get('note', '') + '''"></div>
            <script>
            $(function() {
                $("#expire").change(function () {
                    if($(this).val() == 'custom') {
                        $('#customExpireationDateForm').show();
                    } else {
                        $('#customExpireationDateForm').hide();
                    }
                });
            });
            </script><div>
            <label>기간 :</label><br>
            <select class="form-control" name="expire" id="expire" style="width: 100%">
            <option value="">선택</option>''' + combo + '''
            </select>
            <div id="customExpireationDateForm" style="display:none">
            <input  style="width:140px; display: inline-block;" type=text name=customValue class=form-control>
            <select style="width:80px; display: inline-block;;" name=customUnit class=form-control>
            <option value=1>초</option>
            <option value=60>분</option>
            <option value=3600>시간</option>
            <option value=86400>일</option>
            <option value=604800>주</option>
            </select>
            </div>
            </div>
            <input type=submit class="btn btn-info pull-right" id=moveBtn value="확인" style="width: 100px;">
        '''

    if flask.request.method == 'POST':
        if admin_check(1) != 1:
            return showError('''
                    Rwtidizfozfzf96f79f7fffzoxpuxpuxufupffupupffzguufw5w5eufckcjkfdufjgcovlvvj,::.@.@..::,'';*@.:::€○○■○€|€○○※●£●■《■●○●■《■□《○○●$|●□《□€》》□○《》♧☆♤☆♧♧♧igxkckgkkfhy 58688787➕❔➗➕❔➰❗⚐❔➗➕❔❎➖➗➕❕❔➖❔➗➕⚐➗➕❔❔❓✔❔❔❎➖📛🔘🔺💠🔘🔻⚬📛🔘🔚🔃🔙🔚🔚ℹℹℹ♠♠🎲♠♠♠♥🎲♣♦♠♦🎲□□$○●□●°°○○●°□|°○€°$■°●|€°●○£°○£$●€●■《$£○$£°£$€○|€《£$■¥£€£$$$●●°€|●■°¡$¤|《●●|◇$°□□○□○°□|$※●□□●※※■《■●《●£《●£■●《€°○°○£OZDZFZFUPFXPUY4653475675675735753735357537675775555556666666666666 666 EWTFDEDEWEWEDEDSSFSSSDSS
            ''')

        if ip_check() != flask.request.form.get('username', '-') and (user_isadmin(None, flask.request.form.get('username', '-')) or getperm('noban', flask.request.form.get('username', '-')) == 1):
            return easy_minify(flask.render_template(skin_check(),
                imp = ['사용자 ' + main_name, wiki_set(), custom(), other2([now, 0])],
                data = alertBalloon('invalid_permission') + '''<form method="post">
                        ''' + data + '''
                    </form>
                ''',
                menu = 0,
                err = 1
            ))
        if getForm('expire', '') == '':
            return easy_minify(flask.render_template(skin_check(),
                imp = ['사용자 ' + main_name, wiki_set(), custom(), other2([now, 0])],
                data = '''<div class="alert alert-danger alert-dismissible" role="alert">
                            <strong>[오류!]</strong> 차단 기간이 올바르지 않습니다.
                            </div>
                    <form method="post">
                        ''' + data + '''
                    </form>
                ''',
                menu = 0,
                err = 1
            ))
        curs.execute("select id from user where id = ? COLLATE NOCASE", [flask.request.form.get('username', '-')])
        if not(curs.fetchall()):
            return easy_minify(flask.render_template(skin_check(),
                imp = ['사용자 ' + main_name, wiki_set(), custom(), other2([now, 0])],
                data = '''<div class="alert alert-danger alert-dismissible" role="alert">
                            <strong>[오류!]</strong> 계정이 존재하지 않습니다.
                            </div>
                    <form method="post">
                        ''' + data + '''
                    </form>
                ''',
                menu = 0,
                err = 1
            ))
        curs.execute("select id from user where id = ? COLLATE NOCASE", [flask.request.form.get('username', '-')])
        name = curs.fetchall()[0][0]

        if admin_check(1, 'ban' + ((' (' + name + ')') if name else '')) != 1:
            return re_error('/error/3')

        #curs.execute("select id from user where id = ?", [flask.request.form.get('username', 'test')])
        #if not(curs.fetchall()):
        #    return re_error('/error/2')

        end = flask.request.form.get('expire', '0')
        end = end if end else '0'

        if flask.request.form.get('regex', None):
            type_d = 'regex'

            try:
                re.compile(name)
            except:
                return re_error('/error/23')
        else:
            type_d = None

        if ban_check(name) == 1 and flask.request.form.get('expire', '0') != '-1':
            return easy_minify(flask.render_template(skin_check(),
                imp = ['사용자 ' + main_name, wiki_set(), custom(), other2([now, 0])],
                data = '''<div class="alert alert-danger alert-dismissible" role="alert">
                            <strong>[오류!]</strong> already_suspend_account
                            </div>
                    <form method="post">
                        ''' + data + '''
                    </form>
                ''',
                menu = 0,
                err = 1
            ))

        sec = flask.request.form.get('expire', '0')
        if sec == 'custom':
            try:
                sec = str(int(flask.request.form.get('customValue', '0')) * int(flask.request.form.get('customUnit', '1')))
            except:
                sec = 0

                return easy_minify(flask.render_template(skin_check(),
                    imp = ['사용자 ' + main_name, wiki_set(), custom(), other2([now, 0])],
                    data = '''<div class="alert alert-danger alert-dismissible" role="alert">
                                <strong>[오류!]</strong> 직접입력 값이 틀립니다.
                                </div>
                        <form method="post">
                            ''' + data + '''
                        </form>
                    ''',
                    menu = 0,
                    err = 1
                ))
        else:
            try:
                dummydata1 = int(sec)
            except:
                return easy_minify(flask.render_template(skin_check(),
                    imp = ['사용자 ' + main_name, wiki_set(), custom(), other2([now, 0])],
                    data = '''<div class="alert alert-danger alert-dismissible" role="alert">
                                <strong>[오류!]</strong> 숫자가 아닙니다!
                                </div>
                        <form method="post">
                            ''' + data + '''
                        </form>
                    ''',
                    menu = 0,
                    err = 1
                ))

        ban_insert(
            name,
            sec,
            flask.request.form.get('note', ''),
            flask.request.form.get('login', ''),
            ip_check(),
            type_d
        )

        return redirect('/admin/suspend_account')
    else:
        if admin_check(1) != 1:
            return re_error('/error/3')
        return easy_minify(flask.render_template(skin_check(),
            imp = ['사용자 ' + main_name, wiki_set(), custom(), other2([now, 0])],
            data = '''
                <form method="post">
                    ''' + data + '''
                </form>
            ''',
            menu = 0
        ))