from .tool.func import *

def edit_delete_2(conn, name, app_var):
    curs = conn.cursor()
    
    if acl_check(name, 'render') == 1:
        return re_error('/error/3')

    ip = ip_check()
    if acl_check(name) == 1:
        return re_error('/ban')
    
    
    
    if flask.request.method == 'POST':
        if re.search('^사용자:', name):
            if admin_check() != 1:
                    return re_error('/error/1200')
        if not(flask.request.form.get('con', '')):
            return re_error('/error/1101')
        if captcha_post(flask.request.form.get('g-recaptcha-response', '')) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)

        curs.execute("select data from data where title = ?", [name])
        data = curs.fetchall()
        if data:
            if len(flask.request.form.get('send', '')) < 5:
                return re_error('/error/1100')
            
            today = get_time()
            leng = '-' + str(len(data[0][0]))
            
            history_plus(
                name, 
                '', 
                today, 
                ip, 
                flask.request.form.get('send', ''), 
                leng,
                '삭제'
            )
            
            curs.execute("select title, link from back where title = ? and not type = 'cat' and not type = 'no'", [name])
            for data in curs.fetchall():
                curs.execute("insert into back (title, link, type) values (?, ?, 'no')", [data[0], data[1]])
            
            curs.execute("delete from back where link = ?", [name])
            curs.execute("delete from data where title = ?", [name])
            conn.commit()

        file_check = re.search('^file:(.+)\.(.+)$', name)
        if file_check:
            file_check = file_check.groups()
            os.remove(os.path.join(
                app_var['path_data_image'],
                hashlib.sha224(bytes(file_check[0], 'utf-8')).hexdigest() + '.' + file_check[1]
            ))
            
        return redirect('/w/' + url_pas(name))
    else:
        curs.execute("select title from data where title = ?", [name])
        if not curs.fetchall():
            return redirect('/w/' + url_pas(name))

        return easy_minify(flask.render_template(skin_check(), 
            imp = [name, wiki_set(), custom(), other2([' (삭제)', 0])],
            data =  '''
                    <form method="post">
                        요약<br>
                        <input name="send" type="text"><br>
                        <input type="checkbox" style="width:20px" name="con"> 문서 이동 목적이 아닌, 삭제하기 위함을 확인합니다.<br><br>
                        <b>''' + ip_warring() + '''</b><br><br>
                        ''' + captcha_get() + '''
                        <button type="submit">''' + load_lang('delete') + '''</button>
                    </form>
                    ''',
            menu = [['w/' + url_pas(name), load_lang('return')]],
            st = 5
        ))     