from .tool.func import *

def nerq_2(conn, name):
    curs = conn.cursor()

    ip = ip_check()
    #if acl_check(name) == 1:
     #   return re_error('/ban')
     
    if acl_check(name, 'render') == 1:
        return re_error('/error/3')
        
    if ban_check() == 1:
        return re_error('/ban')
    
    if flask.request.method == 'POST':
        if ban_check() == 1:
            return re_error('/ban')
        if captcha_post(flask.request.form.get('g-recaptcha-response', '')) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)

        if flask.request.form.get('otent', '') == flask.request.form.get('content', ''):
            return redirect('/w/' + url_pas(name))
            
        if edit_filter_do(flask.request.form.get('content', '')) == 1:
            return re_error('/error/21')
                    

        today = get_time()
        content = savemark(flask.request.form.get('content', ''))
        
        curs.execute("select data from data where title = ?", [name])
        old = curs.fetchall()
        if old:
            leng = leng_check(len(flask.request.form.get('otent', '')), len(content))
        else:
            leng = '+' + str(len(content))
        
        curs.execute("select l from leq where m = ?", ['1'])
        cn = curs.fetchall()
        if cn:
            curs.execute("select id from history where title = ? order by id + 0 desc limit 1", [name])
            id_data = curs.fetchall()
            pan = ''
            pan = str(int(id_data[0][0]) + 1) if id_data else '1'
            curs.execute("update leq set l = ? where m = ?", [str(int(cn[0][0]) + 1), '1'])
            curs.execute("insert into erq (name, num, send, leng, data, user, state, time, closer, y, pan, why) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [name, str(int(cn[0][0]) + 1), flask.request.form.get('send', ''), leng, content, ip_check(), 'open', get_time(), '', '', pan, ''])
    
            conn.commit()
            
            return redirect('/edit_request/' + url_pas(str(int(cn[0][0]) + 1)))
        else:
            cn = [['0']]
            curs.execute("select id from history where title = ? order by id + 0 desc limit 1", [name])
            id_data = curs.fetchall()
            pan = ''
            pan = str(int(id_data[0][0]) + 1) if id_data else '1'
            curs.execute("insert into leq (l, m) values (?, ?)", ['1','1'])
            curs.execute("insert into erq (name, num, send, leng, data, user, state, time, closer, y, pan, why) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [name, str(int(cn[0][0]) + 1), flask.request.form.get('send', ''), leng, content, ip_check(), 'open', get_time(), '', '', pan, ''])
    
            conn.commit()
            
            return redirect('/edit_request/' + url_pas(str(int(cn[0][0]) + 1)))
    else:            
        curs.execute("select data from data where title = ?", [name])
        new = curs.fetchall()
        if new:
            data = new[0][0]
        else:
            data = ''
            
        data_old = data
        get_name = ''
            
        if flask.request.args.get('plus', None):
            curs.execute("select data from data where title = ?", [flask.request.args.get('plus', 'test')])
            get_data = curs.fetchall()
            if get_data:
                data = get_data[0][0]
                get_name = ''

        curs.execute('select data from other where name = "edit_bottom_text"')
        sql_d = curs.fetchall()
        if sql_d and sql_d[0][0] != '':
            b_text = '<hr class=\"main_hr\">' + sql_d[0][0]
        else:
            b_text = ''
            
        dfnmgrtutei = ''' '''
        fdvsdvgbrtf = ''' '''
        fgeyhythtrt = '''<br><br>
                    요약<br>
                    <input name="send" type="text" style="width:100% !important;">
                    ''' + captcha_get() + '''<br><br><p>문서 편집을 <strong>저장</strong>하면 당신은 기여한 내용을 <strong>CC-BY-NC-SA 2.0 KR</strong>으로 배포하고 기여한 문서에 대한 하이퍼링크나 URL을 이용하여 저작자 표시를 하는 것으로 충분하다는 데 동의하는 것입니다. 이 <strong>동의는 철회할 수 없습니다.</strong></p><br>
                    <b>''' + ip_warring() + '''</b>취소선, 볼드체, 말 줄임표 등의 표현을 가독성에 문제가 생길 정도로 과도하게 사용하지 말아주시길 부탁드립니다.<br><br><button id="save" type="submit" style="width: 100px;">''' + load_lang('save') + '''</button>
                    <button style="display:none" id="preview" type="button" onclick="do_preview(\'''' + name + '\')">' + load_lang('preview') + '''</button>'''
        admin = admin_check(3)
        #if re.search('^사용자:', name):
         #   if name == '사용자:' + str(ip_check()):
          #      fdsfv = '12'
           # else:
            #    if admin == 1:
             #       fsdvfgh = '2'
              #  else:
               #     fgeyhythtrt = ''' '''
                #    fdvsdvgbrtf = ''' readonly disabled style="background:#eceeef"'''
                 #   dfnmgrtutei = '''<div style="padding:0.5rem 0.8rem; color:#a94442; background-color:#f2dede; border-color:#ebcccc; padding-right:30px; padding:10px; margin-bottom:1rem; border:1px solid #ebcccc; border-radius:.25rem;"><strong>[오류!]</strong> 자기 자신의 사용자 문서만 편집할 수 있습니다.</div>'''
        err = 0

        return easy_minify(flask.render_template(skin_check(), 
            imp = [name, wiki_set(), custom(), other2([' (' + load_lang('edit') + ' 요청)', 0])],
            data = get_name + '''
                <form method="post">
                    ''' + dfnmgrtutei + '''<ul class="nav nav-tabs" role="tablist" style="height: 43px;">
<li class="nav-item" style="list-style-type:none !important">
<a class="nav-link active" data-toggle="tab" href="#edit" role="tab" onclick="document.getElementById(\'content\').style.display = \'block\';document.getElementById(\'see_preview\').style.display = \'none\';">편집</a>
</li>
<li class="nav-item" style="list-style-type:none !important">
<a class="nav-link" data-toggle="tab" role="tab" aria-expanded="false" id="preview" onclick="do_preview(\'''' + name + '''\');document.getElementById(\'content\').style.display = \'none\';document.getElementById(\'see_preview\').style.display = \'block\';">미리보기</a>
</li>

</ul>
                    <textarea id="content" rows="25" id="content" name="content"''' + fdvsdvgbrtf + ''' style="width:100% !important;">''' + html.escape(re.sub('\n$', '', data)) + '''</textarea>
                    <div id="see_preview" style="overflow:auto;height:518px;border-radius: .25rem;padding: .5rem .75rem;display:none"></div>
                    <textarea style="display: none;" name="otent">''' + html.escape(re.sub('\n$', '', data_old)) + '''</textarea>
                    ''' + fgeyhythtrt + '''
                </form>
                ''' + b_text + '''
                
            ''',
            menu = [['w/' + url_pas(name), load_lang('return')], ['delete/' + url_pas(name), load_lang('delete')], ['move/' + url_pas(name), load_lang('move')]],
            st = 0,
            err = err
        ))
        