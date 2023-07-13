from .tool.func import *

voteTypLst = ['공개', '비공개', '기명', 'open']

def getUserDate(conn, un):
    curs = conn.cursor()
    curs.execute("select date from user where id = ?", [un])
    d = curs.fetchall()
    if d:
        return re.sub('[ ]\d{1,2}[:]\d{1,2}[:]\d{1,2}', '', d[0][0])
    else:
        return '9999-99-99'

def voteScreen(conn, num):
    curs = conn.cursor()

    curs.execute("select num, name, start, end, deserve, options, mode from vote where num = ?", [num])
    dbData = curs.fetchall()
    voteTitle = '무제'
    if dbData:
        voteTitle = dbData[0][1]
        data = ''
        data += '시작일 : ' + dbData[0][2] + '<br>'
        data += '종료일 : ' + dbData[0][3] + '<br>'
        data += '투표 방식 : ' + dbData[0][6] + ' 투표<br>'
        if not(dbData[0][6] in ['공개', '비공개', '기명']):
            return showError('투표가 올바르지 않습니다.')
        adminMenu = '<span class="pull-right" style="display: inline-block;">'
        if getperm('delete_vote') == 1:
            adminMenu += '<a href="/admin/vote/' + num + '/delete" class="btn btn-danger btn-sm" onclick="return confirm(\'삭제하시겠습니까?\');">[ADMIN] 삭제</a>'
        if getperm('edit_vote') == 1:
            adminMenu += ' <a href="/admin/vote/' + num + '/edit" class="btn btn-warning btn-sm">[ADMIN] 편집</a></span>'
        if admin_check() == 1:
            delAttr = ''
            if re.sub('[ ]\d{1,2}[:]\d{1,2}[:]\d{1,2}', '', get_time()) >= dbData[0][3]:
                delAttr = " disabled"
            adminMenu += ' <a href="/admin/vote/' + num + '/burst" class="btn btn-danger btn-sm" onclick="return confirm(\'이 투표를 터뜨리시겠습니까?\');"' + delAttr + '>[ADMIN] 터뜨리기</a></span>'
        adminMenu += '</span>'
        data += '<br><h2 style="border:none">투표하기 ' + adminMenu + '</h2>'
        curs.execute("select data, username, date from vodedata where num = ? order by data, date asc", [num])
        if not re.sub('[ ]\d{1,2}[:]\d{1,2}[:]\d{1,2}', '', get_time()) >= dbData[0][3] and admin_check() != 1:
            nodisp = 'display: none;" hidden'
        else:
            nodisp = '"'
        data += '<textarea rows=5 readonly style="' + nodisp + ' class="form-control">'
        for i in curs.fetchall():
            if dbData[0][6] == '기명':
                data += i[2] + ' (UTC) - "' + i[1] + '" 사용자가 투표: ' + i[0] + '\n'
            elif dbData[0][6] == '공개':
                if admin_check() == 1:
                    data += '[개발자] ' + i[2] + ' (UTC) - "' + i[1] + '" 사용자가 투표: ' + i[0] + '\n'
                else:
                    data += i[2] + ' (UTC) - "' + i[1] + '" 사용자가 투표 완료.\n'
            else:
                if admin_check() == 1:
                    data += '[개발자] ' + i[2] + ' (UTC) - "' + i[1] + '" 사용자가 투표: ' + i[0] + '\n'
                else:
                    data += '어떤 사용자가 어디론가 투표\n'
        data += '</textarea><hr>'
        if not('state' in flask.session):
            data += '로그인이 필요합니다.'
        else:
            if re.sub('[ ]\d{1,2}[:]\d{1,2}[:]\d{1,2}', '', get_time()) >= dbData[0][3]:
                data += '기한 만료.'
            elif re.sub('[ ]\d{1,2}[:]\d{1,2}[:]\d{1,2}', '', get_time()) < dbData[0][2]:
                data += '투표가 시작되지 않았음.'
            elif re.sub('[ ]\d{1,2}[:]\d{1,2}[:]\d{1,2}', '', getUserDate(conn, ip_check())) > dbData[0][4]:
                data += '자격 조건 미달.'
            else:
                curs.execute("select data from vodedata where username = ? and num = ?", [ip_check(), num])
                if curs.fetchall():
                    data += '투표 완료.'
                else:
                    data += dbData[0][5] + '<br><div class="btns pull-right"><button type="submit" class="btn btn-info" style="width: 120px;">투표</button></div>'
    else:
        return showError('투표를 찾을 수 없습니다.')

    if flask.request.method == 'POST':
        curs.execute("select num, name, start, end, deserve, options, mode from vote where num = ?", [num])
        dbData = curs.fetchall()
        if not(dbData):
            return showError('투표를 찾을 수 없습니다.')
        if not('state' in flask.session):
            return showError('로그인이 필요합니다.')
        if re.sub('[ ]\d{1,2}[:]\d{1,2}[:]\d{1,2}', '', get_time()) >= dbData[0][3]:
            return showError('기한이 만료되었습니다.')
        elif re.sub('[ ]\d{1,2}[:]\d{1,2}[:]\d{1,2}', '', get_time()) < dbData[0][2]:
            return showError('투표가 아직 시작되지 않았습니다.')
        elif re.sub('[ ]\d{1,2}[:]\d{1,2}[:]\d{1,2}', '', getUserDate(conn, ip_check())) > dbData[0][4]:
            return showError('자격 조건을 충족하지 않습니다.')
        if ban_check() == 1:
            return re_error('/ban')
        curs.execute("select data from vodedata where username = ? and num = ?", [ip_check(), num])
        if curs.fetchall():
            return showError('투표를 이미 완료했습니다.')
        if getForm('voteOptionsSelect', None) == None:
            return easy_minify(flask.render_template(skin_check(),
                imp = [voteTitle, wiki_set(), custom(), other2([' (투표)', 0])],
                data =  alertBalloon('투표한 옵션이 없습니다.') + '''
                        <form method="post" onsubmit="return confirm('계속하시겠습니까? 취소 및 수정은 불가능합니다.');">
                            ''' + data + '''
                        </form>
                        ''',
                menu = 0,
                err = 1,
                vote = 1
            ))
        curs.execute("insert into vodedata (num, username, data, date) values (?, ?, ?, ?)", [num, ip_check(), getForm('voteOptionsSelect'), get_time()])
        conn.commit()
        return redirect('/vote/' + num)
    else:
        return easy_minify(flask.render_template(skin_check(),
            imp = [voteTitle, wiki_set(), custom(), other2([' (투표)', 0])],
            data =  '''
                    <form method="post" onsubmit="return confirm('계속하시겠습니까? 취소 및 수정은 불가능합니다.');">
                        ''' + data + '''
                    </form>
                    ''',
            menu = 0,
            vote = 1,
            smsub = ' 투표'
        ))

def createVote(conn):
    curs = conn.cursor()

    if getperm('create_vote') == 0:
        return showError('권한이 부족합니다.')

    data = '''
        <form method="post" onsubmit="return confirm('등록하시겠습니까?');">
            <label>투표 제목</label><br>
            <input type="text" name="voteTitle" class="form-control"><br><br>

            <div style="display: inline-block; width: 100%;">
                <div style="display: inline-block; width: 49%; float: left;">
                    <label>시작일 (UTC)</label><br>
                    <input type="text" name="start" class="form-control">
                </div>
                <div style="display: inline-block; width: 49%; float: right;">
                    <label>종료일 (UTC)</label><br>
                    <input type="text" name="end" class="form-control">
                </div>
            </div><br><br>

            <label>투표 자격</label><br>
            <input type="text" name="votingQualifications" class="form-control"><br><br>

            <label>답변 종류 (개행으로 구분)</label><br>
            <textarea rows="8" name="options" class="form-control"></textarea><br><br>

            <label>투표 방식</label><br>
            <select name="voteMode" style="width: 100%;" class="form-control">
                <option value="공개">공개 투표</option>
                <option value="비공개">비공개 투표</option>
                <option value="기명">기명 투표</option>
            </select><br><br>

            <div class="btns pull-right">
                <button type="submit" class="btn btn-info" style="width: 120px;">등록</button>
            </div>
        </form>
    '''

    if flask.request.method == 'POST':
        if len(getForm('voteTitle')) < 1:
            return easy_minify(flask.render_template(skin_check(),
                imp = ['투표 등록', wiki_set(), custom(), other2(['', 0])],
                data =  alertBalloon('투표 제목이 비었습니다.') + '''<form method="post" onsubmit="return confirm('등록하시겠습니까?');">
                            ''' + data + '''
                        </form>
                        ''',
                menu = 0,
                err = 1
            ))
        if stringInFormat('\d{1,}[-]\d{1,2}[-]\d{1,2}', getForm('start')) == 0:
            return easy_minify(flask.render_template(skin_check(),
                imp = ['투표 등록', wiki_set(), custom(), other2(['', 0])],
                data =  alertBalloon('시작일의 값은 YYYY-MM-DD이여야 합니다. 시간은 입력하지 않습니다.') + '''<form method="post" onsubmit="return confirm('등록하시겠습니까?');">
                            ''' + data + '''
                        </form>
                        ''',
                menu = 0,
                err = 1
            ))
        if stringInFormat('\d{1,}[-]\d{1,2}[-]\d{1,2}', getForm('end')) == 0:
            return easy_minify(flask.render_template(skin_check(),
                imp = ['투표 등록', wiki_set(), custom(), other2(['', 0])],
                data =  alertBalloon('종료일의 값은 YYYY-MM-DD이여야 합니다. 시간은 입력하지 않습니다.') + '''<form method="post" onsubmit="return confirm('등록하시겠습니까?');">
                            ''' + data + '''
                        </form>
                        ''',
                menu = 0,
                err = 1
            ))
        if stringInFormat('\d{1,}[-]\d{1,2}[-]\d{1,2}', getForm('votingQualifications')) == 0:
            return easy_minify(flask.render_template(skin_check(),
                imp = ['투표 등록', wiki_set(), custom(), other2(['', 0])],
                data =  alertBalloon('투표자격은 해당 날짜 이전에 가입했나를 따집니다. 또한, 해당 값은 YYYY-MM-DD이여야 합니다. 시간은 입력하지 않습니다.') + '''<form method="post" onsubmit="return confirm('등록하시겠습니까?');">
                            ''' + data + '''
                        </form>
                        ''',
                menu = 0,
                err = 1
            ))
        options = getForm('options').split('\n')
        if len(options) < 2:
            return easy_minify(flask.render_template(skin_check(),
                imp = ['투표 등록', wiki_set(), custom(), other2(['', 0])],
                data =  alertBalloon('답변들의 갯수는 2개 이상이여야 합니다.') + '''<form method="post" onsubmit="return confirm('등록하시겠습니까?');">
                            ''' + data + '''
                        </form>
                        ''',
                menu = 0,
                err = 1
            ))
        if not(getForm('voteMode') in voteTypLst):
            return easy_minify(flask.render_template(skin_check(),
                imp = ['투표 등록', wiki_set(), custom(), other2(['', 0])],
                data =  alertBalloon('투표 방식이 올바르지 않습니다.') + '''<form method="post" onsubmit="return confirm('등록하시겠습니까?');">
                            ''' + data + '''
                        </form>
                        ''',
                menu = 0,
                err = 1
            ))

        curs.execute("select num from vote order by CAST(num AS INTEGER) desc")
        ndata = curs.fetchall()
        if ndata:
            lastID = int(ndata[0][0])
        else:
            lastID = 0

        optionsHTML = ''
        for i in range(0, len(options)):
            optionsHTML += '''<label><input type="radio" name="voteOptionsSelect" value="''' + options[i] + '''"> ''' + options[i] + '''</label><br>'''

        curs.execute("insert into vote (num, name, start, end, deserve, options, mode) values (?, ?, ?, ?, ?, ?, ?)", [str(lastID + 1), getForm('voteTitle'), getForm('start'), getForm('end'), getForm('votingQualifications'), optionsHTML, getForm('voteMode')])
        conn.commit()
        return redirect('/vote/' + str(lastID + 1))
    else:
        return easy_minify(flask.render_template(skin_check(),
            imp = ['투표 등록', wiki_set(), custom(), other2(['', 0])],
            data =  alertBalloon('한 번이라도 오류가 발생하면 입력한 자료들이 사라집니다.', 'success', '경고') + '''
                    <form method="post" onsubmit="return confirm('등록하시겠습니까?');">
                        ''' + data + '''
                    </form>
                    ''',
            menu = 0
        ))

def editVote(conn, num):
    curs = conn.cursor()

    if getperm('edit_vote') == 0:
        return showError('권한이 부족합니다.')

    curs.execute("select num, name, start, end, deserve, options, mode from vote where num = ?", [num])
    dbData = curs.fetchall()
    if not(dbData):
        return showError('투표를 찾을 수 없습니다.')
    else:
        data = '''
            <form method="post">
                <label>투표 제목</label><br>
                <input type="text" name="voteTitle" class="form-control" value="''' + dbData[0][1] + '''"><br><br>

                <div style="display: inline-block; width: 100%;">
                    <div style="display: inline-block; width: 49%; float: left;">
                        <label>시작일 (UTC)</label><br>
                        <input type="text" name="start" class="form-control" value="''' + dbData[0][2] + '''">
                    </div>
                    <div style="display: inline-block; width: 49%; float: right;">
                        <label>종료일 (UTC)</label><br>
                        <input type="text" name="end" class="form-control" value="''' + dbData[0][3] + '''">
                    </div>
                </div><br><br>

                <label>투표 자격</label><br>
                <input type="text" name="votingQualifications" class="form-control" value="''' + dbData[0][4] + '''"><br><br>

                <label>답변 종류 (개행으로 구분)</label><br>
                <textarea rows="8" name="options" class="form-control"></textarea><br><br>

                <label>투표 방식</label><br>
                <select name="voteMode" style="width: 100%;" class="form-control" size=3>
                    <option value="공개">공개 투표</option>
                    <option value="비공개">비공개 투표</option>
                    <option value="기명">기명 투표</option>
                    <option value=open>기명 투표</option>
                </select><br><br>

                <div class="btns pull-right">
                    <button type="submit" class="btn btn-info" style="width: 120px;">확인</button>
                </div>
            </form>
        '''

        if flask.request.method == 'POST':
            if len(getForm('voteTitle')) < 1:
                return showError('투표 제목이 비었습니다.')
            if stringInFormat('\d{1,}[-]\d{1,2}[-]\d{1,2}', getForm('start')) == 0:
                return showError('시작일의 값은 YYYY-MM-DD이여야 합니다. 시간은 입력하지 않습니다.')
            if stringInFormat('\d{1,}[-]\d{1,2}[-]\d{1,2}', getForm('end')) == 0:
                return showError('종료일의 값은 YYYY-MM-DD이여야 합니다. 시간은 입력하지 않습니다.')
            if stringInFormat('\d{1,}[-]\d{1,2}[-]\d{1,2}', getForm('votingQualifications')) == 0:
                return showError('투표자격은 해당 날짜 이전에 가입했나를 따집니다. 또한, 해당 값은 YYYY-MM-DD이여야 합니다. 시간은 입력하지 않습니다.')
            options = getForm('options').split('\n')
            if len(options) < 2:
                return showError('답변들의 갯수는 2개 이상이여야 합니다.')
            if not(getForm('voteMode') in voteTypLst):
                return showError('투표 방식이 올바르지 않습니다.')

            optionsHTML = ''
            for i in range(0, len(options)):
                optionsHTML += '''<label><input type="radio" name="voteOptionsSelect" value="''' + options[i] + '''"> ''' + options[i] + '''</label><br>'''

            curs.execute("update vote set num = ?, name = ?, start = ?, end = ?, deserve = ?, options = ?, mode = ? where num = ?", [dbData[0][0], getForm('voteTitle'), getForm('start'), getForm('end'), getForm('votingQualifications'), optionsHTML, getForm('voteMode'), num])
            conn.commit()
            return redirect('/vote/' + dbData[0][0])
        else:
            return easy_minify(flask.render_template(skin_check(),
                imp = [dbData[0][1], wiki_set(), custom(), other2([' (투표 편집)', 0])],
                data =  '''<form method="post">
                            ''' + data + '''
                        </form>
                        ''',
                menu = 0
            ))

def deleteVote(conn, num):
    curs = conn.cursor()
    if getperm('delete_vote') == 0:
        return showError('권한이 부족합니다.')
    curs.execute("select num from vote where num = ?", [num])
    if not(curs.fetchall()):
        return showError('투표를 찾을 수 없습니다.')

    curs.execute("delete from vote where num = ?", [num])
    curs.execute("delete from vodedata where num = ?", [num])

    conn.commit()

    return redirect('/admin/create_vote')