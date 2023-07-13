from .tool.func import *

def user_info_2(conn):
    #return redirect('/member/mypage')

    curs = conn.cursor()

    ip = ip_check()

    curs.execute("select acl from user where id = ?", [ip])
    data = curs.fetchall()
    if ban_check() == 0:
        if data:
            acl = load_lang('member')
            if admin_check(5) == 1:
                acl = loadLang('관리자', "Administrator")
            if getperm('arbiter') == 1:
                acl = loadLang("중재자", "Arbiter")
            if getperm('tribune') == 1:
                acl = loadLang("호민관", "Tribune")
            if admin_check() == 1:
                acl = loadLang("개발자", "Developer")
        else:
            if islogin() == 1:
                acl = loadLang("일반 사용자", "Member")
            else:
                acl = loadLang("로그인하지 않음", "Please Login!")
    else:
        acl = load_lang('blocked')

        match = re.search("^([0-9]{1,3}\.[0-9]{1,3})", ip)
        if match:
            match = match.groups()[0]
        else:
            match = '-'

        curs.execute("select end, login, band from ban where block = ? or block = ?", [ip, match])
        block_data = curs.fetchall()
        if block_data:
            if block_data[0][0] != '':
                acl += ' (' + load_lang('period') + ' : ' + block_data[0][0] + ')'
            else:
                acl += ' (' + load_lang('limitless') + ')'

            if block_data[0][1] != '':
                acl += ' (' + load_lang('login_able') + ')'

            if block_data[0][2] == 'O':
                acl += ' (' + load_lang('band_blocked') + ')'

    curs.execute('select count(name) from alarm where name = ?', [ip_check()])
    notificationData = curs.fetchall()
    if notificationData:
        plus2 = '<li><a href="/member/notifications">' + loadLang("알림", "Notifications") + ' (' + str(notificationData[0][0]) + ')</a></li>'
    else:
        plus2 = '<li><a href="/member/notifications">' + loadLang('알림', 'Notifications') + '</a></li>'

    if custom()[2] != 0:
        ip_user = '<a href="/w/사용자:' + ip + '">' + ip + '</a>'

        spin = custom()[20]

        plus = '''
            <li><a href="/member/logout">''' + load_lang('logout') + '''</a></li>
            <li><a href="/member/mypage">''' + load_lang('user_setting') + '''</a></li>
        '''

        if spin != '00000000':
            plus += '<li style="margin-bottom: 10px;">지원 PIN: ' + spin + '</li>'

        plus2 += '<li><a href="/member/starred_documents">' + load_lang('watchlist') + '</a></li>'
        plus3 = '<li><a href="/acl/사용자:' + url_pas(ip) + '">' + loadLang('사용자 문서 ACL', 'My User Document\'s ACL') + '</a></li>'
    else:
        ip_user = ip

        plus = '''
            <li><a href="/member/login">''' + load_lang('login') + '''</a></li>
            <li><a href="/member/signup">''' + load_lang('register') + '''</a></li>
        '''
        plus3 = ''

        curs.execute("select data from other where name = 'email_have'")
        test = curs.fetchall()
        if test and test[0][0] != '':
            plus += '<li><a href="/pass_find">' + load_lang('password_search') + '</a></li>'

    if 'state' in flask.session and flask.session['state'] == 1:
        ismember = 'author'
    else:
        ismember = 'ip'
    #endif

    return easy_minify(flask.render_template(skin_check(),
        imp = [loadLang('내 계정 도구', "Account Tools"), wiki_set(), custom(), other2([0, 0])],
        data = '''
            <h2>''' + loadLang('내 계정', 'My Account') + '''</h2>
            <ul>
                <li>''' + ip_user + ' (' + acl + ''')</li>
                <li><a href="/contribution/''' + ismember + '''/''' + url_pas(ip) + '''/document">''' + loadLang('내 문서 기여 내역', 'My document contributions') + '''</a></li>
                <li style="margin-bottom: 10px;"><a href="/contribution/''' + ismember + '''/''' + url_pas(ip) + '''/discuss">''' + loadLang('내 토론 참여 내역', 'My discussion history') + '''</a></li>
                ''' + plus + '''
            </ul>
            <br>
            <h2>''' + load_lang('tool') + '''</h2>
            <ul>
                ''' + plus3 + '''
                <li><a href="/custom_head">''' + loadLang('사용자 지정 &lt;HEAD&gt; 코드', 'Custom &lt;HEAD&gt; Code') + '''</a></li>
            </ul>
            <br>
            <h2>''' + load_lang('other') + '''</h2>
            <ul>
            ''' + plus2 + '''
            <li>
                <a href="/member/ip_whitelist">IP ''' + loadLang('허용 목록', 'Whitelist') + '''</a>
            </li>
            </ul>
        ''',
        menu = 0
    ))