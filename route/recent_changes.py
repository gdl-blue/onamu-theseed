from .tool.func import *

def recent_changes_2(conn, name, tool):
    curs = conn.cursor()
    cmp = ''
    rn = ''
    rnr = ''
    see = ''
    raw = ''
    ndc = ''
    
    if tool == 'history' and acl_check(name, 'render') == 1:
        return re_error('/error/3')
    
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

            <table id="main_table_set" class="table table-hover" style="width:100%">
            <colgroup>
<col>
<col style="width: 25%;">
<col style="width: 22%;">
</colgroup>
                <tbody>
                    <tr style="border-top:1px solid #eceeef;border-bottom:2px solid #eceeef;line-height:30px">
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
                    <ul>
                '''
                
                # 기본적인 move만 구현
                tool_select = flask.request.args.get('tool', None)
                if tool_select:
                    if tool_select == 'move':
                        curs.execute('''
                            select id, title, date, ip, send, leng, i from history
                            where send like ? or send like ?
                            order by id + 0 desc
                            limit ?, '30'
                        ''', ['%(<a>' + name +'</a>%', '%<a>' + name + '</a> move)', str(sql_num)])
                    else:
                        curs.execute('''
                            select id, title, date, ip, send, leng, i from history
                            where title = ?
                            order by id + 0 desc
                            limit ?, '30'
                        ''', [name, str(sql_num)])
                else:
                    curs.execute('''
                        select id, title, date, ip, send, leng, i from history
                        where title = ?
                        order by id + 0 desc
                        limit ?, '30'
                    ''', [name, str(sql_num)])
            else:
                div +=  '''
                        <td id="main_table_width"><b>''' + '문서' + '''</b></td>
                        <td id="main_table_width"><b>''' + '수정자' + '''</b></td>
                        <td id="main_table_width"><b>''' + '수정 시간' + '''</b></td>
                    </tr>
                '''

                div = '<div style="padding: .75rem 1rem;margin-bottom: 1rem;list-style: none;background-color: #eceeef;border-radius: .25rem;"><a href="/contribution/author/' + url_pas(name) + '/document">[문서]</a><a href="/contribution/author/' + url_pas(name) + '/discuss"> [토론]</a></div>' + div
                
                curs.execute("select id, title, date, ip, send, leng from history where ip = ? order by date desc limit ?, '30'", [name, str(sql_num)])
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
                        <td id="main_table_width"><b>''' + '항목' + '''</b></td>
                        <td id="main_table_width"><b>''' + '수정자' + '''</b></td>
                        <td id="main_table_width"><b>''' + '수정 시간' + '''</b></td>
                    </tr>
                '''

            div = '<div style="padding: .75rem 1rem;margin-bottom: 1rem;list-style: none;background-color: #eceeef;border-radius: .25rem;"><a href="/RecentChanges">[전체]</a>　<a href="?set=user">[' + load_lang('user_document') + ']</a></div>' + div

            curs.execute('''
                select id, title, date, ip, send, leng from history 
                where not title like '사용자:%' 
                order by date desc 
                limit ?, 30
            ''', [str(sql_num)])

        data_list = curs.fetchall()
        for data in data_list:    
            select += '<option value="' + data[0] + '">' + data[0] + '</option>'     
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
                
            ip = ip_pas(data[3])
            if tool == 'history':
                if int(data[0]) - 1 == 0:
                    revert = ' <a href="/revert/' + url_pas(data[1]) + '?num=' + str(int(data[0])) + '">이 리비젼으로 ' + load_lang('revert') + '</a>'
                else:
                    if int(data[0]) == 1:
                        dsfdsd = ''
                    else:
                        cmp = ' | <a href="/diff/' + url_pas(data[1]) + '?first=' + str(int(data[0]) - 1) + '&second=' + data[0] + '">' + load_lang('compare') + '</a>'
                    revert = ' <a href="/revert/' + url_pas(data[1]) + '?num=' + str(int(data[0])) + '">이 리비젼으로 ' + load_lang('revert') + '</a>'
            else:
                revert = ''
            
            style = ['', '']
            date = data[2]

            curs.execute('''
                select title from history
                where title = ? and id = ? and hide = 'O'
            ''', [data[1], data[0]])
            hide = curs.fetchall()
            
            if six_admin == 1:
                if hide:   
                    if tool == 'history':
                        hidden = ' <a href="/hidden/' + url_pas(data[1]) + '?num=' + data[0] + '">[' + load_lang('hide_release') + ']</a>'
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
                        hidden = ' <a href="/hidden/' + url_pas(data[1]) + '?num=' + data[0] + '">[' + load_lang('hide') + ']</a>'
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
                see = '<a href="/w/' + url_pas(name) + '?num=' + data[0] + '">보기</a> '
                raw = '<a href="/raw/' + url_pas(name) + '?num=' + data[0] + '">' + load_lang('raw') + '</a> '
            else:
                title = '<a href="/w/' + url_pas(data[1]) + '">' + html.escape(data[1]) + '</a> '
                title += '<a href="/history/' + url_pas(data[1]) + '">[역사]</a> '
                if int(data[0]) > 1:
                    title += '<a href="/diff/' + url_pas(data[1]) + '?first=' + str(int(data[0]) - 1) + '&second=' + data[0] + '">[비교]</a> '
                title += '<a href="/topic/' + url_pas(data[1]) + '">[토론]</a> '

            if tool == 'history':
                ita = ''
                snd = send_parser_h(send)
                if re.search(" [(]<i>.*</i>[)]", send_parser_h(send)):
                    ita = '<i>' + re.findall(" [(]<i>.*</i>[)]") + '</i>'
                    snd.replace(re.findall(" [(]<i>.*</i>[)]"), '')
                if rnr == '1':
                    ndc = '<i> (새 문서)</i>'
                    cmp = ''
                if send_parser_h(send) == '[숨기기]':
                    if six_admin == 1:
                        div += '''<li>''' + date + '''
                            <span style="font-size: 8pt;">
                            (''' + see + ''' | ''' + raw + ''' | ''' + revert + cmp + ''')</span> <input name="a" type="radio" style="width:20px" onclick="document.getElementById('a').value=\'''' + str(rnr) + '''\';"><input name="b" type="radio" style="width:20px" onclick="document.getElementById('b').value=\'''' + str(rnr) + '''\';">''' + ndc + data[6] + ''' <b>''' + rn + '''</b> ''' + leng + ''' ''' + ip + ban + hidden + ''' (<span style="color:gray">''' + snd + '''</span>)</li>
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
                    div += '''<li>''' + date + '''
                        <span style="font-size: 8pt;">
                        (''' + see + ''' | ''' + raw + ''' | ''' + revert + cmp + ''')</span> <input name="a" type="radio" style="width:20px" onclick="document.getElementById('a').value=\'''' + str(rnr) + '''\';"><input type="radio" name="b" style="width:20px" onclick="document.getElementById('b').value=\'''' + str(rnr) + '''\';">''' + ndc + data[6] + ''' <b>''' + rn + '''</b> ''' + leng + ''' ''' + eq + ''' ''' + ip + ban + hidden + ''' (<span style="color:gray">''' + snd + '''</span>)</li>
                    '''
            else:
                curs.execute("select i from history where title = ? and id = ?", [data[1], data[0]])
                ii = curs.fetchall()
                title = title.replace('category:', '분류:')
                title = title.replace('file:', '파일:')
                div +=  '''
                    <tr ''' + style[0] + ''' style="line-height:30px" onmouseover="this.style.backgroundColor='#efefef';" onmouseout="this.style.backgroundColor='#ffffff';">
                        <td>''' + title + revert + ' ' + leng + '''</td>
                        <td>''' + ip + ban + hidden + '''</td>
                        <td>''' + date + '''</td>
                    </tr>'''
                
                if send_parser(send) == '<br>':
                    if ii and ii[0][0] == '':
                        dfadsfgasd = 2
                    else:
                        if ii:
                            div += '''<tr ''' + style[1] + ''' style="line-height:30px" onmouseover="this.style.backgroundColor='#efefef';" onmouseout="this.style.backgroundColor='#ffffff';">
                                <td colspan="3">''' + ii[0][0] + '''</td>
                            </tr>'''
                    if not(int(data[0]) > 1):
                        div += '''<tr ''' + style[1] + ''' style="line-height:30px" onmouseover="this.style.backgroundColor='#efefef';" onmouseout="this.style.backgroundColor='#ffffff';">
                            <td colspan="3">''' + send_parser_h(send) + ''' <i>(새 문서)</i></td>
                        </tr>'''
                else:
                    if int(data[0]) > 1:
                        if ii:
                            div += '''<tr ''' + style[1] + ''' style="line-height:30px" onmouseover="this.style.backgroundColor='#efefef';" onmouseout="this.style.backgroundColor='#ffffff';">
                                <td colspan="3">''' + send_parser_h(send) + ''' ''' + ii[0][0] + '''</td>
                            </tr>'''
                        else:
                            div += '''<tr ''' + style[1] + ''' style="line-height:30px" onmouseover="this.style.backgroundColor='#efefef';" onmouseout="this.style.backgroundColor='#ffffff';">
                                <td colspan="3">''' + send_parser_h(send) + '''</td>
                            </tr>'''
                    else:
                        div += '''<tr ''' + style[1] + ''' style="line-height:30px" onmouseover="this.style.backgroundColor='#efefef';" onmouseout="this.style.backgroundColor='#ffffff';">
                            <td colspan="3">''' + send_parser_h(send) + ''' <i>(새 문서)</i></td>
                        </tr>'''
                        

        if tool == 'history':
            div += '''</ul>'''
        else:
            div +=  '''
                    </tbody>
                </table>
            '''
        sub = ''

        if name:
            if tool == 'history':
                if not tool_select:
                    div = '''
                        
                        
                    ''' + div
                    #<div style="padding: .75rem 1rem;margin-bottom: 1rem;list-style: none;background-color: #eceeef;border-radius: .25rem;"><a href="?tool=move">[''' + load_lang('move') + ''']</a></div>
                    
                div = '''
                    <form method="post">
                        <div style="display:none"><select name="a" id="a">''' + select + '''</select> <select name="b" id="b">''' + select + '''</select></div>
                        <button type="submit">선택 리비젼 ''' + load_lang('compare') + '''</button><br><br>
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
                
                menu = [['other', load_lang('other')], ['user', load_lang('user')], ['count/' + url_pas(name), load_lang('count')]]
                
                div += next_fix_f('/contribution/author/' + url_pas(name) + '/document?num=', num, data_list)
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
                st = 7
            ))
        else:
            return easy_minify(flask.render_template(skin_check(), 
                imp = [title, wiki_set(), custom(), other2([sub, 0])],
                data = div,
                menu = menu
            ))