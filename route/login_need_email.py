from .tool.func import *

def login_need_email_2(conn, tool):
    curs = conn.cursor()

    if flask.request.method == 'POST':
        if tool == 'pass_find':
            curs.execute("select id from user_set where id = ? and name = 'email' and data = ?", [
                flask.request.form.get('id', ''),
                flask.request.form.get('email', '')
            ])
            if curs.fetchall():
                flask.session['c_key'] = ''.join(random.choice("0123456789") for i in range(6))
                flask.session['c_id'] = flask.request.form.get('id', '')

                curs.execute('select data from other where name = "email_title"')
                sql_d = curs.fetchall()
                if sql_d and sql_d[0][0] != '':
                    t_text = html.escape(sql_d[0][0])
                else:
                    t_text = '[' + wiki_set()[0] + '] ' + ip_check() + '님의 아이디/비밀번호 찾기 메일 입니다. '

                curs.execute('select data from other where name = "email_text"')
                sql_d = curs.fetchall()
                if sql_d and sql_d[0][0] != '':
                    i_text = html.escape(sql_d[0][0]) + '\n\nKey : ' + flask.session['c_key']
                else:
                    i_text = '안녕하세요. ' + wiki_set()[0] + '입니다.\n' + ip_check() + '님의 아이디/비밀번호 찾기 메일입니다. 해당 계정의 비밀번호를 찾으시려면 아래 PIN 번호를 입력해주세요.\nPIN: ' + flask.session['c_key'] + '\n\n요청 아이피 : ' + ip_check()

                send_email(flask.request.form.get('email', ''), t_text, i_text)
                
                return redirect('/check_pass_key')
            else:
                return re_error('/error/12')
        else:
            if tool == 'email_change':
                flask.session['c_key'] = ''.join(random.choice("0123456789") for i in range(6))
                flask.session['c_id'] = ip_check()
                flask.session['c_pw'] = ''
            
            if 'c_id' in flask.session:
                main_email = ['naver.com', 'gmail.com', 'daum.net', 'hanmail.net', 'hanmail2.net']
                data = re.search('@([^@]+)$', flask.request.form.get('email', ''))
                if data:
                    data = data.groups()[0]

                    curs.execute("select html from html_filter where html = ? and kind = 'email'", [data])
                    if curs.fetchall() or (data in main_email):
                        curs.execute('select id from user_set where name = "email" and data = ?', [flask.request.form.get('email', '')])
                        if curs.fetchall():
                            flask.session.pop('c_id', None)
                            flask.session.pop('c_pw', None)
                            flask.session.pop('c_key', None)
                            
                            # user 대신 오류 화면 보여주게 수정 필요
                            return redirect('/user')
                        else:
                            curs.execute('select data from other where name = "email_title"')
                            sql_d = curs.fetchall()
                            if sql_d and sql_d[0][0] != '':
                                t_text = html.escape(sql_d[0][0])
                            else:
                                if tool == 'email_change':
                                    t_text = '[' + wiki_set()[0] + '] ' + ip_check() + '님의 이메일 변경 인증 메일 입니다. '
                                else:
                                    t_text = '[' + wiki_set()[0] + '] 계정 생성 이메일 주소 인증. '

                            curs.execute('select data from other where name = "email_text"')
                            sql_d = curs.fetchall()
                            if sql_d and sql_d[0][0] != '':
                                i_text = html.escape(sql_d[0][0]) + '\n\nKey : ' + flask.session['c_key']
                            else:
                                if tool == 'email_change':
                                    i_text = '안녕하세요. ' + wiki_set()[0] + '입니다. \n' + ip_check() + '님의 이메일 변경 인증 메일입니다.\n해당 아이디로 변경한게 맞으시면 아래 PIN 번호를 입력해주세요.\nPIN: ' + flask.session['c_key'] + '\n\n요청 아이피 : (미구현 기능)'
                                else:
                                    i_text = '안녕하세요. ' + wiki_set()[0] + ' 입니다.\n' + wiki_set()[0] + ' 계정 생성 이메일 인증 메일입니다.\n본인이 맞다면 아래 PIN 번호를 입력해주세요.\nPIN: ' + flask.session['c_key'] + '\n\n요청 아이피 : ' + ip_check()

                            send_email(flask.request.form.get('email', ''), t_text, i_text)
                            flask.session['c_email'] = flask.request.form.get('email', '')
                  
                            if tool == 'email_change':
                                return redirect('/email_replace')
                            else:
                                return redirect('/check_key')
                    else:
                        return redirect('/email_filter')
            
            return redirect('/user')
    else:
        if tool == 'pass_find':
            curs.execute('select data from other where name = "password_search_text"')
            sql_d = curs.fetchall()
            if sql_d and sql_d[0][0] != '':
                b_text = sql_d[0][0] + '<hr class=\"main_hr\">'
            else:
                b_text = ''

            return easy_minify(flask.render_template(skin_check(),    
                imp = [load_lang('password_search'), wiki_set(), custom(), other2([0, 0])],
                data =  b_text + '''
                        <form method="post">
                            <input placeholder="''' + load_lang('id') + '''" name="id" type="text">
                            <hr class=\"main_hr\">
                            <input placeholder="''' + load_lang('email') + '''" name="email" type="text">
                            <hr class=\"main_hr\">
                            <button type="submit">''' + load_lang('save') + '''</button>
                        </form>
                        ''',
                menu = [['user', load_lang('return')]]
            ))
        else:
            curs.execute('select data from other where name = "email_insert_text"')
            sql_d = curs.fetchall()
            if sql_d and sql_d[0][0] != '':
                b_text = sql_d[0][0] + '<hr class=\"main_hr\">'
            else:
                b_text = ''

            return easy_minify(flask.render_template(skin_check(),    
                imp = [load_lang('email'), wiki_set(), custom(), other2([0, 0])],
                data =  '''
                        <a href="/email_filter">(''' + load_lang('email_filter_list') + ''')</a>
                        <hr class=\"main_hr\">
                        ''' + b_text + '''
                        <form method="post">
                            <input placeholder="''' + load_lang('email') + '''" name="email" type="text">
                            <hr class=\"main_hr\">
                            <button type="submit">''' + load_lang('save') + '''</button>
                        </form>
                        ''',
                menu = [['user', load_lang('return')]]
            ))