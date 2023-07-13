from .tool.func import *

def list_block_2(conn, name, tool):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 100 > 0:
        sql_num = num * 100 - 100
    else:
        sql_num = 0
    data_list = ''
    div = ''

    div += '''
        <ul class="wiki-list">
    '''



    curs.execute("delete from ban where (end < ? and end like '2%')", [get_time()])
    conn.commit()

    if flask.request.args.get('type', '') == 'ongoing':
        sub = ' (' + load_lang('in_progress') + ')'
        menu = [['block_log', load_lang('normal')]]

        curs.execute("select why, block, '', end, '', band from ban where ((end > ? and end like '2%') or end = '') order by end desc limit ?, '100'", [get_time(), str(sql_num)])
    else:
        sub = 0
        menu = 0


        curs.execute("select why, block, blocker, end, today, band, ipacl from rb order by today desc limit ?, '100'", [str(sql_num)])
    if flask.request.args.get('target', None):
        menu = [['BlockHistory', '검색 취소']]

        if flask.request.args.get('target', '') == 'text':
            sub = ''
            qqq = flask.request.args.get('query', '')
            qqq = re.sub('[*]', '%', qqq)
            qqq = re.sub('[?]', '_', qqq)
            curs.execute("select why, block, blocker, end, today, band, ipacl from rb where block like ? || '%' or why like ? || '%' order by today desc limit ?, '100'", [qqq, qqq, str(sql_num)])
        else:
            sub = ''
            qqq = flask.request.args.get('query', '')
            qqq = re.sub('[*]', '%', qqq)
            qqq = re.sub('[?]', '_', qqq)
            curs.execute("select why, block, blocker, end, today, band, ipacl from rb where blocker = ? order by today desc limit ?, '100'", [qqq, str(sql_num)])
    div = '''
                <form method=get><select name=target> <option value=text>내용 </option><option value=author>실행자 </option></select> <input type="text" name=query id="q" placeholder="검색" value=""> <input type=submit value="검색"></form>'''
              #  <div style="padding: .75rem 1rem;margin-bottom: 1rem;list-style: none;background-color: #eceeef;border-radius: .25rem;"><a href="/manager/11">[''' + load_lang('blocked') + ''']</a> <a href="/manager/12">[''' + load_lang('admin') + ''']</a> <a href="?type=ongoing">[''' + load_lang('in_progress') + ''']</a></div>
             #   <hr class=\"main_hr\">
            #''' + div
    if data_list == '':
        data_list = curs.fetchall()

    if not name:
        div += next_fix('/BlockHistory?num=', num, data_list, 100) + '<ul class="wiki-list">'
    else:
        div += next_fix('/' + url_pas(tool) + '/' + url_pas(name) + '?num=', num, data_list, 100) + '<ul class="wiki-list">'

    for data in data_list:
        why = html.escape(data[0])
        if why == '':
            why = '<br>'
        iad = 0
        if data[5] == 'O':
            ip = data[1] + ' (' + load_lang('range') + ')'
        elif data[5] == 'regex':
            ip = data[1] + ' (' + load_lang('regex') + ')'
        else:
            ip = ip_pas_raw(data[1])
        if data[6] == '1':
            iad = 1


        if data[3] == '':
            end = load_lang('limitless')
        elif data[3] == 'release':
            end = load_lang('release')
        else:
            end = data[3]


        if data[2] == '':
            admin = '알 수 없는'
        elif re.search('^tool:', data[2]):
            admin = data[2]
        elif re.search('^도구:', data[2]):
            admin = data[2]
        else:
            admin = ip_pas(data[2])

        if data[4] == '':
            start = ''
        else:
            start2 = data[4]
            ddd = start2.split(' ')[0]
            ttt = start2.split(' ')[1]
            start = '<time datetime="' + ddd + 'T' + ttt + '.000Z" data-format="Y-m-d H:i:s">' + start2 + '</time>'


        if end == '차단 해제':
            #div += '''<div style="display:none"><li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (''' + end + ''' 까지) (''' + why.replace('<br>', '') + ''')</li></div>'''
            if iad == 1:
                div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(IP 주소 차단 해제)</i></li>'''
            else:
                div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단 해제)</i> (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''
        elif end == '무기한' or end == '0':
            #div += '''<div style="display:none"><li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (영구적으로) (''' + why.replace('<br>', '') + ''')</li></div>'''
            if iad == 1:
                div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(IP 주소 차단)</i> (영구적으로) (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''
            else:
                div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (영구적으로) (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''
        elif end == 'grant':
            div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 권한 설정)</i> (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''
        elif end == 'lh':
            div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 로그인 기록 조회)</i></li>'''
        if not(end == '차단 해제' or end == '무기한' or end == '0' or end == 'grant' or end == 'lh'):
            unt = end + '초'
            try:
                if int(end) % 604800 == 0:
                    unt = str(int(end) // 604800) + '주'
                if int(end) % 86400 == 0:
                    unt = str(int(end) // 86400) + '일'
                if int(end) % 3600 == 0:
                    unt = str(int(end) // 3600) + '시간'
                if int(end) % 60 == 0:
                    unt = str(int(end) // 60) + '분'
            except:
                pass

            if end == '31104000':
                unt = '48주'
            elif end == '2592000':
                unt = '4주'
            elif end == '60':
                unt = '1분'
            elif end == '180':
                unt = '3분'
            elif end == '300':
                unt = '5분'
            elif end == '600':
                unt = '10분'
            elif end == '1800':
                unt = '30분'
            elif end == '3600':
                unt = '1시간'
            elif end == '7200':
                unt = '2시간'
            elif end == '86400':
                unt = '1일'
            elif end == '259200':
                unt = '3일'
            elif end == '432000':
                unt = '5일'
            elif end == '604800':
                unt = '1주'
            elif end == '1209600':
                unt = '2주'
            elif end == '1814400':
                unt = '3주'
            elif end == '15552000':
                unt = '6개월'
            if iad == 1:
                div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(IP 주소 차단)</i> (''' + unt + ''' 동안) (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''
            else:
                div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (''' + unt + ''' 동안) (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''


    div += '</ul>'

    if not name:
        div += next_fix('/BlockHistory?num=', num, data_list, 100)
    else:
        div += next_fix('/' + url_pas(tool) + '/' + url_pas(name) + '?num=', num, data_list, 100)

    return easy_minify(flask.render_template(skin_check(),
        imp = [load_lang('recent_ban'), wiki_set(), custom(), other2([sub, 0])],
        data = div,
        menu = menu
    ))