from .tool.func import *
import time
import datetime

def recent_changes_2(conn, name, tool, ismember):
    curs = conn.cursor()
    cmp = ''
    rn = ''
    rnr = ''
    see = ''
    raw = ''
    ndc = ''

    if tool == 'history' and getacl(name, 'read') == 0:
        return noread(conn, name)

    if tool == 'history':
        curs.execute("select id from history where title = ?", [name])
        if not(curs.fetchall()):
            return re_error('/error/8000')

    if flask.request.method == 'POST':
        return redirect(
            '/diff/' + url_pas(name) +
            '?first=' + flask.request.form.get('b', '1') +
            '&second=' + flask.request.form.get('a', '1')
        )
    else:
        one_admin = admin_check(1)
        six_admin = admin_check(6)

        ban = '';
        select = ''

        div = '''

            <table class="table table-hover">
            <colgroup>
<col>
<col style="width: 25%;">
<col style="width: 22%;">
</colgroup><thead>

        '''

        if name:
            num = int(number_check(flask.request.args.get('num', '1')))
            if tool == 'record' or tool == 'contribution':
                if num * 1000 > 0:
                    sql_num = num * 1000 - 1000
                else:
                    sql_num = 0
            elif tool == 'history':
                if num * 30 > 0:
                    sql_num = num * 30 - 30
                else:
                    sql_num = 0
            else:
                if num * 95 > 0:
                    sql_num = num * 95 - 95
                else:
                    sql_num = 0

            if tool == 'history':
                div = '''
                    <ul class=wiki-list>
                '''

                # 기본적인 move만 구현
                tool_select = flask.request.args.get('tool', None)
                if tool_select:
                    if tool_select == 'move':
                        curs.execute('''
                            select id, title, date, ip, send, leng, i, ismember from history
                            where send like ? or send like ?
                            order by id + 0 desc
                            limit ?, '30'
                        ''', ['%(<a>' + name +'</a>%', '%<a>' + name + '</a> move)', str(sql_num)])
                    else:
                        curs.execute('''
                            select id, title, date, ip, send, leng, i, ismember from history
                            where title = ?
                            order by id + 0 desc
                            limit ?, '30'
                        ''', [name, str(sql_num)])
                else:
                    curs.execute('''
                        select id, title, date, ip, send, leng, i, ismember from history
                        where title = ?
                        order by id + 0 desc
                        limit ?, '30'
                    ''', [name, str(sql_num)])
            else:
                div +=  '''
                        <tr><th><b>''' + '문서' + '''</b></th>
                        <th><b>''' + '수정자' + '''</b></th>
                        <th><b>''' + '수정 시간' + '''</b></th>
                    </tr>
                '''
                if flask.request.args.get('logtype', 'all') == 'create':
                    ccmd = " and i = '<i>(새 문서)</i>'"
                else:
                    ccmd = ''
                curs.execute("select count(title) from history where ip = ? and ismember = ?" + ccmd + " COLLATE NOCASE", [name, ismember])
                cntData = curs.fetchall()
                if cntData:
                    cntData = cntData[0][0]
                else:
                    cntData = 0
                #endif
                div = '''<p>이 사용자의 문서 기여 횟수는 ''' + str(cntData) + ''' 입니다.</p><ol class="breadcrumb link-nav">
                        <li><strong>[문서]</strong></li>
                        <li><a href="./discuss">[토론]</a></li>
                        </ol>''' + div

                curs.execute("select id, title, date, ip, send, leng, i, ismember from history where ip = ? and ismember = ?" + ccmd + " COLLATE NOCASE order by date desc limit ?, '1000'", [name, ismember, str(sql_num)])
        else:
            num = int(number_check(flask.request.args.get('num', '1')))
            if tool == 'record' or tool == 'contribution':
                if num * 1000 > 0:
                    sql_num = num * 1000 - 1000
                else:
                    sql_num = 0
            elif tool == 'history':
                if num * 30 > 0:
                    sql_num = num * 30 - 30
                else:
                    sql_num = 0
            else:
                if num * 95 > 0:
                    sql_num = num * 95 - 95
                else:
                    sql_num = 0

            div +=  '''
                        <tr>
                        <th><b>''' + '항목' + '''</b></th>
                        <th><b>''' + '수정자' + '''</b></th>
                        <th><b>''' + '수정 시간' + '''</b></th>
                        </tr>

                '''

            div = '''<ol class="breadcrumb link-nav">
                <li><a href="?logtype=all">[전체]</a></li>
                <li><a href="?logtype=create">[새 문서]</a></li>
                <li><a href="?logtype=delete">[삭제]</a></li>
                <li><a href="?logtype=move">[이동]</a></li>
                <li><a href="?logtype=revert">[되돌림]</a></li>
            </ol>''' + div
            if flask.request.args.get('logtype', 'all') == 'all':
                curs.execute('''
                    select id, title, date, ip, send, leng, i, ismember from history
                    order by date desc
                    limit ?, 95
                ''', [str(sql_num)])
            elif flask.request.args.get('logtype', 'all') == 'create':
                curs.execute('''
                    select id, title, date, ip, send, leng, i, ismember from history
                    where i like '<i>(새 문서)</i>'
                    order by date desc
                    limit ?, 95
                ''', [str(sql_num)])
            elif flask.request.args.get('logtype', 'all') == 'delete':
                curs.execute('''
                    select id, title, date, ip, send, leng, i, ismember from history
                    where i like '<i>(삭제)</i>'
                    order by date desc
                    limit ?, 95
                ''', [str(sql_num)])
            elif flask.request.args.get('logtype', 'all') == 'move':
                curs.execute('''
                    select id, title, date, ip, send, leng, i, ismember from history
                    where i like '<i>(%에서 %(으)로 문서 이동)</i>'
                    order by date desc
                    limit ?, 95
                ''', [str(sql_num)])
            elif flask.request.args.get('logtype', 'all') == 'revert':
                curs.execute('''
                    select id, title, date, ip, send, leng, i, ismember from history
                    where i like '<i>(r%으로 되돌림)</i>'
                    order by date desc
                    limit ?, 95
                ''', [str(sql_num)])
        if tool != 'history':
            div += '</thead><tbody id>'

        data_list = curs.fetchall()
        for data in data_list:
            try:
                if not name and not tool == 'history' and flask.request.args.get('logtype', 'all') == 'all':
                    if data[1].split(':')[0] in getNamespaces(nologOnly = True):
                        continue
            except:
                pass

            select += '<option value="' + data[0] + '" id>' + data[0] + '</option>'
            send = '<br>'

            if data[4]:
                if not re.search("^(?: *)$", data[4]):
                    send = data[4]

            if re.search("\+", data[5]):
                leng = '(<span style="color:green;">' + data[5] + '</span>)'
            elif re.search("\-", data[5]):
                leng = '(<span style="color:red;">' + data[5] + '</span>)'
            else:
                leng = '(<span style="color:gray;">' + data[5] + '</span>)'

            ip = ip_pas(data[3], data[7])
            if tool == 'history':
                if int(data[0]) - 1 == 0:
                    revert = ' <a href="/revert/' + url_pas(data[1]) + '?rev=' + str(int(data[0])) + '">이 리비젼으로 ' + load_lang('revert') + '</a>'
                else:
                    if int(data[0]) == 1:
                        dsfdsd = ''
                    else:
                        cmp = ' | <a href="/diff/' + url_pas(data[1]) + '?olderrev=' + str(int(data[0]) - 1) + '&rev=' + data[0] + '">' + load_lang('compare') + '</a>'
                    revert = ' <a href="/revert/' + url_pas(data[1]) + '?rev=' + str(int(data[0])) + '">이 리비젼으로 ' + load_lang('revert') + '</a>'
            else:
                revert = ''

            style = ['', '']
            date2 = data[2]
            ddd = data[2].split(' ')[0]
            ttt = data[2].split(' ')[1]
            date = '<time datetime="' + ddd + 'T' + ttt + '.000Z" data-format="Y-m-d H:i:s">' + date2 + '</time>'

            curs.execute('''
                select title from history
                where title = ? and id = ? and hide = 'O'
            ''', [data[1], data[0]])
            hide = curs.fetchall()

            if six_admin == 1:
                if hide:
                    if tool == 'history':
                        hidden = ' | <a href="/hidden/' + url_pas(data[1]) + '?num=' + data[0] + '">' + load_lang('hide_release') + '</a>'
                    else:
                        hidden = ' <a href="/hidden/' + url_pas(data[1]) + '?num=' + data[0] + '">[' + load_lang('hide_release') + ']'

                    style[0] = 'id="toron_color_grey"'
                    style[1] = 'id="toron_color_grey"'

                    if send == '<br>':
                        send = '[' + load_lang('hide') + ']'
                    else:
                        send += ' [' + load_lang('hide') + ']'
                else:
                    if tool == 'history':
                        hidden = ' | <a href="/hidden/' + url_pas(data[1]) + '?num=' + data[0] + '">' + load_lang('hide') + '</a>'
                    else:
                        hidden = ' <a href="/hidden/' + url_pas(data[1]) + '?num=' + data[0] + '">[' + load_lang('hide') + ']'
            elif not hide:
                hidden = ''
            else:
                ip = ''
                hidden = ''
                ban = ''
                date = ''

                send = '[' + load_lang('hide') + ']'

                style[0] = 'style="display: none;"'
                style[1] = 'id="toron_color_grey"'

            if tool == 'history':
                rn = 'r' + data[0]
                rnr = data[0]
                see = '<a href="/w/' + url_pas(name) + '?rev=' + data[0] + '">보기</a> '
                raw = '<a href="/raw/' + url_pas(name) + '?rev=' + data[0] + '">' + load_lang('raw') + '</a> '
            else:
                title = '<a href="/w/' + url_pas(data[1]) + '">' + html.escape(data[1]) + '</a> '
                title += '<a href="/history/' + url_pas(data[1]) + '">[역사]</a> '
                if int(data[0]) > 1:
                    title += '<a href="/diff/' + url_pas(data[1]) + '?olderrev=' + str(int(data[0]) - 1) + '&rev=' + data[0] + '">[비교]</a> '
                    title += '<a href="/revert/' + url_pas(data[1]) + '?rev=' + str(int(data[0]) - 1) + '">[편집 취소]</a> '
                else:
                    title += '<a href="/delete/' + url_pas(data[1]) + '">[편집 취소]</a> '
                title += '<a href="/discuss/' + url_pas(data[1]) + '">[토론]</a> '

            if tool == 'history':
                ita = ''
                snd = send_parser_h(send)
                if re.search(" [(]<i>.*</i>[)]", send_parser_h(send)):
                    ita = '<i>' + re.findall(" [(]<i>.*</i>[)]") + '</i>'
                    snd.replace(re.findall(" [(]<i>.*</i>[)]"), '')
                if rnr == '1':
                    ndc = ''
                    cmp = ''
                if send_parser_h(send) == '[숨기기]':
                    if six_admin == 1:
                        div += '''<li>''' + date + '''
                            <span style="font-size: 8pt;">
                            (''' + see + ''' | ''' + raw + ''' | ''' + revert + cmp + hidden + ''')</span> <input name="a" type="radio" style="width:20px" onclick="document.getElementById('a').value=\'''' + str(rnr) + '''\';"><input name="b" type="radio" style="width:20px" onclick="document.getElementById('b').value=\'''' + str(rnr) + '''\';">''' + ndc + data[6] + ''' <b>''' + rn + '''</b> ''' + leng + ''' ''' + ip + ban + ''' (<span style="color:gray">''' + snd + '''</span>)</li>
                        '''
                    else:
                        div += ''
                else:
                    eq = ''
                    curs.execute("select q from history where title = ? and id = ?", [name, rnr])
                    eqq = curs.fetchall()
                    curs.execute("select qn from history where title = ? and id = ?", [name, rnr])
                    eqn = curs.fetchall()

                    if eqq:
                        if eqq[0][0] == 'O':
                            if eqn:
                                eq = '<a href="/edit_request/' + eqn[0][0] + '"><i>(편집 요청)</i></a>'
                            else:
                                eq = '<a><i>(편집 요청)</i></a>'
                    blk = ''
                    if admin_check(1) == 1:
                        if data[7] == 'author':
                            blk = ' | <a href="/admin/suspend_account/' + data[3] + '?note=[[' + url_pas(name) + ']] ' + rn + '">차단</a>'
                    if getperm('ipa') == 1:
                        if data[7] == 'ip':
                            blk = ' | <a href="/admin/ipacl?cidr=' + data[3] + '&note=[[' + url_pas(name) + ']] ' + rn + '">차단</a>'

                    div += '''<li id>''' + date + '''
                        <span style="font-size: 8pt;">
                        (''' + see + ''' | ''' + raw + ''' | ''' + revert + cmp + blk + hidden + ''')</span> <input name="a" type="radio" style="width:20px" onclick="document.getElementById('a').value=\'''' + str(rnr) + '''\';"><input type="radio" name="rev" style="width:20px" onclick="document.getElementById('b').value=\'''' + str(rnr) + '''\';">''' + ndc + data[6] + ''' <b>''' + rn + '''</b> ''' + leng + ''' ''' + eq + ''' ''' + ip + ban + ''' (<span style="color:gray">''' + snd + '''</span>)</li>
                    '''
            else:
                curs.execute("select i from history where title = ? and id = ?", [data[1], data[0]])
                ii = curs.fetchall()

                blk = ''
                if admin_check(1) == 1:
                    if data[7] == 'author':
                        blk = '<a href="/admin/suspend_account/' + data[3] + '?note=[[' + url_pas(data[1]) + ']] r' + data[0] + '"> [차단]</a>'
                if getperm('ipa') == 1:
                    if data[7] == 'ip':
                        blk = '<a href="/admin/ipacl?cidr=' + data[3] + '&note=[[' + url_pas(data[1]) + ']] r' + data[0] + '"> [차단]</a>'

                div +=  '''
                    <tr ''' + style[0] + '''>
                        <td>''' + title + revert + blk + ' ' + leng + '''</td>
                        <td>''' + ip + ban + hidden + '''</td>
                        <td>''' + date + '''</td>
                    </tr>'''

                if send_parser(send) == '<br>':
                    if ii and ii[0][0] == '':
                        dfadsfgasd = 2
                    else:
                        if ii:
                            div += '''<tr ''' + style[1] + '''>
                                <td colspan="3">''' + ii[0][0] + '''</td>
                            </tr>'''
                else:
                    if ii:
                        div += '''<tr ''' + style[1] + '''>
                            <td colspan="3">''' + send_parser_h(send) + ''' ''' + ii[0][0] + '''</td>
                        </tr>'''
                    else:
                        div += '''<tr ''' + style[1] + '''>
                            <td colspan="3">''' + send_parser_h(send) + '''</td>
                        </tr>'''


        if tool == 'history':
            div += '''</ul>'''
        else:
            div +=  '''
                </tbody></table>
            '''
        sub = ''

        if name:
            if tool == 'history':
                if not tool_select:
                    div = '''


                    ''' + div
                    #<div style="padding: .75rem 1rem;margin-bottom: 1rem;list-style: none;background-color: #eceeef;border-radius: .25rem;"><a href="?tool=move">[''' + load_lang('move') + ''']</a></div>

                div = '''
                    <form method="get" action="/diff/''' + url_pas(name) + '''">
                        <div style="display:none"><select name="olderrev" id="a">''' + select + '''</select> <select name="rev" id="b">''' + select + '''</select></div>
                        <button type="submit" class="btn btn-secondary">선택 리비젼 ''' + load_lang('compare') + '''</button><br><br>
                    </form>

                ''' + next_fix('/history/' + url_pas(name) + '?num=', num, data_list, 30) + '''<br><br>''' + div
                title = name

                sub += '의 ' + load_lang('history')

                menu = [['w/' + url_pas(name), load_lang('document')], ['raw/' + url_pas(name), load_lang('raw')]]

                div += next_fix('/history/' + url_pas(name) + '?num=', num, data_list, 30)
            else:
                #curs.execute("select end from ban where block = ?", [name])
                #if curs.fetchall():
                    #sub += ' (' + load_lang('blocked') + ')'

                title = '"' + ip_pas_raw(name) + '" ' + '기여 목록'

                menu = [['other', load_lang('other')], ['user', load_lang('user')]]

                div += next_fix('/contribution/author/' + url_pas(name) + '/document?num=', num, data_list, 1000)
        else:
            menu = 0
            title = load_lang('recent_change')

            #div += next_fix('/RecentChanges?num=', num, data_list)

            if flask.request.args.get('set', 'normal') == 'user':
                sub = ' [' + load_lang('user') + ']'
                menu = [['RecentChanges', load_lang('return')]]

        if sub == '':
            sub = 0

        if tool == 'history':
            return easy_minify(flask.render_template(skin_check(),
                imp = [title, wiki_set(), custom(), other2([sub, 0])],
                data = div,
                menu = menu,
                st = 7,
                smsub = ' (문서 역사)'
            ))
        else:
            if name:
                if ismember == 'author':
                    mv = 1
                else:
                    mv = 0
                return easy_minify(flask.render_template(skin_check(),
                    imp = [title, wiki_set(), custom(), other2([sub, 0])],
                    data = div,
                    menu = menu,
                    cont = 1,
                    un = name,
                    contm = mv
                ))
            else:
                return easy_minify(flask.render_template(skin_check(),
                    imp = [title, wiki_set(), custom(), other2([sub, 0])],
                    data = div,
                    menu = menu,
                    rc = 1
                ))

def senkawaRecentApi(conn):
    curs = conn.cursor()
    if flask.request.args.get('discuss', None) == '1':
        try:
            limit = int(flask.request.args.get('limit', '5'))
            if limit > 50:
                limit = 5
        except:
            limit = 5
        curs.execute("select sub, date, tnum from rd where not stop = 'O' and not agree = 'O' and not pause = 'O' order by date desc limit ?", [limit])

        dv = ''
        for data in curs.fetchall():
            ttt = data[1].split(' ')[1]
            ddd = data[1].split(' ')[0]
            curs.execute("select sub from rd where tnum = ? and stop = 'O'", [data[2]])
            if curs.fetchall():
                s = ' style="text-decoration: line-through"'
            else:
                s = ''
            if flask.request.args.get('skin', 'senkawa') == 'liberty':
                dv += '<li><a class="recent-item" href="/thread/' + url_pas(data[2]) + '"' + s + '>[<time datetime="' + ddd + 'T' + ttt + '.000Z" data-format="H:i:s">00:00:00</time>] ' + data[0] + '</a></li>'
            else:
                dv += '<a href="/thread/' + url_pas(data[2]) + '"' + s + '><span class="time"><time datetime="' + ddd + 'T' + ttt + '.000Z" data-format="H:i">00:00</time></span>' + data[0] + '</a>'

        return dv
    else:
        try:
            limit = int(flask.request.args.get('limit', '15'))
            if limit > 50:
                limit = 15
        except:
            limit = 15
        curs.execute("select title, date from history where not title like '사용자:%' and not title like '파일:%' and not title like '분류:%' and not hide = 'O' order by date desc limit ?", [limit])

        dv = ''
        for data in curs.fetchall():
            ttt = data[1].split(' ')[1]
            ddd = data[1].split(' ')[0]
            curs.execute("select title from data where title = ?", [data[0]])
            if not(curs.fetchall()):
                s = ' style="text-decoration: line-through"'
            else:
                s = ''
            if flask.request.args.get('skin', 'senkawa') == 'liberty':
                dv += '<li><a class="recent-item" href="/w/' + url_pas(data[0]) + '"' + s + '>[<time datetime="' + ddd + 'T' + ttt + '.000Z" data-format="H:i:s">00:00:00</time>] ' + data[0] + '</a></li>'
            else:
                dv += '<a href="/w/' + url_pas(data[0]) + '"' + s + '><span class="time"><time datetime="' + ddd + 'T' + ttt + '.000Z" data-format="H:i">00:00</time></span>' + data[0] + '</a>'

        return dv

def sidebarRecent(conn):
    curs = conn.cursor()
    limit = 15
    curs.execute("select title, date from history where not title like '사용자:%' and not title like '파일:%' and not title like '분류:%' and not hide = 'O' order by date desc limit ?", [300])
    rdata = curs.fetchall()
    dv = []
    c = 0
    ad = []
    for data in rdata:
        if str(data[0]) in ad:
            continue
        if c > limit:
            break
        c += 1

        curs.execute("select title from data where title = ?", [data[0]])
        if not(curs.fetchall()):
            status = "delete"
        else:
            status = "normal"
        dt = data[1]
        dv.append({
            "document": str(data[0]),
            "status": status,
            "date": int(time.mktime(datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").timetuple()))
        })
        ad.append(str(data[0]))
    return flask.jsonify(dv)
