from .tool.func import *
import datetime

def ip_whitelist(conn):
    curs = conn.cursor()
    if not('state' in flask.session and flask.session['state'] == 1):
        return redirect('/member/login?redirect=/member/ip_whitelist')
    curs.execute("select ip from ip_whitelist where username = ? COLLATE NOCASE", [ip_check()])
    content = '''
        <P>다음 목록에 있는 아이피 주소로만 이 계정으로의 로그인이 가능하게 합니다.
        <FORM METHOD=POST>
            <LABEL>아이피 주소 :</LABEL><BR>
            <INPUT TYPE=TEXT NAME=ip CLASS=form-control STYLE="width: 250px;">
            <DIV CLASS=BTNS>
                <BUTTON TYPE=SUBMIT CLASS="btn btn-primary" STYLE="width: 100px;">추가</BUTTON>
            </DIV>
        </FORM>

        <ul class=wiki-list>
    '''
    for i in curs.fetchall():
        content += '<li>' + i[0] + ' <form style="display: inline-block" method=post onsubmit="return confirm(\'삭제하시겠습니까?\');"><input type=hidden name=submittype value=delete><input type=hidden name=ip value="' + i[0] + '"><button type=submit>삭제</button></form></li>'
    content += '</ul>'

    if flask.request.method == 'POST':
        if getForm("submittype", 'add') == 'delete':
            curs.execute("delete from ip_whitelist where username = ? and ip = ?", [ip_check(), getForm('ip')])
        else:
            curs.execute("insert into ip_whitelist (username, ip) values (?, ?)", [ip_check(), getForm('ip')])
        conn.commit()
        return redirect('/member/ip_whitelist')

    return easy_minify(flask.render_template(skin_check(),
        imp = ['IP 화이트리스트', wiki_set(), custom(), other2([0, 0])],
        data = "해당 기능은 현재 작동하지 않습니다.",
        menu = [['user', load_lang('return')]]
    ))

def login_2(conn):
    curs = conn.cursor()

    if custom()[2] != 0:
        return redirect(flask.request.args.get('redirect', '/'))


    if flask.request.method == 'POST':
        if captcha_post(flask.request.form.get('g-recaptcha-response', '')) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)

        #create table ip_whitelist ( ip text default '', username text default '' )
        curs.execute("select username from ip_whitelist where username = ? COLLATE NOCASE", [getForm('id')])
        if curs.fetchall():
            curs.execute("select username from ip_whitelist where username = ? and ip = ? COLLATE NOCASE", [getForm('id'), str(my_ip())])
            if curs.fetchall():
                return easy_minify(flask.render_template(skin_check(),
                    imp = [load_lang('login'), wiki_set(), custom(), other2([0, 0])],
                    data =  alertBalloon(my_ip() + "(으)로 " + getForm('id') + ' 계정에 액세스할 수 없습니다.<br>액세스가 거부되었습니다.') + '''
                            <form class=login-form method=post>
                                Username<br>
                                <input class=form-control name="id" type="text"><br><br>
                                Password<br>
                                <input class=form-control name="pw" type="password"><br><br>
                                ''' + captcha_get() + '''<div class="checkbox" style="display: inline-block;">
                            <label>
                            <input type="checkbox" name="autologin">
                            <span>자동 로그인</span>
                            </label>
                            </div><a href="/member/recover_password" style="float: right;">[아이디/비밀번호 찾기]</a>
                                <br>
                                　<a href="/member/signup" class="btn btn-secondary">계정 만들기</a><button type="submit" class="btn btn-primary">''' + load_lang('login') + '''</button>

                                ''' + '<hr class=\"main_hr\"><span>' + load_lang('http_warring') + '</span>' + '''
                            </form>
                            ''',
                    menu = [['user', load_lang('return')]],
                    err = 1
                ))

        agent = flask.request.headers.get('User-Agent')

        if len(flask.request.form.get('id', '')) < 1:
            return easy_minify(flask.render_template(skin_check(),
                imp = [load_lang('login'), wiki_set(), custom(), other2([0, 0])],
                data =  '''
                        <form class=login-form method=post>
                            Username<br>
                            <input class=form-control name="id" type="text"><p class="error-desc">사용자 이름의 값은 필수입니다.</p><br>
                            Password<br>
                            <input class=form-control name="pw" type="password"><br><br>
                            ''' + captcha_get() + '''<div class="checkbox" style="display: inline-block;">
                        <label>
                        <input type="checkbox" name="autologin">
                        <span>자동 로그인</span>
                        </label>
                        </div><a href="/member/recover_password" style="float: right;">[아이디/비밀번호 찾기]</a>
                            <br>
                            　<a href="/member/signup" class="btn btn-secondary">계정 만들기</a><button type="submit" class="btn btn-primary">''' + load_lang('login') + '''</button>

                            ''' + '<hr class=\"main_hr\"><span>' + load_lang('http_warring') + '</span>' + '''
                        </form>
                        ''',
                menu = [['user', load_lang('return')]],
                err = 1
            ))

        curs.execute("select pw, encode, id from user where id = ? COLLATE NOCASE", [flask.request.form.get('id', None)])
        user = curs.fetchall()
        if not user:
            return easy_minify(flask.render_template(skin_check(),
                imp = [load_lang('login'), wiki_set(), custom(), other2([0, 0])],
                data =  '''
                        <form class=login-form method=post>
                            Username<br>
                            <input class=form-control name="id" type="text" value="''' + flask.request.form.get('id', '') + '''"><p class="error-desc">사용자 이름이 올바르지 않습니다.</p><br>
                            Password<br>
                            <input class=form-control name="pw" type="password"><br><br>
                            ''' + captcha_get() + '''<div class="checkbox" style="display: inline-block;">
                        <label>
                        <input type="checkbox" name="autologin">
                        <span>자동 로그인</span>
                        </label>
                        </div><a href="/member/recover_password" style="float: right;">[아이디/비밀번호 찾기]</a>
                            <br>
                            　<a href="/member/signup" class="btn btn-secondary">계정 만들기</a><button type="submit" class="btn btn-primary">''' + load_lang('login') + '''</button>

                            ''' + '<hr class=\"main_hr\"><span>' + load_lang('http_warring') + '</span>' + '''
                        </form>
                        ''',
                menu = [['user', load_lang('return')]],
                err = 1
            ))
        un = user[0][2]

        pw_check_d = pw_check(
            flask.request.form.get('pw', ''),
            user[0][0],
            user[0][1],
            un
        )
        if pw_check_d != 1:
            return easy_minify(flask.render_template(skin_check(),
                imp = [load_lang('login'), wiki_set(), custom(), other2([0, 0])],
                data =  '''
                        <form class=login-form method=post>
                            Username<br>
                            <input class=form-control name="id" type="text" value="''' + flask.request.form.get('id', '') + '''"><br><br>
                            Password<br>
                            <input class=form-control name="pw" type="password"><p class="error-desc">패스워드가 올바르지 않습니다.</p><br>
                            ''' + captcha_get() + '''<div class="checkbox" style="display: inline-block;">
                        <label>
                        <input type="checkbox" name="autologin">
                        <span>자동 로그인</span>
                        </label>
                        </div><a href="/member/recover_password" style="float: right;">[아이디/비밀번호 찾기]</a>
                           <br>
                            　<a href="/member/signup" class="btn btn-secondary">계정 만들기</a><button type="submit" class="btn btn-primary">''' + load_lang('login') + '''</button>

                            ''' + '<hr class=\"main_hr\"><span>' + load_lang('http_warring') + '</span>' + '''
                        </form>
                        ''',
                menu = [['user', load_lang('return')]],
                err = 1
            ))

        flask.session['state'] = 1
        flask.session['id'] = un

        curs.execute("select css from custom where user = ?", [un])
        css_data = curs.fetchall()
        if css_data:
            flask.session['head'] = css_data[0][0]
        else:
            flask.session['head'] = ''
        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'hi'])
        if not(curs.fetchall()):
            curs.execute("insert into ua_d (name, ip, ua, today, sub) values (?, ?, ?, ?, '')", [un, ip_check(1), agent, get_time()])

        res = flask.make_response(flask.redirect(flask.request.args.get('redirect', '/')))
        res.set_cookie('dooly', '', expires=0)
        res.set_cookie('doornot', '', expires=0)

        if not SQLexec("select pin from spin where username = ?", [un]):
            curs.execute("delete from spin where username = ?", [un])
            curs.execute("insert into spin (username, pin) values (?, ?)", [un, rndval("01234567890", 8)])

        if flask.request.form.get('autologin', 0) != 0:
            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(days=180)

            rndtkn = rndval("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

            #create table token ( username text default '', key text default '' )
            #일부러 update로 안 함
            curs.execute("delete from token where username = ?", [un])
            curs.execute("insert into token (username, key) values (?, ?)", [un, rndtkn])

            res.set_cookie("dooly", value=sha3(sha3(sha3(sha224(sha224(sha3(sha224(sha3(pw_encode(getForm('pw', '')) + sha3(rndtkn))))))))), expires = expire_date, secure = True, httponly = True)
            res.set_cookie("doornot", value=getForm('id', ''), expires = expire_date, secure = True, httponly = True)

        conn.commit()

        return res
    else:
        oauth_check = 0
        oauth_content = '<hr class=\"main_hr\"><div class="oauth-wrapper"><ul class="oauth-list">'
        oauth_supported = load_oauth('_README')['support']
        for i in range(len(oauth_supported)):
            oauth_data = load_oauth(oauth_supported[i])
            if oauth_data['client_id'] != '' and oauth_data['client_secret'] != '':
                oauth_content += '''
                    <li>
                        <a href="/oauth/{}/init">
                            <div class="oauth-btn oauth-btn-{}">
                                <div class="oauth-btn-logo oauth-btn-{}"></div>
                                {}
                            </div>
                        </a>
                    </li>
                '''.format(
                    oauth_supported[i],
                    oauth_supported[i],
                    oauth_supported[i],
                    load_lang('oauth_signin_' + oauth_supported[i])
                )

                oauth_check = 1

        oauth_content += '</ul></div>'

        if oauth_check == 0:
            oauth_content = ''

        http_warring = '<hr class=\"main_hr\"><span>' + load_lang('http_warring') + '</span>'

        return easy_minify(flask.render_template(skin_check(),
            imp = [load_lang('login'), wiki_set(), custom(), other2([0, 0])],
            data =  '''
                <script>
                    $(function() {
                        $("#loginSubmit").attr('type', 'button');
                        $("#loginSubmit").click(function() {
                            $("#httpwarning").show();
                        });
                    });
                </script>
                    <form class=login-form method=post>
                        <div class=alert style="display: none;" id=httpwarning>
                            <strong>[경고!]</strong> 인터넷에 비밀번호를 비롯한 정보를 전송할 때 HTTPS이 아니면 그 정보를 다른 사람이 볼 수 있습니다. <a id=contlnk onclick="$(this).parent().parent().submit();">[계속]</a> <a onclick="$(this).parent().hide();">[취소]</a>
                        </div>
                        Username<br>
                        <input class=form-control name="id" type="text"><br><br>
                        Password<br>
                        <input class=form-control name="pw" type="password"><br><br>
                        ''' + captcha_get() + '''<div class="checkbox" style="display: inline-block;">
                        <label>
                        <input type="checkbox" name="autologin">
                        <span>자동 로그인</span>
                        </label>
                        </div><a href="/member/recover_password" style="float: right;">[아이디/비밀번호 찾기]</a>
                        <br>
                        　<a href="/member/signup" class="btn btn-secondary">계정 만들기</a><button type="submit" class="btn btn-primary" id=loginSubmit>''' + load_lang('login') + '''</button>
                        ''' + oauth_content + '''
                        ''' + '<hr class=\"main_hr\"><span>' + load_lang('http_warring') + '</span>' + '''
                    </form>
                    ''',
            menu = [['user', load_lang('return')]]
        ))