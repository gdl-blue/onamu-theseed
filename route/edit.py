from .tool.func import *

def edit_2(conn, name):
    curs = conn.cursor()
    
    
    if acl_check(name, 'render') == 1:
        return re_error('/error/3')

    ip = ip_check()
    #if acl_check(name) == 1:
     #   return re_error('/ban')
        
    
    
    if flask.request.method == 'POST':
        if captcha_post(flask.request.form.get('g-recaptcha-response', '')) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)
            
        if edit_filter_do(flask.request.form.get('content', '')) == 1:
            return re_error('/error/21')
        
        admin = admin_check(3)
        #if re.search('^사용자:', name):
         #   if name == '사용자:' + str(ip_check()):
          #      fdsfv = '12'
           # else:
            #    if admin == 1:
             #       fsdvfgh = '2'
              #  else:
               #     return re_error('/ban')
                    
        if acl_check(name) == 1:
            return re_error('/ban')
                    

        today = get_time()
        content = savemark(flask.request.form.get('content', ''))
        
        curs.execute("select data from data where title = ?", [name])
        old = curs.fetchall()
        if old:
            leng = leng_check(len(flask.request.form.get('otent', '')), len(content))
            
            if flask.request.args.get('section', None):
                content = old[0][0].replace(flask.request.form.get('otent', ''), content)
                
            curs.execute("update data set data = ? where title = ?", [content, name])
        else:
            leng = '+' + str(len(content))
            
            curs.execute("insert into data (title, data) values (?, ?)", [name, content])

        curs.execute("select user from scan where title = ?", [name])
        for _ in curs.fetchall():
            curs.execute("insert into alarm (name, data, date) values (?, ?, ?)", [ip, ip + ' - <a href="/w/' + url_pas(name) + '">' + name + '</a> (Edit)', today])

        history_plus(
            name,
            content,
            today,
            ip,
            flask.request.form.get('send', ''),
            leng
        )
        
        curs.execute("update data set date = ? where title = ?", [get_time(), name])
        
        curs.execute("delete from back where link = ?", [name])
        curs.execute("delete from back where title = ? and type = 'no'", [name])
        
        render_set(
            title = name,
            data = content,
            num = 1
        )
        
        conn.commit()
        
        return redirect('/w/' + url_pas(name))
    else:            
        curs.execute("select data from data where title = ?", [name])
        new = curs.fetchall()
        if new:
            if flask.request.args.get('section', None):
                test_data = '\n' + re.sub('\r\n', '\n', new[0][0]) + '\n'   
                
                section_data = re.findall('((?:={1,6}) ?(?:(?:(?!={1,6}\n).)+) ?={1,6}\n(?:(?:(?!(?:={1,6}) ?(?:(?:(?!={1,6}\n).)+) ?={1,6}\n).)*\n*)*)', test_data)
                data = section_data[int(flask.request.args.get('section', '1')) - 1]
            else:
                data = new[0][0]
        else:
            data = ''
            
        data_old = data
        
        if not flask.request.args.get('section', None):
            get_name = ''
            #get_name =  '''
                #<a href="/manager/15?plus=''' + url_pas(name) + '">[' + load_lang('load') + ']</a> <a href="/edit_filter">[' + load_lang('edit_filter_rule') + ''']</a>
                #<hr class=\"main_hr\">
            #'''
        else:
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
        if acl_check(name) == 1:
            fgeyhythtrt = ''' '''
            fdvsdvgbrtf = ''' readonly disabled style="background:#eceeef"'''
            dfnmgrtutei = '''<div id="balloon" style="padding:0.5rem 0.8rem; color:#a94442; background-color:#f2dede; border-color:#ebcccc; padding-right:30px; padding:10px; margin-bottom:1rem; border:1px solid #ebcccc; border-radius:.25rem;"><button type="button" class="close" data-dismiss="alert" aria-label="Close" style="color: #000;
                                font-size: 1.5rem!important;
                                margin-left: .5rem;top: 0;
                                right: 0;position: relative;-webkit-appearance: none;
                                padding: 0;
                                cursor: pointer;
                                background: 0 0;
                                border: 0;float: right;line-height: 1;text-shadow: 0 1px 0 #fff;
                                opacity: .2;font-weight: 700; font-family: open sans,arial,apple sd gothic neo,noto sans cjk kr,본고딕,kopubdotum medium,나눔바른고딕,나눔고딕,nanumgothic,맑은고딕,malgun gothic,sans-serif !important;" onclick="document.getElementById(\'balloon\').style.display = \'none\';" onmouseover="this.style.opacity = \'.5\';" onmouseout="this.style.opacity = \'.2\';">
                                <span aria-hidden="true">×</span>
                                <span class="sr-only">Close</span>
                                </button>''' + re_balloon('/ban', 1, name) + '''</div>'''
            err = 1

        return easy_minify(flask.render_template(skin_check(), 
            imp = [name, wiki_set(), custom(), other2([' (' + load_lang('edit') + ')', 0])],
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
            st = 2,
            err = err
        ))