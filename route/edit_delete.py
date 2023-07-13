from .tool.func import *

def edit_delete_2(conn, name, app_var):
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

    if getacl(name, 'read') == 0:
        return noread(conn, name)

    ip = ip_check()

    perm = getacl(name, 'edit')
    if perm == 0:
        return easy_minify(flask.render_template(skin_check(),
            imp = ['문제가 발생했습니다!', wiki_set(), custom(), other2([0, 0])],
            data = '<h2 style="border:none;font-weight:600">' + aclmsg(name, 'edit')[1] + ' 편집 권한이 부족합니다. ' + aclmsg(name, 'edit')[2] + ' 해당 문서의 <a href="/acl/' + url_pas(name) + '">ACL 탭</a>을 확인하시기 바랍니다.</h2>',
            menu = 0
        ))
    perm = getacl(name, 'delete')
    if perm == 0:
        return easy_minify(flask.render_template(skin_check(),
            imp = ['문제가 발생했습니다!', wiki_set(), custom(), other2([0, 0])],
            data = '<h2 style="border:none;font-weight:600">' + aclmsg(name, 'delete')[1] + ' 삭제 권한이 부족합니다. ' + aclmsg(name, 'delete')[2] + ' 해당 문서의 <a href="/acl/' + url_pas(name) + '">ACL 탭</a>을 확인하시기 바랍니다.</h2>',
            menu = 0
        ))


    content = '''
        <form id="deleteForm" method="post">
            <div class="form-group">
            <label class="control-label" for="logInput">요약</label>
            <input type="text" id="logInput" name="send" class="form-control" value="">
            </div>
            <label>
            <input type="checkbox" name="agree" id="agreeCheckbox" value="Y">&nbsp;문서 이동 목적이 아닌, 삭제하기 위함을 확인합니다.
            </label>
            <p>
            <b>알림!&nbsp;:</b>&nbsp;문서의 제목을 변경하려는 경우 <a href="/move/''' + url_pas(name) + '''">문서 이동</a> 기능을 사용해주세요. 문서 이동 기능을 사용할 수 없는 경우 토론 기능이나 게시판을 통해 대행 요청을 해주세요.
            </p>
            <div class="btns">
            <button type="reset" class="btn btn-secondary">초기화</button>
            <button type="submit" class="btn btn-primary" id="submitBtn">삭제</button>
            </div>
            ''' + captcha_get() + '''
        </form>
    '''
    if flask.request.method == 'POST':
        if getacl(name, 'delete') == 0:
            return re_error('/error/3')

        if re.search('^사용자:', name):
            if name.replace('/', '') == name:
                curs.execute("select title from data where title = ?", [name])
                if not curs.fetchall():
                    return redirect('/w/' + url_pas(name))

                return easy_minify(flask.render_template(skin_check(),
                    imp = [name, wiki_set(), custom(), other2([' (삭제)', 0])],
                    data = alertBalloon('disable_user_document') + content,
                    menu = [['w/' + url_pas(name), load_lang('return')]],
                    st = 5,
                    err = 1
                ))

        if captcha_post(flask.request.form.get('g-recaptcha-response', '')) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)

        curs.execute("select data from data where title = ?", [name])
        data = curs.fetchall()
        if data:
            today = get_time()
            if len(data[0][0]) == 0:
                leng = '0'
            else:
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

            curs.execute("update star set lstedt = ? where doc = ?", [get_time(), name])

            curs.execute("select title, link from back where title = ? and not type = 'cat' and not type = 'no'", [name])
            for data in curs.fetchall():
                curs.execute("insert into back (title, link, type) values (?, ?, 'no')", [data[0], data[1]])

            curs.execute("delete from back where link = ?", [name])
            curs.execute("delete from data where title = ?", [name])
            conn.commit()

        return redirect('/w/' + url_pas(name))
    else:
        curs.execute("select title from data where title = ?", [name])
        if not curs.fetchall():
            return showError('문서를 찾을 수 없습니다.')

        return easy_minify(flask.render_template(skin_check(),
            imp = [name, wiki_set(), custom(), other2([' (삭제)', 0])],
            data = content,
            menu = [['w/' + url_pas(name), load_lang('return')]],
            st = 5
        ))

def blowupDocuments(conn):
    curs = conn.cursor();
    if admin_check() != 1:
        return re_error('/error/3');

    content = '''
        <form method=post>
            <div>
                각 줄에 삭제할 문서를 입력합니다.
            </div>
            <div class=form-group>
                <textarea name=documents id=documentsList class=form-control rows=25></textarea>
            </div>
            <div class=btns>
                <button type=reset class="btn btn-secondary">초기화</button>
                <button type=submit class="btn btn-primary">확인</button>
            </div>
        </form>
    ''';

    if flask.request.method == 'POST':
        log = '';
        documentList = getForm('documents').split('\n');
        for i in documentList:
            curs.execute("select title from data where title = ?", [i.replace('\r', '')]);
            if not(curs.fetchall()):
                log += '[오류] 문서가 존재하지 않음 - ' + i + '\n';
            else:
                if re.search("^사용자:", i):
                    log += '[오류] disable_user_document';
                    continue;
                curs.execute("select data from data where title = ?", [i.replace('\r', '')]);
                dbData = curs.fetchall();
                if dbData:
                    if len(dbData[0][0]) < 1:
                        changes = '0';
                    else:
                        changes = '-' + str(len(dbData[0][0]));
                else:
                    changes = '0';
                history_plus(
                    i.replace('\r', ''),
                    '',
                    get_time(),
                    ip_check(),
                    '일괄 삭제',
                    changes,
                    '삭제'
                );
                curs.execute("delete from data where title = ?", [i.replace('\r', '')]);
                log += '[완료] ' + i + '\n';
            conn.commit();
        return easy_minify(flask.render_template(skin_check(),
            imp = ['일괄 문서 삭제', wiki_set(), custom(), other2([0, 0])],
            data = '''<div class=form-group>
                <textarea id=logs rows=10 class=form-control readonly>''' + log + '''</textarea></div>
            ''' + content,
            menu = 0
        ));

    return easy_minify(flask.render_template(skin_check(),
        imp = ['일괄 문서 삭제', wiki_set(), custom(), other2([0, 0])],
        data = content,
        menu = 0
    ));