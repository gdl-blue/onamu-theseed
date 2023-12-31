from .tool.func import *

def setting_2(conn, num):
    curs = conn.cursor()

    if num != 0 and admin_check() != 1:
        return re_error('/ban')

    if num == 0:
        li_list = [
            load_lang('main_setting'),
            load_lang('text_setting'),
            load_lang('main_head'),
            load_lang('main_body'),
            'robots.txt',
            'Google'
        ]

        x = 0

        li_data = ''

        for li in li_list:
            x += 1
            li_data += '<li><a href="/setting/' + str(x) + '">' + li + '</a></li>'

        return easy_minify(flask.render_template(skin_check(),
            imp = [load_lang('setting'), wiki_set(), custom(), other2([0, 0])],
            data = '<h2>' + load_lang('list') + '</h2><ul>' + li_data + '</ul>',
            menu = [['manager', load_lang('return')]]
        ))
    elif num == 1:
        i_list = {
            0 : 'name',
            1 : 'logo',
            2 : 'frontpage',
            3 : 'license',
            4 : 'upload',
            5 : 'skin',
            6 : 'edit',
            7 : 'reg',
            8 : 'ip_view',
            9 : 'back_up',
            10 : 'port',
            11 : 'key',
            12 : 'update',
            13 : 'email_have',
            14 : 'discussion',
            15 : 'encode',
            16 : 'host',
            17 : 'upload_template',
            18 : 'edit_warning',
            19 : 'site_notice',
            20 : 'privacy'
        }
        n_list = {
            0 : 'Wiki',
            1 : '',
            2 : 'Wiki:대문',
            3 : '모든 문서는 CC-0에 따라 사용할 수 있습니다.',
            4 : '2',
            5 : '',
            6 : 'normal',
            7 : '',
            8 : '',
            9 : '0',
            10 : '80',
            11 : 'test',
            12 : 'stable',
            13 : '',
            14 : 'normal',
            15 : 'sha3',
            16 : '127.0.0.1',
            17 : '',
            18 : '문서 편집을 저장하면 당신은 기여한 내용을 CC-0으로 배포하고 기여한 문서에 대한 하이퍼링크나 URL을 이용하여 저작자 표시를 하는 것으로 충분하다는 데 동의하는 것입니다. 이 동의는 철회할 수 없습니다.',
            19 : '',
            20 : ''
        }

        if flask.request.method == 'POST':
            for i in i_list:
                curs.execute("update other set data = ? where name = ?", [
                    flask.request.form.get(i_list[i], n_list[i]),
                    i_list[i]]
                )

            conn.commit()

            admin_check(None, 'edit_set')

            return redirect('/admin/config')
        else:
            d_list = []

            for i in i_list:
                curs.execute('select data from other where name = ?', [i_list[i]])
                sql_d = curs.fetchall()
                if sql_d:
                    d_list += [sql_d[0][0]]
                else:
                    curs.execute('insert into other (name, data) values (?, ?)', [i_list[i], n_list[i]])

                    d_list += [n_list[i]]

            conn.commit()

            div = ''
            acl_list = [
                [load_lang('member'), 'login'],
                [load_lang('ip'), 'normal'],
                [load_lang('admin'), 'admin']
            ]
            for i in acl_list:
                if i[1] == d_list[6]:
                    div = '<option value="' + i[1] + '">' + i[0] + '</option>' + div
                else:
                    div += '<option value="' + i[1] + '">' + i[0] + '</option>'

            div4 = ''
            for i in acl_list:
                if i[1] == d_list[14]:
                    div4 = '<option value="' + i[1] + '">' + i[0] + '</option>' + div4
                else:
                    div4 += '<option value="' + i[1] + '">' + i[0] + '</option>'

            ch_1 = ''
            if d_list[7]:
                ch_1 = 'checked="checked"'

            ch_2 = ''
            if d_list[8]:
                ch_2 = 'checked="checked"'

            ch_3 = ''
            if d_list[13]:
                ch_3 = 'checked="checked"'

            div2 = load_skin(d_list[5])

            div3 =''
            if d_list[12] == 'stable':
                div3 += '<option value="stable">stable</option>'
                div3 += '<option value="master">master</option>'
            else:
                div3 += '<option value="master">master</option>'
                div3 += '<option value="stable">stable</option>'

            div5 =''
            encode_data = [['sha256', 'SHA-256'], ['sha3', 'SHA-3']]
            for i in encode_data:
                if d_list[15] == i[0]:
                    div5 = '<option value="' + i[0] + '">' + i[1] + '</option>' + div5
                else:
                    div5 += '<option value="' + i[0] + '">' + i[1] + '</option>'

            return easy_minify(flask.render_template(skin_check(),
                imp = [wiki_set()[0] + ' 등록 정보', wiki_set(), custom(), other2([0, 0])],
                data = '''
                    <form method="post" class=settings-section>
                        <div class=form-group>
                            <script>
                                $(function() {
                                    $("#sitenameInput").on("change paste keyup input", function() {
                                        $('#frontpageInput').val($(this).val() + ':대문');
                                    });
                                });
                            </script>
                            <label>''' + load_lang('wiki_name') + ''' : </label>
                            <input type="text" id=sitenameInput name="name" class=form-control value="''' + html.escape(d_list[0]) + '''">
                        </div>
                        <div class=form-group>
                            <label>''' + load_lang('wiki_logo') + ''' (HTML) : </label>
                            <input type="text" name="logo" class=form-control value="''' + html.escape(d_list[1]) + '''">
                        </div>
                        <div class=form-group>
                            <label>''' + load_lang('main_page') + ''' : </label>
                            <input type="text" id=frontpageInput name="frontpage" class=form-control readonly value="''' + html.escape(d_list[2]) + '''">
                        </div>
                        <div class=form-group>
                            <label>라이선스 경고 문구(HTML) : </label>
                            <textarea name=license class=form-control rows=7>''' + html.escape(d_list[3]) + '''</textarea>
                        </div>
                        <div class=form-group>
                            <label>''' + load_lang('max_file_size') + ''' (MB) : </label>
                            <input type="text" name="upload" class=form-control value="''' + html.escape(d_list[4]) + '''">
                        </div>
                        <div class=form-group>
                            <label>''' + load_lang('backup_interval') + ' (' + load_lang('hour') + ''') (비활성화: 0; 재시작 필요) : </label>
                            <input type="text" class=form-control name="back_up" value="''' + html.escape(d_list[9]) + '''">
                        </div>
                        <div class=form-group>
                            <label>기본 스킨 : </label>
                            <select name="skin" class=form-control>''' + div2 + '''</select>
                        </div>
                        <div style="display:none">
                        <span>''' + load_lang('default_acl') + '''</span>
                        <hr class=\"main_hr\">
                        <select name="edit">''' + div + '''</select>
                        <hr class=\"main_hr\">
                        <span>''' + load_lang('default_discussion_acl') + '''</span>
                        <hr class=\"main_hr\">
                        <select name="discussion">''' + div4 + '''</select>
                        </div>
                        <div class=form-group>
                            <label><input type="checkbox" name="reg" ''' + ch_1 + '''> ''' + load_lang('no_register') + '''</label><br>
                            <label><input type="checkbox" name="ip_view" ''' + ch_2 + '''> ''' + load_lang('hide_ip') + '''</label><br>
                            <label><input type="checkbox" name="email_have" ''' + ch_3 + '''> 가입시 전자우편 인증 요구</label> (<a href="/setting/6">''' + load_lang('google_imap_required') + '''</a>)
                        </div>
                        <div class=form-group>
                            <label>''' + load_lang('wiki_host') + ''' : </label>
                            <input type="text" name="host" class=form-control value="''' + html.escape(d_list[16]) + '''">
                        </div>
                        <div class=form-group>
                            <label>''' + load_lang('wiki_port') + ''' : </label>
                            <input type="text" name="port" class=form-control value="''' + html.escape(d_list[10]) + '''">
                        </div>
                        <div class=form-group>
                            <label>''' + load_lang('wiki_secret_key') + ''' : </label>
                            <input type="password" name="key" class=form-control value="''' + html.escape(d_list[11]) + '''">
                        </div>
                        <div style="display:none">
                        <span>''' + load_lang('update_branch') + '''</span>
                        <hr class=\"main_hr\">
                        <select name="update">''' + div3 + '''</select>
                        </div>
                        <div class=form-group>
                            <label>''' + load_lang('encryption_method') + ''' : </label>
                            <select name="encode" class=form-control>''' + div5 + '''</select>
                        </div>
                        <div class=form-group>
                            <label>파일 올리기 템플릿 : </label>
                            <textarea name=upload_template class=form-control rows=15>''' + html.escape(d_list[17]) + '''</textarea>
                        </div>
                        <div class=form-group>
                            <label>편집 라이선스 경고 문구 : </label>
                            <input type=text name=edit_warning class=form-control value="''' + html.escape(d_list[18]) + '''">
                        </div>
                        <div class=form-group>
                            <label>공지글 : </label>
                            <input type=text name=site_notice class=form-control placeholder="(공지 없음)" value="''' + html.escape(d_list[19]) + '''">
                        </div>
                        <div class=form-group>
                            <label>개인정보처리방침 : </label>
                            <textarea name=privacy class=form-control rows=15>''' + html.escape(d_list[20]) + '''</textarea>
                        </div>
                        <div class=form-group>
                            <label>기타 설정</label>
                            <ul class=wiki-list>
                                <li><a href="/admin/global_head">전역 &lt;HEAD&gt;</a></li>
                                <li><a href="/admin/robots">ROBOTS.TXT</a></li>
                                <li><a href="/admin/google">Google 설정</a></li>
                                <li><a href="/admin/username_filters">사용자 이름 필터</a></li>
                                <li><a href="/admin/edit_filters">편집 필터</a></li>
                                <li><a href="/admin/namespaces">이름공간 관리자</a></li>
                            </ul>
                        </div>
                        <div class=btns>
                            <button class="btn btn-secondary" type=reset>초기화</button>
                            <button class="btn btn-primary" type="submit">''' + load_lang('save') + '''</button>
                        </div>
                    </form>
                ''',
                menu = [['setting', load_lang('return')], ['admin/username_filters', 'ID필터'], ['admin/google', 'Google'], ['admin/robots', 'ROBOTS.TXT'], ['admin/global_head', '전역HEAD']]
            ))
    elif num == 2:
        i_list = [
            'contract',
            'no_login_warring',
            'edit_bottom_text',
            'check_key_text',
            'email_title',
            'email_text',
            'email_insert_text',
            'password_search_text',
            'reset_user_text'
        ]
        if flask.request.method == 'POST':
            for i in i_list:
                curs.execute("update other set data = ? where name = ?", [
                    flask.request.form.get(i, ''),
                    i
                ])

            conn.commit()

            admin_check(None, 'edit_set')

            return redirect('/setting/2')
        else:
            d_list = []

            for i in i_list:
                curs.execute('select data from other where name = ?', [i])
                sql_d = curs.fetchall()
                if sql_d:
                    d_list += [sql_d[0][0]]
                else:
                    curs.execute('insert into other (name, data) values (?, ?)', [i, ''])

                    d_list += ['']

            conn.commit()

            return easy_minify(flask.render_template(skin_check(),
                imp = [load_lang('text_setting'), wiki_set(), custom(), other2([0, 0])],
                data = '''
                    <form method="post">
                        <span>''' + load_lang('register_text') + ''' (HTML)</span>
                        <hr class=\"main_hr\">
                        <input name="''' + i_list[0] + '''" value="''' + html.escape(d_list[0]) + '''">
                        <hr class=\"main_hr\">
                        <span>''' + load_lang('non_login_alert') + ''' (HTML)</span>
                        <hr class=\"main_hr\">
                        <input name="''' + i_list[1] + '''" value="''' + html.escape(d_list[1]) + '''">
                        <hr class=\"main_hr\">
                        <span>''' + load_lang('edit_bottom_text') + ''' (HTML)</span>
                        <hr class=\"main_hr\">
                        <input name="''' + i_list[2] + '''" value="''' + html.escape(d_list[2]) + '''">
                        <hr class=\"main_hr\">
                        <span>''' + load_lang('check_key_text') + ''' (HTML)</span>
                        <hr class=\"main_hr\">
                        <input name="''' + i_list[3] + '''" value="''' + html.escape(d_list[3]) + '''">
                        <hr class=\"main_hr\">
                        <span>''' + load_lang('email_title') + '''</span>
                        <hr class=\"main_hr\">
                        <input name="''' + i_list[4] + '''" value="''' + html.escape(d_list[4]) + '''">
                        <hr class=\"main_hr\">
                        <span>''' + load_lang('email_text') + '''</span>
                        <hr class=\"main_hr\">
                        <input name="''' + i_list[5] + '''" value="''' + html.escape(d_list[5]) + '''">
                        <hr class=\"main_hr\">
                        <span>''' + load_lang('email_insert_text') + '''</span>
                        <hr class=\"main_hr\">
                        <input name="''' + i_list[6] + '''" value="''' + html.escape(d_list[6]) + '''">
                        <hr class=\"main_hr\">
                        <span>''' + load_lang('password_search_text') + '''</span>
                        <hr class=\"main_hr\">
                        <input name="''' + i_list[7] + '''" value="''' + html.escape(d_list[7]) + '''">
                        <hr class=\"main_hr\">
                        <span>''' + load_lang('reset_user_text') + '''</span>
                        <hr class=\"main_hr\">
                        <input name="''' + i_list[8] + '''" value="''' + html.escape(d_list[8]) + '''">
                        <hr class=\"main_hr\">
                        <button id="save" type="submit">''' + load_lang('save') + '''</button>
                    </form>
                ''',
                menu = [['setting', load_lang('return')]]
            ))
    elif num == 3 or num == 4:
        if flask.request.method == 'POST':
            if num == 4:
                info_d = 'body'
                end_r = '4'
                coverage = ''
            else:
                info_d = 'head'
                end_r = '3'
                if flask.request.args.get('skin', '') == '':
                    coverage = ''
                else:
                    coverage = flask.request.args.get('skin', '')

            curs.execute("select name from other where name = ? and coverage = ?", [info_d, coverage])
            if curs.fetchall():
                curs.execute("update other set data = ? where name = ? and coverage = ?", [
                    flask.request.form.get('content', ''),
                    info_d,
                    coverage
                ])
            else:
                curs.execute("insert into other (name, data, coverage) values (?, ?, ?)", [info_d, flask.request.form.get('content', ''), coverage])

            conn.commit()

            admin_check(None, 'edit_set')

            return redirect('/setting/' + end_r + '?skin=' + flask.request.args.get('skin', ''))
        else:
            if num == 4:
                curs.execute("select data from other where name = 'body'")
                title = '_body'
                start = ''
            else:
                curs.execute("select data from other where name = 'head' and coverage = ?", [flask.request.args.get('skin', '')])
                title = '_head'
                start = '<a href="?">(' + load_lang('all') + ')</a> ' + \
                ' '.join(['<a href="?skin=' + i + '">(' + i + ')</a>' for i in load_skin('', 1)]) + \
                '''
                    <hr class=\"main_hr\">
                    <span>&lt;style&gt;CSS&lt;/style&gt;<br>&lt;script&gt;JS&lt;/script&gt;</span>
                    <hr class=\"main_hr\">
                '''

            head = curs.fetchall()
            if head:
                data = head[0][0]
            else:
                data = ''

            return easy_minify(flask.render_template(skin_check(),
                imp = [load_lang(data = 'main' + title, safe = 1), wiki_set(), custom(), other2([0, 0])],
                data = '''
                    <form method="post">
                        ''' + start + '''
                        <textarea rows="25" name="content" class=form-control>''' + html.escape(data) + '''</textarea>
                        <hr class=\"main_hr\">
                        <button class="btn btn-primary" type="submit">''' + load_lang('save') + '''</button>
                    </form>
                ''',
                menu = [['setting', load_lang('return')]]
            ))
    elif num == 5:
        if flask.request.method == 'POST':
            curs.execute("select name from other where name = 'robot'")
            if curs.fetchall():
                curs.execute("update other set data = ? where name = 'robot'", [flask.request.form.get('content', '')])
            else:
                curs.execute("insert into other (name, data) values ('robot', ?)", [flask.request.form.get('content', '')])

            conn.commit()

            fw = open('./robots.txt', 'w')
            fw.write(re.sub('\r\n', '\n', flask.request.form.get('content', '')))
            fw.close()

            admin_check(None, 'edit_set')

            return redirect('/setting/4')
        else:
            curs.execute("select data from other where name = 'robot'")
            robot = curs.fetchall()
            if robot:
                data = robot[0][0]
            else:
                data = ''

            f = open('./robots.txt', 'r')
            lines = f.readlines()
            f.close()

            if not data or data == '':
                data = ''.join(lines)

            return easy_minify(flask.render_template(skin_check(),
                imp = ['robots.txt', wiki_set(), custom(), other2([0, 0])],
                data = '''
                    <form method="post">
                        <textarea rows="25" name="content" class=form-control>''' + html.escape(data) + '''</textarea>
                        <hr class=\"main_hr\">
                        <button class="btn btn-primary" type="submit">''' + load_lang('save') + '''</button>
                    </form>
                ''',
                menu = [['setting', load_lang('return')]]
            ))
    elif num == 6:
        i_list = [
            'recaptcha',
            'sec_re',
            'g_email',
            'g_pass'
        ]

        if flask.request.method == 'POST':
            for data in i_list:
                if data == 'g_email':
                    into_data = re.sub('@.*$', '', flask.request.form.get(data, ''))
                else:
                    into_data = flask.request.form.get(data, '')

                curs.execute("update other set data = ? where name = ?", [into_data, data])

            conn.commit()

            admin_check(None, 'edit_set')

            return redirect('/setting/6')
        else:
            d_list = []

            x = 0

            for i in i_list:
                curs.execute('select data from other where name = ?', [i])
                sql_d = curs.fetchall()
                if sql_d:
                    d_list += [sql_d[0][0]]
                else:
                    curs.execute('insert into other (name, data) values (?, ?)', [i, ''])

                    d_list += ['']

                x += 1

            conn.commit()

            return easy_minify(flask.render_template(skin_check(),
                imp = ['Google', wiki_set(), custom(), other2([0, 0])],
                data = '''
                    <form method="post">
                        <h2><a href="https://www.google.com/recaptcha/admin">recaptcha</a></h2>
                        <span>''' + load_lang('recaptcha') + ''' (HTML)</span>
                        <hr class=\"main_hr\">
                        <input name="recaptcha" value="''' + html.escape(d_list[0]) + '''">
                        <hr class=\"main_hr\">
                        <span>''' + load_lang('recaptcha') + ' (' + load_lang('secret_key') + ''')</span>
                        <hr class=\"main_hr\">
                        <input name="sec_re" value="''' + html.escape(d_list[1]) + '''">
                        <hr class=\"main_hr\">
                        <h2><a href="https://support.google.com/mail/answer/7126229">''' + load_lang('google_imap') + '</a> {' + load_lang('restart_required') + '''}</h1>
                        <span>''' + load_lang('google_email') + '''</span>
                        <hr class=\"main_hr\">
                        <input name="g_email" value="''' + html.escape(d_list[2]) + '''">
                        <hr class=\"main_hr\">
                        <span><a href="https://security.google.com/settings/security/apppasswords">''' + load_lang('google_app_password') + '''</a></span>
                        <hr class=\"main_hr\">
                        <input type="password" name="g_pass" value="''' + html.escape(d_list[3]) + '''">
                        <hr class=\"main_hr\">
                        <button id="save" type="submit">''' + load_lang('save') + '''</button>
                    </form>
                ''',
                menu = [['setting', load_lang('return')]]
            ))
    else:
        return redirect()