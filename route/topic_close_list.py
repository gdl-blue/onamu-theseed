from .tool.func import *
from flask import Flask, request, render_template

def topic_close_list_2(conn, name, tool):
    curs = conn.cursor()
    
    if acl_check(name, 'render') == 1:
        return re_error('/error/3')
    
    div = ''
    
    if flask.request.method == 'POST':
        cny = format(request.form['conty'])
        
        curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm) values (?, ?, ?, ?, ?, ?, '', '', ?)", [1, name, flask.request.form.get('topic'), cny, get_time(), ip_check(), admin_check()])
        curs.execute("insert into rd (title, sub, date) values (?, ?, ?)", [name, flask.request.form.get('topic'), get_time()])
        conn.commit()

        return redirect('/topic/' + url_pas(name) + '/sub/' + url_pas(flask.request.form.get('topic')))
    else:
        plus = ''
        menu = [['topic/' + url_pas(name), load_lang('return')]]
        
        eq = ['']
        curs.execute("select num from erq where name = ? and state = 'open' order by time asc", [name])
        eq = curs.fetchall()
        
        if tool == 'close':
            curs.execute("select sub from rd where title = ? and stop = 'O' order by sub asc", [name])
            
            sub = load_lang('close') + ''
        elif tool == 'agree':
            curs.execute("select sub from rd where title = ? and agree = 'O' order by sub asc", [name])
            
            sub = load_lang('agreement') + ''
        elif tool == 'eqclose':
            curs.execute("select num from erq where name = ? and state = 'close' order by time asc", [name])
            
            sub = '닫힌 편집 요청'
        else:
            curs.execute("select sub from rd where title = ? order by date desc", [name])
            
            sub = load_lang('discussion_list')
            
            menu = [['w/' + url_pas(name), load_lang('document')]]
            
            plus =  '''
                    <a href="/topic/''' + url_pas(name) + '''/close">[''' + load_lang('close') + ''' 목록 보기]</a><br><a href="/topic/''' + url_pas(name) + '''/agree">[''' + load_lang('agreement') + '''된 토론 목록 보기]</a>
                    <br><br><h3 style="font-weight: 600; font-size: 1.6em; cursor: pointer; border: none; margin-top:12px; " onclick="var dsp = document.getElementById(\'newt\'); if(dsp.style.display == \'block\') dsp.style.display = \'none\'; else dsp.style.display = \'block\';">새 주제 생성</h3><div id="newt" style="display:block;">주제 : <br>
                    <input name="topic" type="text"><br>
                    내용 : <br>
                    <textarea name="conty" rows="5"></textarea>
                    <button type="submit" id="save" style="width:120px">전송</button></div>
                    '''
        cnt = 1
        if tool == 'close' or tool == 'agree' or tool == 'eqclose':
            div = '<ul>'
            edv = '<ul>'
        else:
            div = '<h3 style="font-weight: 600; font-size: 1.6em; cursor: pointer; border: none; " onclick="var ds = document.getElementById(\'tl\');if(ds.style.display==\'block\')ds.style.display=\'none\';else ds.style.display=\'block\';">토론</h3><ul id="tl" style="display:block;">'
            edv = '<h3 style="font-weight: 600; font-size: 1.6em; cursor: pointer; border: none; " onclick="var ds = document.getElementById(\'el\');if(ds.style.display==\'block\')ds.style.display=\'none\';else ds.style.display=\'block\';">편집 요청</h3><ul id="el" style="display:block;">'
        for data in curs.fetchall():
            if not(tool == 'eqclose'):
                curs.execute("select data, date, ip, block from topic where title = ? and sub = ? and id = '1'", [name, data[0]])
                if curs.fetchall():                
                    it_p = 0
                    
                    if sub == load_lang('discussion_list'):
                        curs.execute("select title from rd where title = ? and sub = ? and stop = 'O' order by sub asc", [name, data[0]])
                        if curs.fetchall():
                            it_p = 1
                    
                    if it_p != 1:
                        div += '<li><a href="#s-' + str(cnt) + '">' + str(cnt) + '</a>. <a href="/topic/' + url_pas(name) + '/sub/' + url_pas(data[0]) + '">' + data[0] + '</a></li>'
            else:
                div += '<li><a href="/edit_request/' + url_pas(data[0]) + '">편집 요청 ' + data[0] + '</a></li>'
            
            cnt += 1
        for data in eq:
            edv += '<li><a href="/edit_request/' + url_pas(data[0]) + '">편집 요청 ' + data[0] + '</a></li>'
        div += '</ul>'
        edv += '</ul><a href="/topic/''' + url_pas(name) + '/eqclose">[닫힌 편집 요청 보기]</a><br><br>'
        if div == '':
            plus = re.sub('^<br>', '', plus)
        if tool == 'close':
            edv = ''
        elif tool == 'agree':
            edv = ''
        elif tool == 'eqclose':
            edv = ''
        
        return easy_minify(flask.render_template(skin_check(), 
            imp = [name, wiki_set(), custom(), other2([' (' + sub + ')', 0])],
            data =  '<form method="post">' + edv + div + plus + '</form>',
            menu = menu,
            st = 3
        ))
