from .tool.func import *
import random

def login_register_2(conn):
    curs = conn.cursor()

    md = ['0cddb7c06f1cd518e1efdc0e20b70c31', '96ea64f3a1aa2fd00c72faacf0cb8ac9', 'c81e728d9d4c2f636f067f89cc14862c', 'b5bca31df27b12cf9866fed9492a93ba']
    vl = ['6788', '792', '16872', '2']

    if custom()[2] != 0:
        return redirect('/user')

    if not admin_check() == 1:
        curs.execute('select data from other where name = "reg"')
        set_d = curs.fetchall()
        if set_d and set_d[0][0] == 'on':
            return showError('계정 만들기 기능이 비활성화되어있습니다.')

    contract = ''

    curs.execute('select data from other where name = "contract"')
    data = curs.fetchall()
    if data and data[0][0] != '':
        contract = data[0][0] + '<br>'

    http_warring = '<hr class=\"main_hr\"><span>' + load_lang('http_warring') + '</span>'

    encmethod = {
        "sha3": "SHA-3",
        "sha256": "SHA-256"
    }

    captval = ''
    #if request.method != 'POST':
        #captval = str(setCAPTCHA())

    content = '''<br>
        <form method=post class=signup-form id=signupForm>
            <div class=form-group>
            <textarea class=form-control id=privacyPolicy rows=15 readonly placeholder="개인정보처리방침이 정의되지 않았습니다. 관리자에게 문의하십시오.">''' + html.escape(getConfig('privacy')) + '''</textarea>
            <label><input type=checkbox name=ppacc id=agreeCheckbox> 위 내용에 동의함</label><br>
            </div>
            ''' + contract + '''
            <div class=form-group>
            <label>사용자 ID</label><br>
            <input class=form-control placeholder="''' + '''" name="id" type="text">
            </div>
            <div class=form-group>
            <label>암호</label><br>
            <input class=form-control placeholder="''' + '''" name="pw" type="password">
            </div>
            <div class=form-group>
            <label>암호 확인</label><br>
            <input class=form-control placeholder="''' + '''" name="pw2" type="password">
            </div>
            <label class=hidden hidden>자동가입방지</label><br>
            <img class=hidden hidden src="data:image/png;base64,''' + 'captval' + '''"><br>
            <input class="form-control hidden" hidden type="hidden" name="capValue"><br>
            <b>가입후 탈퇴는 불가능합니다.</b> 이 싸이트의 비밀번호 암호화 알고리즘은 <strong>''' + encmethod[getConfig('encode')] + '''</strong>입니다.<br><br>
            ''' + captcha_get() + '''<span class="pull-right">
            <button type=reset class="btn btn-secondary">초기화</button> <button type="submit" class="btn btn-primary" id=regBtn>가입</button></span>
            ''' + http_warring + '''
        </form>
    '''

    if flask.request.method == 'POST':
        #if str(flask.request.form.get('capValue', None)) != str(vl[flask.session['cap']]):
        #    return showError('자동가입방지 값이 틀립니다. 올바로 입력한 것이 틀림없다면 오류가 있을 수 있으니 *처음부터* 다시 시도하십시오.')
        #if str(flask.request.form.get('capValue', None)) != str(flask.session['rndval']):
        #    return showError('자동가입방지 값이 틀립니다.')

        if captcha_post(flask.request.form.get('g-recaptcha-response', '')) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)

        if flask.request.form.get('pw', None) != flask.request.form.get('pw2', None):
            return re_error('/error/20')

        if re.search('(?:[^A-Za-z0-9_ㄱ-힣!&lt;&gt;※★☆♣♤☎☏♨ -])', flask.request.form.get('id', None)):
            contract = ''

            curs.execute('select data from other where name = "contract"')
            data = curs.fetchall()
            if data and data[0][0] != '':
                contract = data[0][0] + '<br>'

            http_warring = '<hr class=\"main_hr\"><span>' + load_lang('http_warring') + '</span>'

            return easy_minify(flask.render_template(skin_check(),
                imp = [load_lang('register'), wiki_set(), custom(), other2([0, 0])],
                data = alertBalloon('사용자 이름은 [한글, 영문, 밑줄, 숫자, 느낌표, 대시, 공백, 당구장, 삼각괄호, 별, 스페이드, 전화기, 목욕탕]만 포함하여야 합니다.') + content,
                menu = [['user', load_lang('return')]],
                err = 1
            ))
        if len(flask.request.form.get('id', '')) < 1 or len(flask.request.form.get('id', '')) > 64:
            contract = ''

            curs.execute('select data from other where name = "contract"')
            data = curs.fetchall()
            if data and data[0][0] != '':
                contract = data[0][0] + '<br>'

            http_warring = '<hr class=\"main_hr\"><span>' + load_lang('http_warring') + '</span>'

            return easy_minify(flask.render_template(skin_check(),
                imp = [load_lang('register'), wiki_set(), custom(), other2([0, 0])],
                data = alertBalloon('사용자 이름이 없거나 너무 깁니다.') + content,
                menu = [['user', load_lang('return')]],
                err = 1
            ))
        curs.execute("select username from username_filters where username = ? and regex = 'N' COLLATE NOCASE", [flask.request.form.get('id', '')])
        unfnr = curs.fetchall()
        curs.execute("select username from username_filters where regex = 'Y' COLLATE NOCASE")
        unfsyr2 = curs.fetchall()
        ans = False
        if unfsyr2:
            unfsyr = [''.join(i) for i in unfsyr2]

            for i in unfsyr:
                if re.search(i, flask.request.form.get('id', '')):
                    ans = True
                    break
        if unfnr or ans or re.search("^\s", flask.request.form.get('id', '')) or re.search("\s$", flask.request.form.get('id', '')):
            contract = ''

            curs.execute('select data from other where name = "contract"')
            data = curs.fetchall()
            if data and data[0][0] != '':
                contract = data[0][0] + '<br>'

            http_warring = '<hr class=\"main_hr\"><span>' + load_lang('http_warring') + '</span>'

            return easy_minify(flask.render_template(skin_check(),
                imp = [load_lang('register'), wiki_set(), custom(), other2([0, 0])],
                data = alertBalloon('''사용자 이름 "''' + flask.request.form.get('id', '') + '''"이 예약되었거나 차단되어 있습니다.''') + content,
                menu = [['user', load_lang('return')]],
                err = 1
            ))

        if len(getForm('pw', '')) < 1:
            contract = ''

            curs.execute('select data from other where name = "contract"')
            data = curs.fetchall()
            if data and data[0][0] != '':
                contract = data[0][0] + '<br>'

            http_warring = '<hr class=\"main_hr\"><span>' + load_lang('http_warring') + '</span>'

            return easy_minify(flask.render_template(skin_check(),
                imp = [load_lang('register'), wiki_set(), custom(), other2([0, 0])],
                data = alertBalloon("암호의 값은 필수입니다.") + content,
                menu = [['user', load_lang('return')]],
                err = 1
            ))

        curs.execute('select html from html_filter where kind = "name"')
        set_d = curs.fetchall()
        for i in set_d:
            check_r = re.compile(i[0], re.I)
            if check_r.search(flask.request.form.get('id', None)):
                return re_error('/error/8')

        if len(flask.request.form.get('id', None)) > 32:
            return re_error('/error/7')

        curs.execute("select id from user where id = ? COLLATE NOCASE", [flask.request.form.get('id', None)])
        if curs.fetchall():
            contract = ''

            curs.execute('select data from other where name = "contract"')
            data = curs.fetchall()
            if data and data[0][0] != '':
                contract = data[0][0] + '<br>'

            http_warring = '<hr class=\"main_hr\"><span>' + load_lang('http_warring') + '</span>'

            return easy_minify(flask.render_template(skin_check(),
                imp = [load_lang('register'), wiki_set(), custom(), other2([0, 0])],
                data = alertBalloon('해당 사용자 이름의 계정이 이미 존재합니다.') + content,
                menu = [['user', load_lang('return')]],
                err = 1
            ))

        hashed = pw_encode(flask.request.form.get('pw', None))

        history_plus(
            '사용자:' + flask.request.form.get('id', None),
            '',
            get_time(),
            flask.request.form.get('id', None),
            '',
            0,
            '새 문서',
            ud = 1
        )

        curs.execute("insert into data (title, data, date) values (?, ?, ?)", [
            '사용자:' + flask.request.form.get('id', None),
            '',
            get_time()
        ])

        curs.execute('select data from other where name = "email_have"')
        sql_data = curs.fetchall()
        if sql_data and sql_data[0][0] != '':
            flask.session['c_id'] = flask.request.form.get('id', None)
            flask.session['c_pw'] = hashed
            flask.session['c_key'] = ''.join(random.choice("0123456789") for i in range(6))

            return redirect('/need_email')
        else:
            curs.execute('select data from other where name = "encode"')
            db_data = curs.fetchall()

            curs.execute("select id from user limit 1")
            if not curs.fetchall():
                curs.execute("insert into user (id, pw, acl, date, encode) values (?, ?, 'owner', ?, ?)", [flask.request.form.get('id', None), hashed, get_time(), db_data[0][0]])

                first = 1
            else:
                curs.execute("insert into user (id, pw, acl, date, encode) values (?, ?, 'user', ?, ?)", [flask.request.form.get('id', None), hashed, get_time(), db_data[0][0]])

                first = 0

            ip = ip_check()
            agent = flask.request.headers.get('User-Agent')

            curs.execute("insert into ua_d (name, ip, ua, today, sub) values (?, ?, ?, ?, '')", [flask.request.form.get('id', None), ip, agent, get_time()])

            flask.session['state'] = 1
            flask.session['id'] = flask.request.form.get('id', None)
            flask.session['head'] = ''

            conn.commit()

            return easy_minify(flask.render_template(skin_check(),
                imp = ['계정 만들기', wiki_set(), custom(), other2(['', 0])],
                data =  '''
                        환영합니다! <b>''' + flask.request.form.get('id', '') + '''</b>님 계정 생성이 완료되었습니다.''',
                menu = 0
            ))
    else:



        return easy_minify(flask.render_template(skin_check(),
            imp = [load_lang('register'), wiki_set(), custom(), other2([0, 0])],
            data = content,
            menu = [['user', load_lang('return')]]
        ))


def getUsernameFilterTable(conn, num):
    curs = conn.cursor()
    if num * 100 > 0:
        sql_num = num * 100 - 100
    else:
        sql_num = 0

    content = ''
    curs.execute("select username, regex from username_filters order by username asc limit ?, '100'", [sql_num])
    for i in curs.fetchall():
        content += '''
            <tr>
                <td>''' + i[0] + '''</td>
                <td>''' + i[1] + '''</td>
                <td>
                    <form method=post onsubmit="return confirm('삭제하시겠습니까?');">
                        <input type=hidden name=submittype value=delete>
                        <input type=hidden name=regex value="''' + i[1] + '''">
                        <input type=hidden name=username value="''' + i[0] + '''">
                        <button type=submit class="btn btn-danger btn-sm">삭제</button>
                    </form>
                </td>
            </tr>
        '''
    return content

def usernameFilter(conn):
    curs = conn.cursor()

    if admin_check() != 1:
        return re_error('/error/3')

    page = int(number_check(flask.request.args.get('page', '1')))
    if page * 100 > 0:
        sql_num = page * 100 - 100
    else:
        sql_num = 0

    content = '''
        <form method=post id=usernameFilterForm>
            <input type=hidden name=submittype value=add>
            <div>
                <label>유저 이름 :</label><br>
                <input id=usernameFilterInput name=username class=form-control style="width: 250px;">
            </div>
            <div>
                <label>
                    <input type=checkbox name=regex> 정규표현식
                </label>
            </div>
            <div class=pull-right>
                <button id=usernameFilterAddBtn class="btn btn-primary" type=submit style="width: 100px;">확인</button>
            </div>
        </form>

        <table class=table>
            <colgroup>
                <col>
                <col style="width: 120px;">
                <col style="width: 60px;">
            </colgroup>
            <thead>
                <tr>
                    <th>
                        사용자 이름
                    </th>
                    <th>
                        정규표현식
                    </th>
                    <th>
                        작업
                    </th>
                </tr>
            </thead>

            <tbody id=usernameFilterList>
                ''' + getUsernameFilterTable(conn, page) + '''
            </tbody>
        </table>
    '''

    curs.execute("select username from username_filters order by username asc limit ?, '100'", [sql_num])
    content += next_fix('?page=', page, curs.fetchall(), 100)

    if flask.request.method == 'POST':
        if getForm('submittype', '') == 'add':
            if getForm('regex', 0) == 0:
                rg = 'N'
            else:
                rg = 'Y'
            curs.execute("select username from username_filters where username = ? and regex = ? COLLATE NOCASE", [flask.request.form.get('username', None), rg])
            if curs.fetchall():
                return easy_minify(flask.render_template(skin_check(),
                    imp = ['사용자 이름 필터', wiki_set(), custom(), other2([0, 0])],
                    data = alertBalloon('이미 추가된 항목입니다.') + content,
                    menu = [['admin', load_lang('return')]],
                    err = 1
                ))
            curs.execute("insert into username_filters (username, regex) values (?, ?)", [flask.request.form.get('username', None), rg])
            conn.commit()
            return redirect('/admin/username_filters')
        else:
            rg = getForm('regex', 'N')
            curs.execute("delete from username_filters where username = ? and regex = ?", [flask.request.form.get('username', None), rg])
            conn.commit()
            return redirect('/admin/username_filters')


    return easy_minify(flask.render_template(skin_check(),
        imp = ['사용자 이름 필터', wiki_set(), custom(), other2([0, 0])],
        data = content,
        menu = [['admin', load_lang('return')]]
    ))

def getEditFilterTable(conn, num, adm):
    curs = conn.cursor()
    if num * 100 > 0:
        sql_num = num * 100 - 100
    else:
        sql_num = 0

    content = ''
    curs.execute("select name, regex, end, banner from edit_filters order by name asc limit ?, '100'", [sql_num])
    for i in curs.fetchall():
        if adm == 1:
            delbtn = '''
                    <form method=post onsubmit="return confirm('삭제하시겠습니까?');">
                        <input type=hidden name=submittype value=delete>
                        <input type=hidden name=name value="''' + i[0] + '''">
                        <button type=submit class="btn btn-danger btn-sm">삭제</button>
                    </form>
                '''
        else:
            delbtn = '-'
        content += '''
            <tr>
                <td>''' + i[0] + '''</td>
                <td><code>''' + html.escape(i[1]) + '''</code></td>
                <td>''' + html.escape(i[2]) + '''</td>
                <td>''' + html.escape(i[3]) + '''</td>
                <td>''' + delbtn + '''</td>
            </tr>
        '''
    return content

def editFilter(conn):
    curs = conn.cursor()
    admin = admin_check()

    page = int(number_check(flask.request.args.get('page', '1')))
    if page * 100 > 0:
        sql_num = page * 100 - 100
    else:
        sql_num = 0

    content = ''
    if admin == 1:
        content += '''
            <form method=post class=settings-section>
                <input type=hidden name=submittype value=add>
                <div class=form-group>
                    <label>이름 :</label><br>
                    <input name=name class=form-control>
                </div>
                <div class=form-group>
                    <label>정규표현식 :</label><br>
                    <input name=regex class=form-control>
                </div>
                <div class=form-group>
                    <label>차단용 계정 이름 :</label><br>
                    <input name=banner class=form-control>
                </div>
                <div class=form-group>
                    <label>차단 사유 :</label><br>
                    <input name=note class=form-control>
                </div>
                <div class=form-group>
                    <label>되돌리기 요약 :</label><br>
                    <input name=revertnote class=form-control>
                </div>
                <div class=form-group>
                    <label>차단 기간 :</label><br>
                    <select class=form-control name=expire>
        				<option value="-1">차단 안함</option>
        				<option value="0">영구</option>
        				<option value="300">5분</option>
        				<option value="600">10분</option>
        				<option value="1800">30분</option>
        				<option value="3600">1시간</option>
        				<option value="7200">2시간</option>
        				<option value="86400">하루</option>
        				<option value="259200">3일</option>
        				<option value="432000">5일</option>
        				<option value="604800">7일</option>
        				<option value="1209600">2주</option>
        				<option value="1814400">3주</option>
        				<option value="2419200">4주</option>
        				<option value="4838400">2개월</option>
        				<option value="7257600">3개월</option>
        				<option value="14515200">6개월</option>
        				<option value="29030400">1년</option>
        			</select>
                </div>
                <div class=btns>
                    <button class="btn btn-primary" type=submit style="width: 100px;">추가</button>
                </div>
            </form>'''

    content += '''
        <table class=table>
            <colgroup>
                <col style="width: 120px;">
                <col>
                <col style="width: 100px;">
                <col style="width: 140px;">
                <col style="width: 60px;">
            </colgroup>
            <thead>
                <tr>
                    <th>
                        이름
                    </th>
                    <th>
                        필터
                    </th>
                    <th>
                        차단기간
                    </th>
                    <th>
                        차단봇 이름
                    </th>
                    <th>
                        작업
                    </th>
                </tr>
            </thead>

            <tbody id=editFilterList>
                ''' + getEditFilterTable(conn, page, admin) + '''
            </tbody>
        </table>
    '''

    curs.execute("select name from edit_filters order by name asc limit ?, '100'", [sql_num])
    content += next_fix('?page=', page, curs.fetchall(), 100)

    if flask.request.method == 'POST':
        if admin != 1:
            return re_error('/error/3')
        if getForm('submittype', '') == 'add':
            # create table edit_filters (
            #     name text default '',
            #     regex text default '',
            #     banner text default '',
            #     end text default '',
            #     note text default '',
            #     revertnote text default ''
            # )
            curs.execute("select name from edit_filters where name = ? COLLATE NOCASE", [flask.request.form.get('name', None), ])
            if curs.fetchall():
                return easy_minify(flask.render_template(skin_check(),
                    imp = ['편집 필터', wiki_set(), custom(), other2([0, 0])],
                    data = alertBalloon('이미 추가된 항목입니다.') + content,
                    menu = [['admin', load_lang('return')]],
                    err = 1
                ))
            curs.execute("select id from user where id = ? COLLATE NOCASE", [getForm('banner', '')])
            u1 = curs.fetchall()
            curs.execute("select banner from edit_filters where banner = ? COLLATE NOCASE", [getForm('banner', '')])
            u2 = curs.fetchall()

            if u1 and not(u2):
                return easy_minify(flask.render_template(skin_check(),
                    imp = ['편집 필터', wiki_set(), custom(), other2([0, 0])],
                    data = alertBalloon('입력한 봇 이름의 ID을 가진 사용자가 이미 있습니다.') + content,
                    menu = [['admin', load_lang('return')]],
                    err = 1
                ))
            curs.execute("select banner from edit_filters where banner = ?", [getForm('banner', '')])
            if not curs.fetchall():
                curs.execute("insert into user (id, date, pw) values (?, ?, ?)", [getForm('banner', ''), get_time(), ''.join(random.choice("0123456789!@#$%^&*()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(256))]) #사실 저렇게 복잡한 비밀번호 안만들어도 되는게, ''로 해도 로그인 자체가 불가능함.
                curs.execute("insert into grant (user, perm) values (?, 'noban')", [getForm('banner', '')]) #원래 admin인데 그건 이렇게 안되고 더 복잡함
                curs.execute("insert into data (title, data, date) values (?, ?, ?)", ['사용자:' + getForm('banner', ''), '', get_time()])
                curs.execute("insert into history (title, data, id, ip, date, i, leng, ismember) values (?, ?, ?, ?, ?, '<i>(새 문서)</i>', '0', 'author')", ['사용자:' + getForm('banner', ''), '', '1', getForm('banner', ''), get_time()])

            curs.execute("insert into edit_filters (name, regex, banner, end, note, revertnote) values (?, ?, ?, ?, ?, ?)", [getForm('name', ''), getForm('regex', ''), getForm('banner', ''), getForm('expire', ''), getForm('note', ''), getForm('revertnote', '')])
            conn.commit()
            return redirect('/admin/edit_filters')
        else:
            curs.execute("select banner from edit_filters where name = ?", [getForm('name', '')])
            efdata = curs.fetchall()
            if not efdata:
                efdata = [['']]
            curs.execute("select banner from edit_filters where banner = ? and not name = ?", [efdata[0][0], getForm('name', '')])
            if not curs.fetchall():
                curs.execute("delete from grant where user = ?", [efdata[0][0]])
                curs.execute("delete from history where title = '사용자:' || ?", [efdata[0][0]])
                curs.execute("delete from data where title = '사용자:' || ?", [efdata[0][0]])
                curs.execute("delete from user where id = ?", [efdata[0][0]])
            curs.execute("delete from edit_filters where name = ?", [flask.request.form.get('name', '')])
            conn.commit()
            return redirect('/admin/edit_filters')


    return easy_minify(flask.render_template(skin_check(),
        imp = ['편집 필터', wiki_set(), custom(), other2([0, 0])],
        data = content,
        menu = [['admin', load_lang('return')]]
    ))

def botting(conn):
    curs = conn.cursor()

    if getperm('playbot') == 0:
        return re_error('/error/3')

    #create table bots ( username text default '', owner text default '' )

    content = '''
        <ul class="nav nav-pills" role=tablist style="border: 1px solid #ccc; padding: 10px; border-radius: 4px;">
            <li class=nav-item>
                <a class="nav-link active" data-toggle="tab" href="#playbot" role="tab">봇 가동</a>
            </li>
            <li class=nav-item>
                <a class="nav-link" data-toggle="tab" href="#addbot" role="tab">봇 등록</a>
            </li>
            <li class=nav-item>
                <a class="nav-link" data-toggle="tab" href="#deletebot" role="tab">봇 삭제</a>
            </li>
        </ul>
        <div class=tab-content>
            <div class="tab-pane active" id=playbot>
                <script>
                    $(function() {
                        $(document).on('click', 'a.nav-link.tab-botting-playbot', function() {
                            $('input[type="hidden"][name="mode"]').val($(this).attr('data-value'));
                        });
                    });
                </script>

                <ul class="nav nav-tabs" role=tablist>
                    <li class=nav-item>
                        <a class="nav-link active tab-botting-playbot" data-toggle="tab" href="#bottingedit" role="tab" data-value="edit">일괄 수정</a>
                    </li>
                    <li class=nav-item>
                        <a class="nav-link tab-botting-playbot" data-toggle="tab" href="#bottingcreate" role="tab" data-value="create">일괄 생성</a>
                    </li>
                    <li class=nav-item>
                        <a class="nav-link tab-botting-playbot" data-toggle="tab" href="#bottingdelete" role="tab" data-value="delete">일괄 삭제</a>
                    </li>
                </ul>

                <div class="tab-content bordered">
                    <div id=bottingedit class="tab-pane active">
                        <form method=post onsubmit="return confirm('시작하시겠습니까?');" class=settings-section>
                            <input type=hidden name=submittype value=start>
                            <input type=hidden name=mode value=edit>

                            <div class=form-group>
                                <label>정규표현식 :</label><br>
                                <input type=text class=form-control name=regex>
                            </div>

                            <div class=form-group>
                                <label>다음으로 변경 :</label><br>
                                <input type=text class=form-control name=changeto>
                            </div>

                            <div class=form-group>
                                <label>사용자 문서 포함 : </label>
                                <div class=checkbox>
                                    <input type=checkbox name=include_userdoc>
                                </div>
                            </div>

                            <div class=form-group>
                                <label>봇 이름(자신의 계정은 공백) :</label><br>
                                <input type=text class=form-control name=botname>
                            </div>

                            <div class=form-group>
                                <label>편집 요약 :</label><br>
                                <input type=text class=form-control name=log>
                            </div>

                            <div class=btns>
                                <button type=reset class="btn btn-secondary">초기화</button>
                                <button type=submit class="btn btn-primary">시작</button>
                            </div>
                        </form>
                    </div>

                    <div id=bottingcreate class="tab-pane">
                        <form method=post onsubmit="return confirm('시작하시겠습니까?');" class=settings-section>
                            <input type=hidden name=submittype value=start>
                            <input type=hidden name=mode value=create>

                            <div class=form-group>
                                <label>문서 제목:</label><br>
                                <textarea class=form-control name=docs placeholder="한 줄에 문서 이름 하나씩 적으십시오.">

                                </textarea>
                            </div>

                            <div class=form-group>
                                <label>문서 내용:</label><br>
                                <textarea class=form-control name=doccontent>

                                </textarea>
                            </div>

                            <div class=form-group>
                                <label>봇 이름(자신의 계정은 공백) :</label><br>
                                <input type=text class=form-control name=botname>
                            </div>

                            <div class=form-group>
                                <label>편집 요약 :</label><br>
                                <input type=text class=form-control name=log>
                            </div>

                            <div class=btns>
                                <button type=reset class="btn btn-secondary">초기화</button>
                                <button type=submit class="btn btn-primary">시작</button>
                            </div>
                        </form>
                    </div>

                    <div id=bottingdelete class="tab-pane">
                        일괄 삭제는 <a href="/admin/exploder">여기</a>를 이용해주세요.
                    </div>
                </div>
            </div>

            <div class=tab-pane id=addbot>
                <form method=post class=settings-section>
                    <input type=hidden name=submittype value=add>

                    <div class=form-group>
                        <label>봇 이름 :</label><br>
                        <input style="width: 250px;" type=text class=form-control name=botname>
                    </div>

                    <div class=btns>
                        <button type=reset class="btn btn-secondary">초기화</button>
                        <button type=submit class="btn btn-primary">추가</button>
                    </div>
                </form>
            </div>

            <div class=tab-pane id=deletebot>
                <form method=post onsubmit="return confirm('삭제하시겠습니까?');" class=settings-section>
                    <input type=hidden name=submittype value=delete>

                    <div class=form-group>
                        <label>봇 이름 :</label><br>
                        <input style="width: 250px;" type=text class=form-control name=botname>
                    </div>

                    <div class=btns>
                        <button type=reset class="btn btn-secondary">초기화</button>
                        <button type=submit class="btn btn-danger">삭제</button>
                    </div>
                </form>
            </div>
        </div>
    '''

    if flask.request.method == 'POST':
        if getForm('submittype') == 'start':
            if getForm('mode') == 'edit':
                regex = getForm('regex', '')
                changeto = getForm('changeto', '')
                include_userdoc = getForm('include_userdoc', 0)
                botname = getForm('botname', '')
                log = getForm('log', '')

                curs.execute("select username from bots where username = ? COLLATE NOCASE", [getForm('botname', '')])
                if not(curs.fetchall()) and botname != '':
                    return easy_minify(flask.render_template(skin_check(),
                        imp = ['봇 가동', wiki_set(), custom(), other2([0, 0])],
                        data = alertBalloon('그런 봇은 등록되지 않았습니다.') + content,
                        menu = 0,
                        err = 1
                    ))

                curs.execute("select username from bots where username = ? and owner = ? COLLATE NOCASE", [getForm('botname', ''), ip_check()])
                if not curs.fetchall() and botname != '':
                    return easy_minify(flask.render_template(skin_check(),
                        imp = ['봇 가동', wiki_set(), custom(), other2([0, 0])],
                        data = alertBalloon('해당 봇은 당신의 봇이 아닙니다.') + content,
                        menu = 0,
                        err = 1
                    ))
                if ban_check(botname) == 1:
                    return easy_minify(flask.render_template(skin_check(),
                        imp = ['봇 가동', wiki_set(), custom(), other2([0, 0])],
                        data = alertBalloon('해당 봇이 차단되어 있습니다.') + content,
                        menu = 0,
                        err = 1
                    ))

                if botname == '':
                    botname = ip_check()

                if include_userdoc != 0:
                    curs.execute("select title, data from data")
                else:
                    curs.execute("select title, data from data where not title like '사용자:%'")

                docs = curs.fetchall()

                for docdata in docs:
                    doctitle = docdata[0]
                    content = docdata[1]
                    otent = docdata[1]

                    content = re.sub(regex, changeto, content)

                    if content == otent:
                        continue
                    if content != otent:
                        curs.execute("update data set data = ?, date = ? where title = ?", [content, get_time(), doctitle])
                        history_plus(doctitle, content, get_time(), botname, log, leng_check(len(otent), len(content)), '', 1)

                        render_set(
                            title = doctitle,
                            data = content,
                            num = 1
                        )
            else:
                doccontent = getForm('doccontent', '')
                docs = getForm('docs', '').replace('\r', '').split('\n')
                botname = getForm('botname', '')
                log = getForm('log', '')

                curs.execute("select username from bots where username = ? COLLATE NOCASE", [getForm('botname', '')])
                if not(curs.fetchall()) and botname != '':
                    return easy_minify(flask.render_template(skin_check(),
                        imp = ['봇 가동', wiki_set(), custom(), other2([0, 0])],
                        data = alertBalloon('그런 봇은 등록되지 않았습니다.') + content,
                        menu = 0,
                        err = 1
                    ))

                curs.execute("select username from bots where username = ? and owner = ? COLLATE NOCASE", [getForm('botname', ''), ip_check()])
                if not curs.fetchall() and botname != '':
                    return easy_minify(flask.render_template(skin_check(),
                        imp = ['봇 가동', wiki_set(), custom(), other2([0, 0])],
                        data = alertBalloon('해당 봇은 당신의 봇이 아닙니다.') + content,
                        menu = 0,
                        err = 1
                    ))
                if ban_check(botname) == 1:
                    return easy_minify(flask.render_template(skin_check(),
                        imp = ['봇 가동', wiki_set(), custom(), other2([0, 0])],
                        data = alertBalloon('해당 봇이 차단되어 있습니다.') + content,
                        menu = 0,
                        err = 1
                    ))

                if botname == '':
                    botname = ip_check()

                for doctitle in docs:
                    curs.execute("select data from data where title = ?", [doctitle])

                    if not curs.fetchall():
                        dcnt = re.sub("[$][{]document_title[}]", doctitle, doccontent, flags=re.IGNORECASE)

                        curs.execute("insert into data (date, data, title) values (?, ?, ?)", [get_time(), dcnt, doctitle])
                        history_plus(doctitle, dcnt, get_time(), botname, log, '+' + str(len(dcnt)), '', 1)

                        render_set(
                            title = doctitle,
                            data = dcnt,
                            num = 1
                        )

        elif getForm('submittype') == 'add':
            curs.execute("select username from bots where username = ? COLLATE NOCASE", [getForm('botname', '')])
            if(curs.fetchall()):
                return easy_minify(flask.render_template(skin_check(),
                    imp = ['봇 가동', wiki_set(), custom(), other2([0, 0])],
                    data = alertBalloon('이미 해당 봇이 등록되어 있습니다.') + content,
                    menu = 0,
                    err = 1
                ))
            curs.execute("select id from user where id = ? COLLATE NOCASE", [getForm('botname', '')])
            if(curs.fetchall()):
                return easy_minify(flask.render_template(skin_check(),
                    imp = ['봇 가동', wiki_set(), custom(), other2([0, 0])],
                    data = alertBalloon('해당 이름의 사용자가 존재합니다.') + content,
                    menu = 0,
                    err = 1
                ))
            if len(getForm('botname', '')) < 1:
                return easy_minify(flask.render_template(skin_check(),
                    imp = ['봇 가동', wiki_set(), custom(), other2([0, 0])],
                    data = alertBalloon('botname의 값은 필수입니다.') + content,
                    menu = 0,
                    err = 1
                ))
            if re.search('^\s', getForm('botname', '')) or re.search('\s$', getForm('botname', '')):
                return easy_minify(flask.render_template(skin_check(),
                    imp = ['봇 가동', wiki_set(), custom(), other2([0, 0])],
                    data = alertBalloon('봇 이름이 올바르지 않습니다.') + content,
                    menu = 0,
                    err = 1
                ))
            curs.execute("insert into bots (username, owner) values (?, ?)", [getForm('botname', ''), ip_check()])
            curs.execute("insert into user (id, date, pw) values (?, ?, '0')", [getForm('botname', ''), get_time()])
            curs.execute("insert into data (title, data, date) values (?, '', ?)", ['사용자:' + getForm('botname', ''), get_time()])
            curs.execute("insert into history (title, data, i, id, date, ismember, leng, ip) values (?, '', '<i>(새 문서)</i>', '1', ?, 'author', '0', ?)", ['사용자:' + getForm('botname', ''), get_time(), getForm('botname', '')])
        elif getForm('submittype') == 'delete':
            curs.execute("select username from bots where username = ? COLLATE NOCASE", [getForm('botname', '')])
            if not(curs.fetchall()):
                return easy_minify(flask.render_template(skin_check(),
                    imp = ['봇 가동', wiki_set(), custom(), other2([0, 0])],
                    data = alertBalloon('그런 봇은 등록되지 않았습니다.') + content,
                    menu = 0,
                    err = 1
                ))
            curs.execute("select username from bots where username = ? and owner = ? COLLATE NOCASE", [getForm('botname', ''), ip_check()])
            if not curs.fetchall():
                return easy_minify(flask.render_template(skin_check(),
                    imp = ['봇 가동', wiki_set(), custom(), other2([0, 0])],
                    data = alertBalloon('해당 봇은 당신이 만든 봇이 아닙니다.') + content,
                    menu = 0,
                    err = 1
                ))
            curs.execute("delete from bots where username = ?", [getForm('botname', '')])
            curs.execute("delete from user where id = ?", [getForm('botname', '')])
            curs.execute("delete from data where title = '사용자:' || ?", [getForm('botname', '')])
            curs.execute("delete from history where title = '사용자:' || ?", [getForm('botname', '')])

        conn.commit()
        return redirect("/admin/botting")

    return easy_minify(flask.render_template(skin_check(),
        imp = ['봇 가동', wiki_set(), custom(), other2([0, 0])],
        data = content,
        menu = 0
    ))