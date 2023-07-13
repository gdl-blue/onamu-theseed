from .tool.func import *

def newEditRequest(conn, title):
    curs = conn.cursor()

    curs.execute("select data from data where title = ?", [title])
    docData = curs.fetchall()
    if not docData:
        return showError("'" + title + "' 문서를 찾을 수 없습니다. 제목을 올바르게 입력했는지 확인하고 다시 시도하십시오.")
    docContent = docData[0][0]

    if getacl(title, 'edit_request') != 1:
        return showError(title + '문서 편집 요청을 생설할 수 없습니다.<br><br>액세스가 거부되었습니다.')


    content = '''
        <form method="post" id="editForm">
            <ul class="nav nav-tabs" role="tablist" style="height: 38px;">
                <li class="nav-item">
                    <a class="nav-link active" data-toggle="tab" href="#edit" role="tab">편집</a>
                </li>
                <li class="nav-item">
                    <a id="previewLink" class="nav-link" data-toggle="tab" href="#preview" role="tab">미리보기</a>
                </li>
            </ul>

            <div class="tab-content bordered">
                <div class="tab-pane active" id="edit" role="tabpanel">
                    <textarea id="textInput" name="text" class="form-control" wrap="soft">''' + html_escape(docContent) + '''</textarea>
                </div>
                <div class="tab-pane" id="preview" role="tabpanel"></div>
            </div>

            <div class="form-group" style="margin-top: 1rem;">
                <label class="control-label" for="summaryInput">요약</label>
                <input class="form-control" id="logInput" name="log" value="" type="text" maxlength=190>
            </div>

            <label><input name="agree" id="agreeCheckbox" value="Y" type="checkbox">&nbsp;문서 편집을 <strong>저장</strong>하면 당신은 기여한 내용을 <strong>CC BY-NC-SA 2.0 KR</strong>으로 배포하고 기여한 문서에 대한 하이퍼링크나 URL을 이용하여 저작자 표시를 하는 것으로 충분하다는 데 동의하며, 위키의 <a href="https://www.alphawiki.org/w/알파위키:기본규칙">기본규칙</a>및 <a href="https://www.alphawiki.org/w/알파위키:면책%20조항">면책조항</a>등을 포함한 일체의 이용 규약에 <strong>동의</strong>하는 것으로 간주됩니다. 이 <strong>동의는 철회할 수 없습니다.</strong></label>

            <p style="font-weight: bold;">''' + ip_warning() + '''</p>

            <div class="btns">
                <button id="editBtn" class="btn btn-primary" style="width: 100px;">저장</button>
            </div>

            ''' + captcha_get() + '''
        </form>
    '''

    if flask.request.method == 'POST':
        curs.execute("select l from leq where m = 1")
        l = curs.fetchall()
        if not l:
            l = '1'
        else:
            l = str(int(l[0][0]) + 1)
        curs.execute("select id from history where title = ? order by date desc limit 1", [title])
        b = curs.fetchall()
        if not b:
            b = '1'
        else:
            b = b[0][0]

        curs.execute('''
            insert into thread_edit_requests (
                baserev, num, state,
                content, log, applied_rev, requester, closer,
                request_time, close, doctitle)
            values (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        ''', [
            b, l, 'open', getForm('text'), getForm('log'), '', ip_check(), '', get_time(), '', title
        ])
        conn.commit()

        return redirect('/edit_request/' + l)
    return easy_minify(flask.render_template(skin_check(),
        imp = [title, wiki_set(), custom(), other2([' (편집 요청)', 0])],
        data = content,
        menu = [['w/' + url_pas(name), load_lang('return')], ['delete/' + url_pas(name), load_lang('delete')], ['move/' + url_pas(name), load_lang('move')]],
        st = 0
    ))

def eq_2(conn, num):
    curs = conn.cursor()

    name = ''
    curs.execute("select name from erq where num = ?", [num])
    naamam = curs.fetchall()
    if naamam:
        name = naamam[0][0]
    r = ''
    curs.execute("select user from erq where num = ?", [num])
    ifdfpipp = curs.fetchall()
    if ifdfpipp:
        r = ifdfpipp[0][0]
    state = ''
    curs.execute("select state from erq where num = ?", [num])
    statestate = curs.fetchall()
    if statestate:
        state = statestate[0][0]
    else:
        return re_error('/error/4000')
    t = ''
    curs.execute("select time from erq where num = ?", [num])
    tt = curs.fetchall()
    if tt:
        t = tt[0][0]
    s = ''
    curs.execute("select send from erq where num = ?", [num])
    ss = curs.fetchall()
    if ss:
        s = ss[0][0]
    d = ''
    curs.execute("select data from erq where num = ?", [num])
    dd = curs.fetchall()
    if dd:
        d = dd[0][0]
    ap = ''
    curs.execute("select ap from erq where num = ?", [num])
    app = curs.fetchall()
    if app:
        ap = app[0][0]
    p = ''
    curs.execute("select pan from erq where num = ?", [num])
    pp = curs.fetchall()
    if pp:
        p = pp[0][0]
    w = ''
    curs.execute("select why from erq where num = ?", [num])
    ww = curs.fetchall()
    if ww:
        w = ww[0][0]

    if getacl(name, 'read') != 1:
        return showError(aclmsg(name, 'read')[1] + ' 읽기 권한이 부족합니다. ' + aclmsg(name, 'read')[2] + ' 해당 문서의 <a href="/acl/' + url_pas(name) + '">ACL 탭</a>을 확인하시기 바랍니다.')

    if flask.request.method == 'POST':
        rea = flask.request.form.get('close_reason', '')
        if not(r == ip_check()) and not(admin_check(5) == 1):
            return re_error('/error/3')

        curs.execute("update erq set state = ? where num = ?", ['close', str(num)])
        curs.execute("update erq set closer = ? where num = ?", [ip_check(), str(num)])
        curs.execute("update erq set y = ? where num = ?", [get_time(), str(num)])
        curs.execute("update erq set why = ? where num = ?", [rea, str(num)])
        #flask.request.form.get('otent', '')

        conn.commit()

        return redirect('/edit_request/' + str(num))
    else:
        curs.execute("select data from history where id = ? and title = ?", [str(int(str(p)) - 1), name])
        first_raw_data = curs.fetchall()
        if first_raw_data:
            first_raw_data = first_raw_data[0][0]
        else:
            first_raw_data = ''
        #<th class="texttitle">r7 vs. r8</th>
        result = '''
            <input type=hidden id=contextSize value="5">
            <input type=hidden id=rev value="0">
            <input type=hidden id=olderrev value="0">
            <div id=diffoutput></div>
            <textarea id=baseText style="display: none;">''' + first_raw_data + '''</textarea>
            <textarea id=newText style="display: none;">''' + d + '''</textarea>
            <script>
                $(function() {
                    diffUsingJS(1);
                    $("th.texttitle").html('<a target=_blank href="/edit_request/''' + str(num) + '''/preview">(미리보기)</a>');
                });
            </script>
        '''

        dis = ''
        act = '이 편집 요청을 문서에 적용합니다.'
        if getacl(name, 'edit') == 0:
            dis = ' disabled'
            act = '이 문서를 편집할 수 있는 권한이 없습니다.'
        cds = ''
        cdt = '이 편집 요청을 닫습니다.'
        spo = '<span data-toggle="modal" data-target="#edit-request-close-modal">'
        spc = '</span>'
        if not(r == ip_check()) and not(admin_check(5) == 1):
            cds = ' disabled'
            cdt = '편집 요청을 닫기 위해서는 요청자 본인이거나 권한이 있어야 합니다.'
            spo = ''
            spc = ''
        crd = '''<div class="card">
                        <div class="card-block">
                        <h4 class="card-title" style="border:none">이 편집 요청을...</h4>
                        <p class="card-text">''' + generateTime(t, 'Y-m-d H:i:s') + '''에 마지막으로 수정됨</p>
                        <form id="edit-request-accept-form" style="display: inline;">
                        <script>
                            $(document).on('click', '.modal-dialog button[data-dismiss="modal"]', function() {
                                $(this).parent().parent().parent().parent().parent().hide();
                            });
                            $(document).on('click', 'span[data-toggle="modal"] input[type=button]', function() {
                                $($(this).parent().attr('data-target')).show();
                            });
                        </script>
                        <input type="button" class="btn btn-lg btn-success''' + dis + '''" value="Accept" data-toggle="tooltip" data-placement="top" title="''' + act + '''" style="width:auto" onclick="location.href = \'/edit_request_accept/''' + str(num) + '''\';"''' + dis + '''>
                        </form>
                        ''' + spo + '''<input type="button" class="btn btn-lg''' + cds + '''" data-toggle="tooltip" data-placement="top" title="''' + cdt + '''" value="Close" style="width:auto;background:#efefef"''' + cds + '''>''' + spc + '''
                        <input type="button" class="btn btn-info btn-lg disabled" data-toggle="tooltip" data-placement="top" title="지원되지 않습니다." style="cursor: not-allowed;width:auto" value="Edit">
                        </div>
                        </div>'''

        dtdt = '''<br><ul class="nav nav-tabs" role="tablist" style="height: 43px;">
<li class="nav-item" style="list-style-type:none !important">
<a id="cmtb" class="nav-link active" data-toggle="tab" role="tab" onclick="$('#compareBox').show(); $('#rawDataBox').hide(); $('#see_preview').hide(); document.getElementById('cmtb').className = 'nav-link active'; document.getElementById('prtb').className = 'nav-link'; document.getElementById('rwtb').className = 'nav-link';">비교</a>
</li>
<li class="nav-item" style="list-style-type:none !important">
<a id="rwtb" class="nav-link"        data-toggle="tab" role="tab" onclick="$('#compareBox').hide(); $('#rawDataBox').show(); $('#see_preview').hide(); document.getElementById('cmtb').className = 'nav-link'; document.getElementById('prtb').className = 'nav-link'; document.getElementById('rwtb').className = 'nav-link active';">RAW</a>
</li>
<li class="nav-item" style="list-style-type:none !important">
<a id="prtb" class="nav-link"        data-toggle="tab" role="tab" onclick="$('#compareBox').hide(); $('#rawDataBox').hide(); $('#see_preview').show(); document.getElementById('cmtb').className = 'nav-link'; document.getElementById('prtb').className = 'nav-link active'; document.getElementById('rwtb').className = 'nav-link';">미리보기</a>
</li>

</ul>
<div id=compareBox>''' + result + '''</div>
<textarea id="rawDataBox" class=form-control style="display:none;background:#eceeef;" rows=20 readonly>''' + d + '''</textarea>
<div id="see_preview" style="display:none;height: 700px; overflow: auto;padding:12px">''' + render_set(name, d) + '''</div>
'''

        if state == 'close':
            ct = ''
            cr = ''
            curs.execute("select y from erq where num = ?", [num])
            ctct = curs.fetchall()
            curs.execute("select closer from erq where num = ?", [num])
            crcr = curs.fetchall()
            if ctct and crcr:
                ct = ctct[0][0]
                cr = crcr[0][0]
                crd = '''<div class="card">
                            <div class="card-block">
                            <h4 class="card-title" style="border:none">편집 요청이 닫혔습니다.</h4>

                            <p class="card-text">''' + generateTime(ct, 'Y-m-d H:i:s') + '''에 ''' + ip_pas(cr) + '''가 편집 요청을 닫았습니다.</p>'''
                if not(w == ''):
                    crd += '''<p class="card-text">사유 : ''' + w + '''</p>'''

                crd += '''</div>
                            </div>'''
        elif state == 'accept':
            dtdt = ''
            ct = ''
            cr = ''
            curs.execute("select y from erq where num = ?", [num])
            ctct = curs.fetchall()
            curs.execute("select closer from erq where num = ?", [num])
            crcr = curs.fetchall()
            if ctct and crcr:
                ct = ctct[0][0]
                cr = crcr[0][0]
                crd = '''<div class="card">
                            <div class="card-block">
                            <h4 class="card-title" style="border:none">편집 요청이 승인되었습니다.</h4>

                            <p class="card-text">''' + generateTime(ct, 'Y-m-d H:i:s') + '''에 ''' + ip_pas(cr) + '''가 r''' + str(ap) + '''으로 승인함.</p>
                            </div>
                            </div>'''

        ip = ip_check()




        #if acl_check(name) == 1:
         #   return re_error('/ban')



        if 3 == 4:
            return re_error('/error/666')
        else:
            return easy_minify(flask.render_template(skin_check(),
                imp = [name, wiki_set(), custom(), other2([' (' + load_lang('edit') + ' 요청 ' + str(num) + ')', 0])],
                data = '''
                        <h3 style="border:0">
                        ''' + ip_pas(r) + '''가 ''' + generateTime(t, 'Y-m-d H:i:s') + '''에 요청
                        </h3>
                        <hr>
                        <div class="form-group">
                        <label class="control-label">기준 판</label>
                        r''' + str(int(str(p)) - 1) + '''
                        </div>
                        <div class="form-group">
                        <label class="control-label">편집 요약</label>
                        ''' + s + '''
                        </div>
                        <div id="edit-request-close-modal" class="modal fade" role="dialog" style="display: none;" aria-hidden="true">
                        <div class="modal-dialog">
                        <form id="edit-request-close-form" method="post">
                        <div class="modal-content">
                        <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal">×</button>
                        <h4 class="modal-title" style="border:none">편집 요청 닫기</h4>
                        </div>
                        <div class="modal-body">
                        <p>사유:</p>
                        <input type="text" name="close_reason">
                        </div>
                        <div class="modal-footer">
                        <button type="submit" class="btn btn-primary" style="width:auto">확인</button>
                        <button type="button" class="btn btn-default" data-dismiss="modal" style="background:#efefef">취소</button>
                        </div>
                        </div>
                        </form>
                        </div>
                        </div>
                        ''' + crd + dtdt,
                menu = [['w/' + url_pas(name), load_lang('return')], ['delete/' + url_pas(name), load_lang('delete')], ['move/' + url_pas(name), load_lang('move')]],
                st = 0,
                err = 0,
                is_edit_request = 1
            ))

def eqc_2(conn, num):
#if acl_check(name) == 1:
    curs = conn.cursor()
    ip = ip_check()
    admin = admin_check(1)
    name = ''
    curs.execute("select name from erq where num = ?", [num])
    naamam = curs.fetchall()
    if naamam:
        name = naamam[0][0]
    r = ''
    curs.execute("select user from erq where num = ?", [num])
    ifdfpipp = curs.fetchall()
    if ifdfpipp:
        r = ifdfpipp[0][0]
    state = ''
    curs.execute("select state from erq where num = ?", [num])
    statestate = curs.fetchall()
    if statestate:
        state = statestate[0][0]
    t = ''
    curs.execute("select time from erq where num = ?", [num])
    tt = curs.fetchall()
    if tt:
        t = tt[0][0]
    s = ''
    curs.execute("select send from erq where num = ?", [num])
    ss = curs.fetchall()
    if ss:
        s = ss[0][0]
    d = ''
    curs.execute("select data from erq where num = ?", [num])
    dd = curs.fetchall()
    if dd:
        d = dd[0][0]

    if not(r == ip_check()) and not(admin == 1):
        return re_error('/error/3')

    curs.execute("update erq set state = ? where num = ?", ['close', str(num)])
    curs.execute("update erq set closer = ? where num = ?", [ip, str(num)])
    curs.execute("update erq set y = ? where num = ?", [get_time(), str(num)])
    #flask.request.form.get('otent', '')

    return redirect('/edit_request/' + str(num))

def eqa_2(conn, num):
#if acl_check(name) == 1:
    curs = conn.cursor()
    ip = ip_check()
    admin = admin_check(5)
    name = ''
    curs.execute("select name from erq where num = ?", [num])
    naamam = curs.fetchall()
    if naamam:
        name = naamam[0][0]
    r = ''
    curs.execute("select user from erq where num = ?", [num])
    ifdfpipp = curs.fetchall()
    if ifdfpipp:
        r = ifdfpipp[0][0]
    state = ''
    curs.execute("select state from erq where num = ?", [num])
    statestate = curs.fetchall()
    if statestate:
        state = statestate[0][0]
    t = ''
    curs.execute("select time from erq where num = ?", [num])
    tt = curs.fetchall()
    if tt:
        t = tt[0][0]
    s = ''
    curs.execute("select send from erq where num = ?", [num])
    ss = curs.fetchall()
    if ss:
        s = ss[0][0]
    d = ''
    curs.execute("select data from erq where num = ?", [num])
    dd = curs.fetchall()
    if dd:
        d = dd[0][0]
    l = ''
    curs.execute("select leng from erq where num = ?", [num])
    ll = curs.fetchall()
    if ll:
        l = ll[0][0]

    if int(l) > 0:
        l = '+' + str(int(l))

    if int(l) == 0:
        l = '0'

    if int(l) < 0:
        l = str(int(l))

    if getacl(name, 'edit') == 0:
        return re_error('/error/3')

    curs.execute("select id from history where title = ? order by id + 0 desc limit 1", [name])
    id_data = curs.fetchall()

    curs.execute("update erq set state = ? where num = ?", ['accept', str(num)])
    curs.execute("update erq set closer = ? where num = ?", [ip, str(num)])
    curs.execute("update erq set y = ? where num = ?", [get_time(), str(num)])
    curs.execute("update data set data = ? where title = ?", [d, name])
    curs.execute("update data set date = ? where title = ?", [get_time(), name])
    curs.execute("update erq set ap = ? where num = ?", [str(int(id_data[0][0]) + 1) if id_data else '1', str(num)])



    curs.execute("insert into history (id, title, data, date, ip, send, leng, hide, i, q, qn) values (?, ?, ?, ?, ?, ?, ?, '', ?, ?, ?)", [
        str(int(id_data[0][0]) + 1) if id_data else '1',
        name,
        d,
        get_time(),
        r,
        s,
        l,
        '',
        'O',
        num
    ])

    curs.execute("update star set lstedt = ? where doc = ?", [get_time(), name])

    conn.commit()

    return redirect('/edit_request/' + str(num))


def viewEditRequest(conn, num):
    curs = conn.cursor()
    #                     0      1       2       3      4        5           6        7          8            9
    curs.execute("select num, baserev, state, content, log, applied_rev, requester, closer, request_time, doctitle from thread_edit_requests where num = ?", [num])
    erqData = curs.fetchall()
    if not erqData:
        curs.execute("select num from erq where num = ?", [num])
        if curs.fetchall():
            return eq_2(conn, num)
        else:
            return showError('편집 요청을 찾을 수 없습니다.')

    if getperm(erqData[0][9], 'read') != 1:
        return showError('편집 요청을 열람할 수 없습니다.<br><br>액세스가 거부되었습니다.')

    content = '''
        <div>
            <h2>''' + ip_pas(erqData[0][6]) + ''' 사용자가 ''' + generateTime(erqData[0][8]) + '''에 요청</h2>
            <p>기준 판 r''' + erqData[0][1] + '''</p>
            <p>편집 요약: ''' + html.escape(erqData[0][4]) + '''</p>
        </div>
    '''




def nerq_2(conn, name):
    curs = conn.cursor()

    if re.search('^사용자:', name):
        ns = '사용자'
    elif re.search('^분류:', name):
        ns = '분류'
    elif re.search('^틀:', name):
        ns = '틀'
    elif re.search('^휴지통:', name):
        ns = '휴지통'
    elif re.search('^파일:', name):
        ns = '파일'
    elif re.search('^' + wiki_set()[0] + ':', name):
        ns = wiki_set()[0]
    else:
        ns = '문서'

    ip = ip_check()
    #if acl_check(name) == 1:
     #   return re_error('/ban')

    if getacl(name, 'read') == 0:
        return noread(conn, name)

    if ban_check() == 1:
        return re_error('/ban')

    if flask.request.method == 'POST':
        perm = getacl(name, 'edit_request')
        if perm == 0:
            return re_error('/error/3')

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
            return re_error('/error/666')
    else:
        perm = getacl(name, 'edit_request')
        if perm == 0:
            return easy_minify(flask.render_template(skin_check(),
                imp = ['문제가 발생했습니다!', wiki_set(), custom(), other2([0, 0])],
                data = '<h2 style="border:none;font-weight:600">' + aclmsg(name, 'edit_request')[1] + ' 편집요청 권한이 부족합니다. ' + aclmsg(name, 'edit_request')[2] + ' 해당 문서의 <a href="/acl/' + url_pas(name) + '">ACL 탭</a>을 확인하시기 바랍니다.</h2>',
                menu = 0
            ))
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
                    <input class="form-control" name="send" type="text" style="width:100% !important;">
                    ''' + captcha_get() + '''<br><br><p>''' + getConfig('edit_warning', '') + '''</p><br>
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
                    ''' + dfnmgrtutei + '''<br><ul class="nav nav-tabs" role="tablist" style="height: 38px;">
        <li class="nav-item" style="list-style-type:none !important">
        <a id="edtb" class="nav-link active" data-toggle="tab" href="#edit" role="tab" onclick="document.getElementById(\'content\').style.display = \'block\';document.getElementById(\'see_preview\').style.display = \'none\'; document.getElementById('edtb').className = 'nav-link active'; document.getElementById('prtb').className = 'nav-link';">편집</a>
        </li>
        <li class="nav-item" style="list-style-type:none !important">
        <a id="prtb" class="nav-link" data-toggle="tab" role="tab" aria-expanded="false" id="preview" onclick="document.getElementById('edtb').className = 'nav-link'; document.getElementById('prtb').className = 'nav-link active'; do_preview(\'''' + name + '''\');document.getElementById(\'content\').style.display = \'none\';document.getElementById(\'see_preview\').style.display = \'block\'; ">미리보기</a>
        </li>

        </ul>
                    <textarea class="form-control" id="content" rows="25" class=form-control name="content"''' + fdvsdvgbrtf + ''' style="width:100% !important;">''' + html.escape(re.sub('\n$', '', data)) + '''</textarea>
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
