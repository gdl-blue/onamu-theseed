from .tool.func import *

def topic_seed_2_3(conn, tnum, snum):
    curs = conn.cursor()

    return discussFetch(tnum, '0', snum)

def api_topic_sub_2(conn, tnum, time):
    curs = conn.cursor()

    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')

    curs.execute("select sub from rd where tnum = ? and removed = '1'", [tnum])
    if curs.fetchall() and admin_check() != 1:
        return re_error('/error/7000')

    if getacl(name, 'read') == 0:
        return noread(conn, name)

    if flask.request.args.get('num', None):
        curs.execute("select id, data, date, ip, block, top, adm, ismember from topic where tnum = ? and id + 0 = ? + 0 order by id + 0 asc", [
            tnum,
            flask.request.args.get('num', '')
        ])
    elif flask.request.args.get('top', None):
        curs.execute("select id, data, date, ip, block, top, adm, ismember from topic where tnum = ? and top = 'O' order by id + 0 asc", [tnum])
    else:
        curs.execute("select id, data, date, ip, block, top, adm, ismember from topic where tnum = ? order by id + 0 asc", [tnum])

    data = curs.fetchall()
    if data:
        json_data = {}
        admin = admin_check(3)

        for i in data:
            t_data_f = render_set(data = i[1])
            if t_data_f == '스레드 상태를 <b>open</b>로 변경':
                t_data_f = '스레드 상태를 <b>normal</b>로 변경'
            if i[4] != 'O':
                b_color = ''
            else:
                b_color = 'toron_color_grey'
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'htc'])
                if not(curs.fetchall()):
                    curs.execute("select who from re_admin where what = ? order by time desc limit 1", ['blind (' + name + ' - ' + sub + '#' + str(i[0]) + ')'])
                    who_blind = curs.fetchall()
                    if who_blind:
                        t_data_f = '[' + who_blind[0][0] + '에 의해 숨겨진 글입니다.]'
                        blablabla = 1
                    else:
                        t_data_f = '[숨겨진 글입니다.]'
                        blablabla = 1
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'htc'])
                if curs.fetchall():
                    curs.execute("select who from re_admin where what = ? order by time desc limit 1", ['blind (' + name + ' - ' + sub + '#' + str(i[0]) + ')'])
                    who_blind = curs.fetchall()
                    if who_blind:
                        t_data_f = '<span class="hidden-info">[' + who_blind[0][0] + '에 의해 숨겨진 글입니다.]</span><ctl class="new-show-hidden-content-button"> <a class="btn btn-danger btn-sm" onclick="$(this).parent().children(\'.hidden-content\').show(); $(this).hide(); $(this).parent().parent().children(\'.hidden-info\').hide(); $(this).parent().parent().attr(\'class\', \'r-body\'); return false;" style="color: rgb(255, 255, 255); width: auto;">[ADMIN] SHOW</a><div class="hidden-content" style="display:none">' + t_data_f + '</div></ctl><ctl class="old-show-hidden-content-button" style="display: none;"><div class="text-line-break" style="margin: 25px 0px 0px -10px; display:block"><a class="text" onclick="$(this).parent().parent().children(\'.hidden-content\').show(); $(this).parent().css(\'margin\', \'15px 0 15px -10px\'); $(this).hide(); return false;" style="display: block; color: #fff;">[ADMIN] Show hidden content</a><div class="line"></div></div><div class="hidden-content" style="display:none">' + t_data_f + '</div></ctl>'
                        blablabla = 1
                    else:
                        t_data_f = '[숨겨진 글입니다.]<br><br>' + t_data_f
                        blablabla = 1

            if flask.request.args.get('render', None):
                if i[0] == '1':
                    s_user = i[3]
                else:
                    if flask.request.args.get('num', None):
                        curs.execute("select ip from topic where tnum = ? order by id + 0 asc limit 1", [tnum])
                        g_data = curs.fetchall()
                        if g_data:
                            s_user = g_data[0][0]
                        else:
                            s_user = ''
                oraoraorgaanna = 0
                if flask.request.args.get('top', None):
                    t_color = 'toron_color_red'
                elif i[3] == s_user:
                    t_color = 'toron_color_green'
                elif i[5] == '1':
                    if i[3] == s_user:
                        t_color = 'toron_color_green'
                    else:
                        t_color = 'toron_color'
                    oraoraorgaanna = 1
                else:
                    t_color = 'toron_color'

                ip = ''

                if 3 == 4: #admin_check(1) == 1:
                    if i[7] == 'ip':
                        if ban_check(i[3], ipacl = True) == 1:
                            ip += ' <a href="/admin/ipacl?cidr=' + url_pas(i[3]) + '/32&note=쓰레드 ' + tnum + ' %23' + i[0] + '">[차단 해제]</a>'
                        else:
                            ip += ' <a href="/admin/ipacl?cidr=' + url_pas(i[3]) + '/32&note=쓰레드 ' + tnum + ' %23' + i[0] + '">[차단]</a>'
                    else:
                        if ban_check(i[3]) == 1:
                            ip += ' <a href="/admin/suspend_account/' + url_pas(i[3]) + '?note=쓰레드 ' + tnum + ' %23' + i[0] + '">[차단 해제]</a>'
                        else:
                            ip += ' <a href="/admin/suspend_account/' + url_pas(i[3]) + '?note=쓰레드 ' + tnum + ' %23' + i[0] + '">[차단]</a>'



                if i[6] == '1':
                    if i[7] != 'ip':
                        ip += '<a style="font-weight: bold;" href="/w/사용자:' + url_pas(i[3]) + '">' + html.escape(i[3]) + '</a>'
                    else:
                        ip += '<a style="font-weight: bold;" href="/contribution/ip/' + url_pas(i[3]) + '/document">' + html.escape(i[3]) + '</a>'
                else:
                    if i[7] != 'ip':
                        ip += '<a href="/w/사용자:' + url_pas(i[3]) + '">' + html.escape(i[3]) + '</a>'
                    else:
                        ip += '<a href="/contribution/ip/' + url_pas(i[3]) + '/document">' + html.escape(i[3]) + '</a>'
                #ip += ip_pas_t(i[3], i[7], i[6])

                #if admin == 1 or b_color != 'toron_color_grey':
                    #ip += ' <a href="/topic/' + url_pas(name) + '/sub/' + url_pas(sub) + '/admin/' + i[0] + '">(' + load_lang('discussion_tool') + ')</a>'
                if i[7] == 'ip':
                    if ban_check(i[3], ipacl = True) == 1:
                        ip += ' <sub>(차단된 아이피)</sub>'
                else:
                    if ban_check(i[3]) == 1:
                        ip += ' <sub>(차단된 사용자)</sub>'
                pinbtn = ''
                curs.execute("select perm from grant where perm = 'htc' and user = ?", [ip_check()])
                if curs.fetchall():
                    if i[5] == 'O':
                        pinbtn = '<a class="btn btn-warning btn-sm" href="/admin/thread/' + tnum + '/' + i[0] + '/unpin">[ADMIN] 고정 해제</a>'
                    else:
                        pinbtn = '<a class="btn btn-warning btn-sm" href="/admin/thread/' + tnum + '/' + i[0] + '/pin">[ADMIN] 고정</a>'
                if i[5] == '1':
                    pinbtn = ''

                all_data = '''
                    <div class="res-wrapper" data-id="''' + i[0] + '''">'''
                if i[5] == '1':
                    all_data +=  '<div class="res res-type-status">'
                else:
                    all_data +=  '<div class="res res-type-normal">'
                all_data += '''
                        <div class="r-head'''
                if i[3] == s_user:
                    all_data += ' first-author'
                ddd = i[2].split(' ')[0]
                ttt = i[2].split(' ')[1]
                all_data += '''
                                "><span class="num"><a id="''' + i[0] + '">#' + i[0] + '</a>&nbsp;</span> ' + ip + ' <span style="margin-left: 25px;float:right"><time datetime="''' + ddd + 'T' + ttt + '''.000Z" data-format="Y-m-d H:i:s">''' + i[2] + '''</time></span><div class="clearfix"></div>
                                </div>
                        <div class="r-body'''
                if i[4] == 'O':
                    all_data += ' r-hidden-body'
                all_data += '''">'''
                all_data += t_data_f + '''
                            </div>
                '''
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'htc'])
                if curs.fetchall():
                    if i[4] == 'O':
                        urlToHideOrShow = 'show'
                    else:
                        urlToHideOrShow = 'hide'
                    all_data += '''
                    <div class="combo admin-menu">

				    <a class="btn btn-danger btn-sm" href="/admin/thread/''' + url_pas(tnum) + '''/''' + i[0] + '''/''' + urlToHideOrShow + '''" style="color:#fff">'''
                    if i[4] == 'O':
                        all_data += '''[ADMIN] 숨기기 해제'''
                    else:
                        all_data += '''[ADMIN] 숨기기'''
                    all_data += '''</a>''' + pinbtn + '''</div>'''
                all_data += '</div></div>'

                #all_data += '<br /><br />'

                json_data[i[0]] = {
                    "data" : all_data
                }
            else:
                json_data[i[0]] = {
                    "data" : t_data_f,
                    "date" : i[2],
                    "ip" : i[3],
                    "block" : i[4],
                }

        return flask.jsonify(json_data)
    else:
        return flask.jsonify({})