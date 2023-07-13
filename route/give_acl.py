from .tool.func import *

def give_acl_2(conn, name):
    curs = conn.cursor()

    check_ok = ''
    
    if flask.request.method == 'POST':
        check_data = 'acl (' + name + ')'
    else:
        check_data = None
    
    user_data = re.search('^사용자:(.+)$', name)
    if user_data:
        if check_data and custom()[2] == 0:
            return redirect('/login')
        
        if user_data.groups()[0] != ip_check():
            if admin_check(5, check_data) != 1:
                if check_data:
                    return re_error('/error/3')
                else:
                    check_ok = 'disabled'
    else:
        if admin_check(5, check_data) != 1:
            if check_data:
                return re_error('/error/3')
            else:
                check_ok = 'disabled'

    if flask.request.method == 'POST':
        ip = ip_check()
        curs.execute("select data from data where title = ?", [name])
        data = curs.fetchall()
        today = get_time()
        leng = '-' + str(len(data[0][0]))
        
        dec = flask.request.form.get('dec', '')
        view = flask.request.form.get('view', '')

        curs.execute("select title from acl where title = ?", [name])
        if curs.fetchall():
            curs.execute("update acl set dec = ? where title = ?", [dec, name])
            curs.execute("update acl set dis = ? where title = ?", [flask.request.form.get('dis', ''), name])
            curs.execute("update acl set why = ? where title = ?", [flask.request.form.get('why', ''), name])
            curs.execute("update acl set view = ? where title = ?", [view, name])
        else:
            curs.execute("insert into acl (title, dec, dis, why, view) values (?, ?, ?, ?, ?)", [
                name, 
                dec, 
                flask.request.form.get('dis', ''), 
                flask.request.form.get('why', ''), 
                view
            ])
        
        if view == '':
            view = 'default'
        
        if dec == '':
            dec = 'default'
            
        if flask.request.form.get('dis', '') == '':
            dis = 'default'
        else:
            dis = flask.request.form.get('dis', '')
        
        if data:
            history_plus(
                name, 
                data[0][0], 
                get_time(), 
                ip_check(), 
                flask.request.form.get('why', ''), 
                '0',
                '' + dec + ',' + dis + ',' + view + '으로 ACL 변경'
            )

        else:
            history_plus(
                name, 
                '', 
                get_time(), 
                ip_check(), 
                flask.request.form.get('why', ''), 
                '0',
                '' + dec + ',' + dis + ',' + view + '으로 ACL 변경'
            )
        
        curs.execute("select title from acl where title = ? and dec = '' and dis = '' and view = ''", [name])
        if curs.fetchall():
            curs.execute("delete from acl where title = ?", [name])
        


        conn.commit()
            
        return redirect('/acl/' + url_pas(name))            
    else:
        data = ''
        #if re.search('^user:', name):
         #   acl_list = [['', 'normal'], ['user', 'member'], ['all', 'all']]
        #else:
        acl_list = [['', '(없음)'], ['all', '모두'], ['user', '로그인된 사용자'], ['admin', '관리자'], ['50_edit', '50회 편집'], ['email', '인증자']]
        #if not re.search('^사용자:', name):
        data += '<h2>' + '편집' + '</h2><select style="display:block;width:100%;" name="dec" ' + check_ok + '>'
    
        
        
        curs.execute("select dec from acl where title = ?", [name])
        acl_data = curs.fetchall()
        for data_list in acl_list:
            if acl_data and acl_data[0][0] == data_list[0]:
                check = 'selected="selected"'
            else:
                check = ''
            
            data += '<option value="' + data_list[0] + '" ' + check + '>' + data_list[1] + '</option>'
            
        data += '</select>'
        
        #if not re.search('^user:', name):
        data += '<h2>' + '토론 댓글' + '</h2><select style="display:block;width:100%;" name="dis" ' + check_ok + '>'
    
        curs.execute("select dis, why, view from acl where title = ?", [name])
        acl_data = curs.fetchall()
        for data_list in acl_list:
            if acl_data and acl_data[0][0] == data_list[0]:
                check = 'selected="selected"'
            else:
                check = ''
                
            data += '<option value="' + data_list[0] + '" ' + check + '>' + data_list[1] + '</option>'
            
        data += '</select>'

        data += '<h2>' + '읽기' + '</h2><select style="display:block;width:100%;" name="view" ' + check_ok + '>'
        for data_list in acl_list:
            if acl_data and acl_data[0][2] == data_list[0]:
                check = 'selected="selected"'
            else:
                check = ''
                
            data += '<option value="' + data_list[0] + '" ' + check + '>' + data_list[1] + '</option>'
            
        data += '''
            </select>
        '''#'''    <h2>''' + load_lang('explanation') + '''</h2>
           # <ul>
            #    <li>normal : ''' + load_lang('default') + '''</li>
             #   <li>admin : ''' + load_lang('admin_acl') + '''</li>
              #  <li>member : ''' + load_lang('member_acl') + '''</li>
               # <li>50 edit : ''' + load_lang('50_edit_acl') + '''</li>
                #<li>all : ''' + load_lang('all_acl') + '''</li>
           #     <li>all : ''' + load_lang('email_acl') + '''</li>
          #  </ul>
        #'''
            
        if check_ok == '':
            if acl_data:
                data += '<hr class=\"main_hr\"><input value="' + html.escape(acl_data[0][1]) + '" placeholder="' + load_lang('why') + '" name="why" type="text" ' + check_ok + '>'
            else:
                data += '<hr class=\"main_hr\"><input placeholder="요약" name="why" type="text" ' + check_ok + '>'
        
        return easy_minify(flask.render_template(skin_check(), 
            imp = [name, wiki_set(), custom(), other2([' (' + load_lang('acl') + ')', 0])],
            data =  '''
                <form method="post">
                    ''' + data + '''
                    <hr class=\"main_hr\">
                    <button type="submit" ''' + check_ok + '''>삽입</button>
                </form>
            ''',
            menu = [['w/' + url_pas(name), load_lang('document')], ['manager', load_lang('admin')]],
            st = 8
        ))