from .tool.func import *

def edit_2(conn, name, isrequest = False):
    curs = conn.cursor()

    if re.search('^\s', name) or re.search('\s$', name):
        return re_error('/error/9001')

    if not('state' in flask.session):
        identifier = 'i:' + ip_check()
    else:
        identifier = 'm:' + ip_check()
    curs.execute("select id from history where title = ? order by date desc", [name])
    fet = curs.fetchall()
    if fet:
        baserev = fet[0][0]
    else:
        baserev = '1'

    if name == ' ' or name == '' or re.sub('\s', '', name) == '':
        return re_error('/error/9001')


    if getacl(name, 'read') == 0:
        return noread(conn, name)

    curs.execute("select data from data where title = ?", [name])
    if not(curs.fetchall()):
        smsub = ' (새 문서 생성)'
    else:
        smsub = ' (r' + baserev + ' 편집)'

    ip = ip_check()
    #if acl_check(name) == 1:
     #   return re_error('/ban')


    #-----------------------------------------------------------------


    curs.execute("select data from data where title = ?", [name])
    new = curs.fetchall()
    if new:
        if flask.request.args.get('section', None):
            test_data = '\n' + re.sub('\r\n', '\n', new[0][0]) + '\n'

            section_data = re.findall('((?:={1,6}) ?(?:(?:(?!={1,6}\n).)+) ?={1,6}\n(?:(?:(?!(?:={1,6}) ?(?:(?:(?!={1,6}\n).)+) ?={1,6}\n).)*\n*)*)', test_data)
            try:
                data = section_data[int(flask.request.args.get('section', '1')) - 1]
            except:
                return re_error('/error/8001')
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
        smsub = ' (문단 편집)'

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

    if 'timecosmos' in flask.request.cookies:
        chkbx = ' checked'
    else:
        chkbx = ''

    dfnmgrtutei = ''' '''
    fdvsdvgbrtf = ''' '''
    fgeyhythtrt = '''
    <script>
    function setLogLabelLength() {
      document.getElementById('logInputLabel').innerHTML = '요약 (' + String($('#logInput').val().length) + '/190)';
    }
    document.getElementById('logInput').onchange = function() {
      document.getElementById('logInputLabel').innerHTML = '요약 (' + String($('#logInput').val().length) + '/190)';
    };
    $("#logInput").on("change paste keyup input", function() {
      document.getElementById('logInputLabel').innerHTML = '요약 (' + String($('#logInput').val().length) + '/190)';
    });
    </script><div class=form-group>
                <label id="logInputLabel">요약</label><br>
                <input class="form-control" name="send" onchange="setLogLabelLength();" id="logInput" type="text" style="width:100% !important;">
                <script>
                    $("#logInput").on("change paste keyup input", function() {
                      document.getElementById('logInputLabel').innerHTML = '요약 (' + String($('#logInput').val().length) + '/190)';
                    });
                </script></div>
                ''' + captcha_get() + '''<label><input type=checkbox name=agree id=agreeCheckbox''' + chkbx + '''>&nbsp;''' + getConfig('edit_warning', '') + '''</label><br>
                <b>''' + ip_warring() + '''</b><div class=btns><button class="btn btn-primary" type="submit" style="width: 100px;">''' + load_lang('save') + '''</button></div>
                '''
    admin = admin_check(5)
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
    if getacl(name, 'edit') == 0:
        fgeyhythtrt = ''' '''
        fdvsdvgbrtf = ''' readonly disabled style="background:#eceeef"'''
        dfnmgrtutei = alertBalloon(re_balloon('/ban', 1, name))
        err = 1

    #-----------------------------------------------------------------



    if flask.request.method == 'POST':
        if flask.request.form.get('send', '') == '빙하타고 내려와' and 'easteregg1' in flask.session:
            flask.session['easteregg2'] = 1

        if not(flask.session['token']):
            return re_error('/error/987654321')
        curs.execute("select id from history where title = ? order by date desc", [name])
        fet = curs.fetchall()
        if fet:
            crv = fet[0][0]
        else:
            crv = '0'


        if int(crv) > int(flask.request.form.get('baserev', '')):
            curs.execute("select data from data where title = ?", [name])
            fetc = curs.fetchall()
            if fetc:
                newdat = fetc[0][0]
            else:
                newdat = ''
            curs.execute("select data from history where title = ? and id = ?", [name, flask.request.form.get('baserev', '')])
            first_raw_data = curs.fetchall()
            if first_raw_data:
                first_raw_data = first_raw_data[0][0]
            else:
                first_raw_data = ''
            diffContent = '''
                <input type=hidden id=contextSize value="5">
                <input type=hidden id=rev value="0">
                <input type=hidden id=olderrev value="0">
                <div id=diffoutput></div>
                <textarea id=baseText style="display: none;">''' + first_raw_data + '''</textarea>
                <textarea id=newText style="display: none;">''' + savemark(flask.request.form.get('content', '')) + '''</textarea>
                <script>
                    $(function() {
                        diffUsingJS(1);
                        $("th.texttitle").html("r''' + flask.request.form.get('baserev', '') + ''' vs. 사용자 입력");
                    });
                </script>
            '''
            result = diffContent + '<a id="showUserData" onclick="$(\'#userData\').show(); $(this).remove();" class="btn btn-info">사용자 입력 RAW</a><textarea id="userData" rows="12" style="display:none;" class=form-control readonly>' + savemark(flask.request.form.get('content', '')) + '</textarea><br><br>'


            return easy_minify(flask.render_template(skin_check(),
                    imp = [name, wiki_set(), custom(), other2([' (' + load_lang('edit') + ')', 0])],
                    data = get_name + '''<div class="alert alert-danger edit-alert" role="alert">
<strong>[오류!]</strong> 편집 도중에 다른 사용자가 먼저 편집을 했습니다.
</div>''' + result + '''<span style="color:red; font-weight: bold; padding-bottom: 5px; padding-top: 5px;">자동 병합에 실패했습니다! 수동으로 수정된 내역을 아래 텍스트 박스에 다시 입력해주세요.</span>
                        <form method="post" id="editForm">
                        <input type="hidden" name="identifier" value="''' + identifier + '''">
                        <input type="hidden" name="baserev" value="''' + baserev + '''">
                        <input type="hidden" name="token" value="''' + flask.session['token'] + '''">
                            ''' + dfnmgrtutei + edit_button() + '''<br><ul class="nav nav-tabs" role="tablist" style="height: 43px;">
        <li class="nav-item" style="list-style-type:none !important">
        <a id="edtb" class="nav-link active" data-toggle="tab" href="#edit" role="tab" onclick="document.getElementById(\'content\').style.display = \'block\';document.getElementById(\'see_preview\').style.display = \'none\'; document.getElementById('edtb').className = 'nav-link active'; document.getElementById('prtb').className = 'nav-link';">편집</a>
        </li>
        <li class="nav-item" style="list-style-type:none !important">
        <a id="prtb" class="nav-link" data-toggle="tab" role="tab" aria-expanded="false" id="preview" onclick="document.getElementById('edtb').className = 'nav-link'; document.getElementById('prtb').className = 'nav-link active'; do_preview(\'''' + name + '''\');document.getElementById(\'content\').style.display = \'none\';document.getElementById(\'see_preview\').style.display = \'block\'; ">미리보기</a>
        </li>

        </ul>
                            <textarea id="content" rows="25" class=form-control name="content"''' + fdvsdvgbrtf + ''' style="width:100% !important;">''' + newdat + '''</textarea>
                            <div id="see_preview" style="overflow:auto;height:518px;border-radius: .25rem;padding: .5rem .75rem;display:none"></div>
                            <textarea style="display: none;" name="otent">''' + html.escape(re.sub('\n$', '', data_old)) + '''</textarea>
                            ''' + fgeyhythtrt + '''
                        </form>
                        ''' + b_text + '''

                    ''',
                    menu = [['w/' + url_pas(name), load_lang('return')], ['delete/' + url_pas(name), load_lang('delete')], ['move/' + url_pas(name), load_lang('move')]],
                    st = 2,
                    err = 1, smsub = smsub
                ))
        if (flask.request.form.get('token', '') != flask.session['token']) or (flask.request.form.get('identifier', '') != identifier):
            return easy_minify(flask.render_template(skin_check(),
                    imp = [name, wiki_set(), custom(), other2([' (' + load_lang('edit') + ')', 0])],
                    data = get_name + '''<div class="alert alert-danger edit-alert" role="alert">
<strong>[오류!]</strong> CSRF 방지 토큰이 일치하지 않습니다. 다시 시도해주세요.
</div>
                        <form method="post" id="editForm">
                        <input type="hidden" name="identifier" value="''' + identifier + '''">
                        <input type="hidden" name="baserev" value="''' + baserev + '''">
                        <input type="hidden" name="token" value="''' + flask.session['token'] + '''">
                            ''' + dfnmgrtutei + edit_button() + '''<br><ul class="nav nav-tabs" role="tablist" style="height: 43px;">
        <li class="nav-item" style="list-style-type:none !important">
        <a id="edtb" class="nav-link active" data-toggle="tab" href="#edit" role="tab" onclick="document.getElementById(\'content\').style.display = \'block\';document.getElementById(\'see_preview\').style.display = \'none\'; document.getElementById('edtb').className = 'nav-link active'; document.getElementById('prtb').className = 'nav-link';">편집</a>
        </li>
        <li class="nav-item" style="list-style-type:none !important">
        <a id="prtb" class="nav-link" data-toggle="tab" role="tab" aria-expanded="false" id="preview" onclick="document.getElementById('edtb').className = 'nav-link'; document.getElementById('prtb').className = 'nav-link active'; do_preview(\'''' + name + '''\');document.getElementById(\'content\').style.display = \'none\';document.getElementById(\'see_preview\').style.display = \'block\'; ">미리보기</a>
        </li>

        </ul>
                            <textarea id="content" rows="25" class=form-control name="content"''' + fdvsdvgbrtf + ''' style="width:100% !important;">''' + savemark(flask.request.form.get('content', '')) + '''</textarea>
                            <div id="see_preview" style="overflow:auto;height:518px;border-radius: .25rem;padding: .5rem .75rem;display:none"></div>
                            <textarea style="display: none;" name="otent">''' + html.escape(re.sub('\n$', '', data_old)) + '''</textarea>
                            ''' + fgeyhythtrt + '''
                        </form>
                        ''' + b_text + '''

                    ''',
                    menu = [['w/' + url_pas(name), load_lang('return')], ['delete/' + url_pas(name), load_lang('delete')], ['move/' + url_pas(name), load_lang('move')]],
                    st = 2,
                    err = 1, smsub = smsub
                ))

        curs.execute("select data from data where title = ?", [name])
        if not(curs.fetchall()) and re.search('^사용자:', name) and not(re.search('[/]', name)):
            return easy_minify(flask.render_template(skin_check(),
                    imp = [name, wiki_set(), custom(), other2([' (' + load_lang('edit') + ')', 0])],
                    data = get_name + '''<div class="alert alert-danger edit-alert" role="alert">
<strong>[오류!]</strong> disable_user_document
</div>
                        <form method="post" id="editForm">
                        <input type="hidden" name="identifier" value="''' + identifier + '''">
                        <input type="hidden" name="baserev" value="''' + baserev + '''">
                        <input type="hidden" name="token" value="''' + flask.session['token'] + '''">
                            ''' + dfnmgrtutei + edit_button() + '''<br><ul class="nav nav-tabs" role="tablist" style="height: 43px;">
        <li class="nav-item" style="list-style-type:none !important">
        <a id="edtb" class="nav-link active" data-toggle="tab" href="#edit" role="tab" onclick="document.getElementById(\'content\').style.display = \'block\';document.getElementById(\'see_preview\').style.display = \'none\'; document.getElementById('edtb').className = 'nav-link active'; document.getElementById('prtb').className = 'nav-link';">편집</a>
        </li>
        <li class="nav-item" style="list-style-type:none !important">
        <a id="prtb" class="nav-link" data-toggle="tab" role="tab" aria-expanded="false" id="preview" onclick="document.getElementById('edtb').className = 'nav-link'; document.getElementById('prtb').className = 'nav-link active'; do_preview(\'''' + name + '''\');document.getElementById(\'content\').style.display = \'none\';document.getElementById(\'see_preview\').style.display = \'block\'; ">미리보기</a>
        </li>

        </ul>
                            <textarea id="content" rows="25" class=form-control name="content"''' + fdvsdvgbrtf + ''' style="width:100% !important;">''' + savemark(flask.request.form.get('content', '')) + '''</textarea>
                            <div id="see_preview" style="overflow:auto;height:518px;border-radius: .25rem;padding: .5rem .75rem;display:none"></div>
                            <textarea style="display: none;" name="otent">''' + html.escape(re.sub('\n$', '', data_old)) + '''</textarea>
                            ''' + fgeyhythtrt + '''
                        </form>
                        ''' + b_text + '''

                    ''',
                    menu = [['w/' + url_pas(name), load_lang('return')], ['delete/' + url_pas(name), load_lang('delete')], ['move/' + url_pas(name), load_lang('move')]],
                    st = 2,
                    err = 1, smsub = smsub
                ))

        if len(flask.request.form.get('send', '')) > 190:
            return easy_minify(flask.render_template(skin_check(),
                    imp = [name, wiki_set(), custom(), other2([' (' + load_lang('edit') + ')', 0])],
                    data = get_name + '''<div class="alert alert-danger edit-alert" role="alert">
<strong>[오류!]</strong> 요약의 값은 190자 이하이여야 합니다.
</div>
                        <form method="post" id="editForm">
                        <input type="hidden" name="identifier" value="''' + identifier + '''">
                        <input type="hidden" name="baserev" value="''' + baserev + '''">
                        <input type="hidden" name="token" value="''' + flask.session['token'] + '''">
                            ''' + dfnmgrtutei + edit_button() + '''<br><ul class="nav nav-tabs" role="tablist" style="height: 43px;">
        <li class="nav-item" style="list-style-type:none !important">
        <a id="edtb" class="nav-link active" data-toggle="tab" href="#edit" role="tab" onclick="document.getElementById(\'content\').style.display = \'block\';document.getElementById(\'see_preview\').style.display = \'none\'; document.getElementById('edtb').className = 'nav-link active'; document.getElementById('prtb').className = 'nav-link';">편집</a>
        </li>
        <li class="nav-item" style="list-style-type:none !important">
        <a id="prtb" class="nav-link" data-toggle="tab" role="tab" aria-expanded="false" id="preview" onclick="document.getElementById('edtb').className = 'nav-link'; document.getElementById('prtb').className = 'nav-link active'; do_preview(\'''' + name + '''\');document.getElementById(\'content\').style.display = \'none\';document.getElementById(\'see_preview\').style.display = \'block\'; ">미리보기</a>
        </li>

        </ul>
                            <textarea id="content" rows="25" class=form-control name="content"''' + fdvsdvgbrtf + ''' style="width:100% !important;">''' + savemark(flask.request.form.get('content', '')) + '''</textarea>
                            <div id="see_preview" style="overflow:auto;height:518px;border-radius: .25rem;padding: .5rem .75rem;display:none"></div>
                            <textarea style="display: none;" name="otent">''' + html.escape(re.sub('\n$', '', data_old)) + '''</textarea>
                            ''' + fgeyhythtrt + '''
                        </form>
                        ''' + b_text + '''

                    ''',
                    menu = [['w/' + url_pas(name), load_lang('return')], ['delete/' + url_pas(name), load_lang('delete')], ['move/' + url_pas(name), load_lang('move')]],
                    st = 2,
                    err = 1, smsub = smsub
                ))

        if flask.request.form.get('agree', 0) == 0:
            return easy_minify(flask.render_template(skin_check(),
                    imp = [name, wiki_set(), custom(), other2([' (' + load_lang('edit') + ')', 0])],
                    data = get_name + '''<div class="alert alert-danger edit-alert" role="alert">
<strong>[오류!]</strong> 문서에 기여하려면 라이선스에 동의해야합니다. 기여한 내용은 문서 역사, 기여 목록에 공개적으로 영구히 기록됩니다.
</div>
                        <form method="post" id="editForm">
                        <input type="hidden" name="identifier" value="''' + identifier + '''">
                        <input type="hidden" name="baserev" value="''' + baserev + '''">
                        <input type="hidden" name="token" value="''' + flask.session['token'] + '''">
                            ''' + dfnmgrtutei + edit_button() + '''<br><ul class="nav nav-tabs" role="tablist" style="height: 43px;">
        <li class="nav-item" style="list-style-type:none !important">
        <a id="edtb" class="nav-link active" data-toggle="tab" href="#edit" role="tab" onclick="document.getElementById(\'content\').style.display = \'block\';document.getElementById(\'see_preview\').style.display = \'none\'; document.getElementById('edtb').className = 'nav-link active'; document.getElementById('prtb').className = 'nav-link';">편집</a>
        </li>
        <li class="nav-item" style="list-style-type:none !important">
        <a id="prtb" class="nav-link" data-toggle="tab" role="tab" aria-expanded="false" id="preview" onclick="document.getElementById('edtb').className = 'nav-link'; document.getElementById('prtb').className = 'nav-link active'; do_preview(\'''' + name + '''\');document.getElementById(\'content\').style.display = \'none\';document.getElementById(\'see_preview\').style.display = \'block\'; ">미리보기</a>
        </li>

        </ul>
                            <textarea id="content" rows="25" class=form-control name="content"''' + fdvsdvgbrtf + ''' style="width:100% !important;">''' + savemark(flask.request.form.get('content', '')) + '''</textarea>
                            <div id="see_preview" style="overflow:auto;height:518px;border-radius: .25rem;padding: .5rem .75rem;display:none"></div>
                            <textarea style="display: none;" name="otent">''' + html.escape(re.sub('\n$', '', data_old)) + '''</textarea>
                            ''' + fgeyhythtrt + '''
                        </form>
                        ''' + b_text + '''

                    ''',
                    menu = [['w/' + url_pas(name), load_lang('return')], ['delete/' + url_pas(name), load_lang('delete')], ['move/' + url_pas(name), load_lang('move')]],
                    st = 2,
                    err = 1, smsub = smsub
                ))



        curs.execute("select data from data where title = ?", [name])
        old = curs.fetchall()
        if old:
            if old[0][0] == savemark(flask.request.form.get('content', '')):
                return easy_minify(flask.render_template(skin_check(),
                    imp = [name, wiki_set(), custom(), other2([' (' + load_lang('edit') + ')', 0])],
                    data = get_name + '''<div class="alert alert-danger edit-alert" role="alert">
<strong>[오류!]</strong> 문서 내용이 같습니다.
</div>
                        <form method="post" id="editForm">
                        <input type="hidden" name="identifier" value="''' + identifier + '''">
                        <input type="hidden" name="baserev" value="''' + baserev + '''">
                        <input type="hidden" name="token" value="''' + flask.session['token'] + '''">
                            ''' + dfnmgrtutei + edit_button() + '''<br><ul class="nav nav-tabs" role="tablist" style="height: 43px;">
        <li class="nav-item" style="list-style-type:none !important">
        <a id="edtb" class="nav-link active" data-toggle="tab" href="#edit" role="tab" onclick="document.getElementById(\'content\').style.display = \'block\';document.getElementById(\'see_preview\').style.display = \'none\'; document.getElementById('edtb').className = 'nav-link active'; document.getElementById('prtb').className = 'nav-link';">편집</a>
        </li>
        <li class="nav-item" style="list-style-type:none !important">
        <a id="prtb" class="nav-link" data-toggle="tab" role="tab" aria-expanded="false" id="preview" onclick="document.getElementById('edtb').className = 'nav-link'; document.getElementById('prtb').className = 'nav-link active'; do_preview(\'''' + name + '''\');document.getElementById(\'content\').style.display = \'none\';document.getElementById(\'see_preview\').style.display = \'block\'; ">미리보기</a>
        </li>

        </ul>
                            <textarea id="content" rows="25" class=form-control name="content"''' + fdvsdvgbrtf + ''' style="width:100% !important;">''' + html.escape(re.sub('\n$', '', data)) + '''</textarea>
                            <div id="see_preview" style="overflow:auto;height:518px;border-radius: .25rem;padding: .5rem .75rem;display:none"></div>
                            <textarea style="display: none;" name="otent">''' + html.escape(re.sub('\n$', '', data_old)) + '''</textarea>
                            ''' + fgeyhythtrt + '''
                        </form>
                        ''' + b_text + '''

                    ''',
                    menu = [['w/' + url_pas(name), load_lang('return')], ['delete/' + url_pas(name), load_lang('delete')], ['move/' + url_pas(name), load_lang('move')]],
                    st = 2,
                    err = 1, smsub = smsub
                ))


        if captcha_post(flask.request.form.get('g-recaptcha-response', '')) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)
        curs.execute("select data from data where title = ?", [name])
        old = curs.fetchall()
        efchh = True
        if not old:
            efchh = False

        admin = admin_check(5)
        #if re.search('^사용자:', name):
         #   if name == '사용자:' + str(ip_check()):
          #      fdsfv = '12'
           # else:
            #    if admin == 1:
             #       fsdvfgh = '2'
              #  else:
               #     return re_error('/ban')

        if getacl(name, 'edit') == 0:
            return re_error('/ban')


        today = get_time()
        content = savemark(flask.request.form.get('content', ''))
        iii = ''
        curs.execute("select data from data where title = ?", [name])
        old = curs.fetchall()
        if old:
            leng = leng_check(len(flask.request.form.get('otent', '')), len(content))

            if flask.request.args.get('section', None):
                content = old[0][0].replace(flask.request.form.get('otent', ''), content)

            curs.execute("update data set data = ? where title = ?", [content, name])
        else:
            iii = '새 문서'
            if len(content) == 0:
                leng = '0'
            else:
                leng = '+' + str(len(content))

            curs.execute("insert into data (title, data) values (?, ?)", [name, content])

        curs.execute("select user from scan where title = ?", [name])
        for _ in curs.fetchall():
            curs.execute("insert into alarm (name, data, date) values (?, ?, ?)", [ip, ip + ' - <a href="/w/' + url_pas(name) + '">' + name + '</a> (Edit)', today])

        editlog = flask.request.form.get('send', '')
        if 'easteregg2' in flask.session:
            editlog = ''

        if iii == '새 문서':
            history_plus(
                name,
                content,
                today,
                ip,
                editlog,
                leng,
                iii
            )
        else:
            history_plus(
                name,
                content,
                today,
                ip,
                editlog,
                leng
            )

        editfilterCheck = checkEditFilter(flask.request.form.get('content', ''), str(baserev), name, h = efchh)
        if editfilterCheck[0] == 1:
            return easy_minify(flask.render_template(skin_check(),
                    imp = [name, wiki_set(), custom(), other2([' (' + load_lang('edit') + ')', 0])],
                    data = get_name + '''<div class="alert alert-danger edit-alert" role="alert">
<strong>[오류!]</strong> <a href="/admin/edit_filters">편집 필터</a>에 의해 금지된 키워드가 사용됐습니다. - ''' + editfilterCheck[1] + '''
</div>
                        <form method="post" id="editForm">
                        <input type="hidden" name="identifier" value="''' + identifier + '''">
                        <input type="hidden" name="baserev" value="''' + str(int(baserev) + 1) + '''">
                        <input type="hidden" name="token" value="''' + flask.session['token'] + '''">
                            ''' + dfnmgrtutei + edit_button() + '''<br><ul class="nav nav-tabs" role="tablist" style="height: 43px;">
        <li class="nav-item" style="list-style-type:none !important">
        <a id="edtb" class="nav-link active" data-toggle="tab" href="#edit" role="tab" onclick="document.getElementById(\'content\').style.display = \'block\';document.getElementById(\'see_preview\').style.display = \'none\'; document.getElementById('edtb').className = 'nav-link active'; document.getElementById('prtb').className = 'nav-link';">편집</a>
        </li>
        <li class="nav-item" style="list-style-type:none !important">
        <a id="prtb" class="nav-link" data-toggle="tab" role="tab" aria-expanded="false" id="preview" onclick="document.getElementById('edtb').className = 'nav-link'; document.getElementById('prtb').className = 'nav-link active'; do_preview(\'''' + name + '''\');document.getElementById(\'content\').style.display = \'none\';document.getElementById(\'see_preview\').style.display = \'block\'; ">미리보기</a>
        </li>

        </ul>
                            <textarea id="content" rows="25" class=form-control name="content" disabled readonly ''' + fdvsdvgbrtf + ''' style="width:100% !important;">''' + savemark(flask.request.form.get('content', '')) + '''</textarea>
                            <div id="see_preview" style="overflow:auto;height:518px;border-radius: .25rem;padding: .5rem .75rem;display:none"></div>
                            <textarea style="display: none;" name="otent">''' + html.escape(re.sub('\n$', '', data_old)) + '''</textarea>
                            ''' + fgeyhythtrt + '''
                        </form>
                        ''' + b_text + '''

                    ''',
                    menu = [['w/' + url_pas(name), load_lang('return')], ['delete/' + url_pas(name), load_lang('delete')], ['move/' + url_pas(name), load_lang('move')]],
                    st = 2,
                    err = 1, smsub = smsub
                ))

        curs.execute("update data set date = ? where title = ?", [get_time(), name])

        curs.execute("delete from back where link = ?", [name])
        curs.execute("delete from back where title = ? and type = 'no'", [name])

        render_set(
            title = name,
            data = content,
            num = 1
        )

        curs.execute("update star set lstedt = ? where doc = ?", [get_time(), name])

        conn.commit()

        res = flask.make_response(redirect('/w/' + url_pas(name)))

        expireingDate = datetime.datetime.now()
        expireingDate = expireingDate + datetime.timedelta(days=30)

        if not 'timecosmos' in flask.request.cookies:
            res.set_cookie('timecosmos', value='', expires=expireingDate)

        return res
    else:
        flask.session['token'] = sha224(ip_check() + ''.join(random.choice("0123456789abcDEFghiJKLmnoPQRstuVWXyz") for i in range(64)))

        if name == '라면과 구공탄' and 'easteregg2' in flask.session:
            flask.session.pop('easteregg2', None)
            flask.session.pop('easteregg1', None)

            return easy_minify(flask.render_template(skin_check(),
                imp = [name, wiki_set(), custom(), other2([0, 0])],
                data = '''<p>새로고침하면 편집으로 이동합니다.</p>
                            <iframe width=640 height=360 src="https://www.youtube-nocookie.com/embed/n1Qxem9wjFM?autoplay=1&rel=0rel=0" frameborder=0 allow="autoplay; encrypted-media;"></iframe>
                          <br><br>
                          <marquee direction=up width=100% height=300px bgcolor=#008080 loop=2 style="padding: 10px; border: 2px solid #00c8c8; border-top-width: 5px; border-radius: 0 0 5px 5px; text-align: center;">
                              &lt;위키 엔진 개발 기여자&gt;<br><br>
                              <a href="https://github.com/2du"><font color=white>2du</font></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                              <a href="https://github.com/gnote8-0"><font color=white>GW-BASIC</font></a><br>

                              <a href="https://github.com/namuwiki"><font color=white>namu</font></a>
                          </marquee><br><br>''' + render_set(data = open('./route/alphgame.txt', 'r').read()),
                st = 0
            ))

        return easy_minify(flask.render_template(skin_check(),
            imp = [name, wiki_set(), custom(), other2([' (' + load_lang('edit') + ')', 0])],
            data = get_name + '''
                <form method="post" id="editForm" data-title="''' + name + '''">
                <input type="hidden" name="identifier" value="''' + identifier + '''">
                <input type="hidden" name="baserev" value="''' + baserev + '''">
                <input type="hidden" name="token" value="''' + flask.session['token'] + '''">
                    ''' + dfnmgrtutei + edit_button() + '''<br><ul class="nav nav-tabs" role="tablist" style="height: 38px;">
        <li class="nav-item" style="list-style-type:none !important">
        <a id="edtb" class="nav-link active" data-toggle="tab" href="#edit" role="tab" onclick="document.getElementById(\'content\').style.display = \'block\';document.getElementById(\'see_preview\').style.display = \'none\'; document.getElementById('edtb').className = 'nav-link active'; document.getElementById('prtb').className = 'nav-link';">편집</a>
        </li>
        <li class="nav-item" style="list-style-type:none !important">
        <a id="prtb" class="nav-link" data-toggle="tab" role="tab" aria-expanded="false" id="preview" onclick="document.getElementById('edtb').className = 'nav-link'; document.getElementById('prtb').className = 'nav-link active'; do_preview(\'''' + name + '''\');document.getElementById(\'content\').style.display = \'none\';document.getElementById(\'see_preview\').style.display = \'block\'; ">미리보기</a>
        </li>

        </ul>
                            <textarea id="content" rows="25" class=form-control name="content"''' + fdvsdvgbrtf + ''' style="width:100% !important;">''' + html.escape(data) + '''</textarea>
                            <div id="see_preview" style="overflow:auto;height:518px;border-radius: .25rem;padding: .5rem .75rem;display:none"></div><textarea style="display: none;" name="otent">''' + html.escape(re.sub('\n$', '', data_old)) + '''</textarea>
                    ''' + fgeyhythtrt + '''
                </form>
                ''' + b_text + '''

            ''',
            menu = [['w/' + url_pas(name), load_lang('return')], ['delete/' + url_pas(name), load_lang('delete')], ['move/' + url_pas(name), load_lang('move')]],
            st = 2,
            err = err,
            smsub = smsub
        ))

def Preview(title = ''):
    content = '<article class="container-fluid wiki-article" style="margin: 0;"><h1 class="title">' + title + '</h1><div class="wiki-content">';
    content += render_set(data = getForm('content', ''));
    content += '</div></article>';

    header = '''
        <html>
            <head>
                <script src="/skins/main_css/js/jquery.min.js"></script>
                <meta charset=utf-8>
                <meta name="generator" content="onamu-theseed">
                <link rel="stylesheet" href="/views/main_css/css/wiki.css">
                <script src="/views/main_css/js/theseed-onamu.js"></script>
                <script src="/skins/main_css/js/intersection-observer.js"></script>
                <script src="/skins/main_css/js/dateformatter.js"></script>
        ''';

    skin = skin_check(1)
    try:
        for files in os.listdir("../views/main_css/js"):
            filename = re.search(".js$", files, re.IGNORECASE);
            if filename:
                header += '<script src="/views/main_css/js/' + filename + '"></script>';
    except:
        pass;
    try:
        for files in os.listdir("../views/main_css/css"):
            filename = re.search(".css$", files, re.IGNORECASE);
            if filename:
                header += '<link rel="stylesheet" href="/views/main_css/css/' + filename + '">';
    except:
        pass;
    try:
        for files in os.listdir("../views/" + skin + "/css"):
            filename = re.search(".css$", files, re.IGNORECASE);
            if filename:
                header += '<link rel="stylesheet" href="/skins/' + skin + '/css/' + filename + '">';
    except:
        pass;
    try:
        for files in os.listdir("../views/" + skin + "/js"):
            filename = re.search(".js$", files, re.IGNORECASE);
            if filename:
                header += '<script src="/skins/' + skin + '/js/' + filename + '"></script>';
    except:
        pass;

    header += '''
                <script>
                    jQuery(function() {
                        $("time").each(function () {
                            var format = $(this).attr("data-format");
                            var time = $(this).attr("datetime");
                            if (!format || !time) {
                                return;
                            }
                            $(this).text(formatDate(new Date(time), format));
                        });
                    });
                </script>
            </head>
            <body>
    '''

    footer = '''
            </body>
        </html>
    '''

    return header + content + footer;