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
    if not name:
        div += next_fix_f('/block_log?num=', num, data_list) + '<br><br>'
    else:
        div += next_fix_f('/' + url_pas(tool) + '/' + url_pas(name) + '?num=', num, data_list) + '<br><br>'
    div += '''
        <ul>
    '''
    
    

    curs.execute("delete from ban where (end < ? and end like '2%')", [get_time()])
    conn.commit()
    
    if not name:        
        if flask.request.args.get('type', '') == 'ongoing':
            sub = ' (' + load_lang('in_progress') + ')'
            menu = [['block_log', load_lang('normal')]]

            curs.execute("select why, block, '', end, '', band from ban where ((end > ? and end like '2%') or end = '') order by end desc limit ?, '100'", [get_time(), str(sql_num)])
        else:
            sub = 0
            menu = 0

            div = '''
                <form><select id="t">
<option value="/block_user/" selected>내용</option>
<option value="/block_admin/">실행자</option>
</select> <input type="text" id="q" placeholder="검색" value="" style="width:200px"> <input style="width:65px" type="button" onclick="location.href = document.getElementById('t').value + document.getElementById('q').value;" value="검색"></form>''' + div
              #  <div style="padding: .75rem 1rem;margin-bottom: 1rem;list-style: none;background-color: #eceeef;border-radius: .25rem;"><a href="/manager/11">[''' + load_lang('blocked') + ''']</a> <a href="/manager/12">[''' + load_lang('admin') + ''']</a> <a href="?type=ongoing">[''' + load_lang('in_progress') + ''']</a></div>
             #   <hr class=\"main_hr\">
            #''' + div
            
            curs.execute("select why, block, blocker, end, today, band from rb order by today desc limit ?, '100'", [str(sql_num)])
    else:
        menu = [['block_log', load_lang('normal')]]
        
        if tool == 'block_user':
            sub = ''
            
            curs.execute("select why, block, blocker, end, today, band from rb where block = ? order by today desc limit ?, '100'", [name, str(sql_num)])
        else:
            sub = ''
            
            curs.execute("select why, block, blocker, end, today, band from rb where blocker = ? order by today desc limit ?, '100'", [name, str(sql_num)])

    if data_list == '':
        data_list = curs.fetchall()

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
        if re.search(".*\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}.*",ip):
            ip = ip + '/32'
            iad = 1
        if re.search("\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}",ip):
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
            start = data[4]
            
        if re.search("\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}",ip):
            iad = 1
        
        if end == '차단 해제':
            #div += '''<div style="display:none"><li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (''' + end + ''' 까지) (''' + why.replace('<br>', '') + ''')</li></div>'''
            if iad == 1:
                div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(IP 주소 차단 해제)</i></li>'''
            else:
                div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단 해제)</i> (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''
        elif end == '무기한':
            #div += '''<div style="display:none"><li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (영구적으로) (''' + why.replace('<br>', '') + ''')</li></div>'''
            if iad == 1:
                div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(IP 주소 차단)</i> (영구적으로) (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''
            else:
                div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (영구적으로) (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''
        elif end == 'grant':
            div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 권한 설정)</i> (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''
        elif end == 'lh':
            div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 로그인 기록 조회)</i></li>'''
        if not(end == '차단 해제' or end == '무기한' or end == 'grant' or end == 'lh'):
            if len(str(end)) == 19:
                if iad == 1:
                    div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(IP 주소 차단)</i> (''' + end + ''' 까지) (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''
                else:
                    div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (''' + end + ''' 까지) (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''
            else:
                if iad == 1:
                    div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(IP 주소 차단)</i> (''' + end + ''' 동안) (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''
                else:
                    div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (''' + end + ''' 동안) (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''
            

    div += '</ul>'
    
    if not name:
        div += next_fix_f('/block_log?num=', num, data_list)
    else:
        div += next_fix_f('/' + url_pas(tool) + '/' + url_pas(name) + '?num=', num, data_list)
                
    return easy_minify(flask.render_template(skin_check(), 
        imp = [load_lang('recent_ban'), wiki_set(), custom(), other2([sub, 0])],
        data = div,
        menu = menu
    ))