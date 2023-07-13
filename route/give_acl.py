from .tool.func import *

def give_acl_2(conn, name):
    curs = conn.cursor()

    try:
        ns = getNamespace(name.split(':')[0])
    except:
        ns = '문서'

    #구버전 브라우져는 Non-JS 페이지로 돌리기
    ua = flask.request.headers.get('User-Agent')
    nojs = flask.request.args.get('nojs', None)
    if nojs != '1':
        nojs = None
    if re.search('[;] MSIE \d{1,1}[.]\d{1,5};', ua) and not(nojs): # MS IE 1.0부터 9.0까지 인식
        return redirect('/acl/' + url_pas(name) + '?nojs=1')

    curs.execute("delete from seedacl where (exp < ? and not exp like '0' and not exp like '')", [get_time()])
    curs.execute("delete from nsacl where (exp < ? and not exp like '0' and not exp like '')", [get_time()])
    conn.commit()

    if ns in getNamespaces(unuseableOnly = True):
        return re_error('/error/9001')

    wikiname = wiki_set()[0]

    perm = getacl(name, 'acl')
    curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'nsacl'])
    if curs.fetchall():
        perm = 1

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
        perm = getacl(name, 'acl')
        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'nsacl'])
        if curs.fetchall():
            perm = 1
        if perm != 1:
            return flask.jsonify( { "status": str(aclmsg(name, 'acl')[1] + ' ACL ' + load_lang('authority_error') + ' ' + aclmsg(name, 'acl')[2] + ' 해당 문서의 <a href="/acl/' + url_pas(name) + '">ACL 탭</a>을 확인하시기 바랍니다. ') } )
        tbodyData = ''
        if flask.request.form['mode'] == 'delete':
            if flask.request.form['isNS'] != 'Y':
                id = flask.request.form['id']
                what = flask.request.form['type']
                curs.execute("select id, type, perm, how, exp, what from seedacl where name = ? and id = ? and what = ? order by id asc", [name, id, what])
                dat = curs.fetchall()
                if dat:
                    history_plus(
                            name,
                            '<h2>이 리비젼을 볼 수 없습니다.</h2>',
                            get_time(),
                            ip_check(),
                            '',
                            '0',
                            'delete,' + dat[0][5] + ',' + dat[0][3] + ',' + dat[0][1] + ':' + dat[0][2] + '으로 ACL 변경'
                        )

                    #curs.execute("select id, type, perm, how, exp from seedacl where name = ? and what = 'wtc' order by id4 asc", [name])
                    curs.execute("delete from seedacl where name = ? and id = ? and what = ?", [name, id, what])

                tbodyData = ''
                curs.execute("select id, type, perm, how, exp from seedacl where name = ? and what = ? order by cast(id as integer) asc", [name, what])
                alt = curs.fetchall()
                if not(alt):
                    tbodyData = '''<tr class="ui-sortable-handle">
                            <td colSpan="5" style="text-align: center;">(규칙이 존재하지 않습니다. 이름공간 ACL이 적용됩니다.)</td>
                            </tr>'''
                else:
                    ic = 1
                    for acldata in alt:
                        if acldata[3] == 'allow':
                            tt = '허용'
                        elif acldata[3] == 'deny':
                            tt = '거부'
                        else:
                            tt = '없음'
                        if acldata[1] == "comment" and acldata[2] == '-':
                            tbodyData += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td colspan=4><hr></td><td>'''
                        else:
                            tbodyData += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td>''' + str(ic) + '''</td>
                                        <td>''' + acldata[1] + ':' + acldata[2] + '''</td>
                                        <td>''' + tt + '''</td>
                                        <td>''' + generateTime(acldata[4], f = 1) + '''</td>
                                        <td>'''

                        if perm == 1:
                            tbodyData += '''<button type="submit" class="btn btn-danger btn-sm">삭제</button>'''

                        tbodyData += '''</td>
                                </tr>'''
                        ic += 1
                conn.commit()
                return tbodyData
            elif flask.request.form['isNS'] == 'Y':
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'nsacl'])
                if not curs.fetchall():
                    return ''
                id = flask.request.form['id']
                what = flask.request.form['type']
                curs.execute("select id, type, perm, how, exp, what from nsacl where ns = ? and id = ? and what = ? order by id asc", [ns, id, what])
                dat = curs.fetchall()
                if dat:

                    #curs.execute("select id, type, perm, how, exp from seedacl where name = ? and what = 'wtc' order by id4 asc", [name])
                    curs.execute("delete from nsacl where ns = ? and id = ? and what = ?", [ns, id, what])

                tbodyData = ''
                curs.execute("select id, type, perm, how, exp from nsacl where ns = ? and what = ? order by cast(id as integer) asc", [ns, what])
                alt = curs.fetchall()
                if not(alt):
                    tbodyData = '''<tr class="ui-sortable-handle">
                            <td colSpan="5" style="text-align: center;">(규칙이 존재하지 않습니다. 모두 거부됩니다.)</td>
                            </tr>'''
                else:
                    ic = 1
                    for acldata in alt:
                        if acldata[3] == 'allow':
                            tt = '허용'
                        elif acldata[3] == 'deny':
                            tt = '거부'
                        else:
                            tt = '없음'
                        if acldata[1] == "comment" and acldata[2] == '-':
                            tbodyData += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td colspan=4><hr></td><td>'''
                        else:
                            tbodyData += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td>''' + str(ic) + '''</td>
                                        <td>''' + acldata[1] + ':' + acldata[2] + '''</td>
                                        <td>''' + tt + '''</td>
                                        <td>''' + generateTime(acldata[4], f = 1) + '''</td>
                                        <td>'''

                        if perm == 1:
                            tbodyData += '''<button type="submit" class="btn btn-danger btn-sm">삭제</button>'''

                        tbodyData += '''</td>
                                </tr>'''
                        ic += 1
                conn.commit()
                return tbodyData
        elif flask.request.form['mode'] == 'insert':
            if flask.request.form['isNS'] != 'Y':
                what = flask.request.form['type']
                allid = 1
                act = flask.request.form['action']
                exp = flask.request.form['expire']
                typ = flask.request.form['condType']
                permn = flask.request.form['condVal']
                curs.execute("select id from seedacl where name = ? and what = ? order by cast(id as integer) desc limit 1", [name, what])

                adsfdsf = curs.fetchall()
                if adsfdsf:
                    allid = int(adsfdsf[0][0])
                else:
                    allid = 1

                allid = 1
                while(1):
                    curs.execute("select id from seedacl where name = ? and what = ? and id = ?", [name, what, str(allid)])
                    if curs.fetchall():
                        allid += 1
                        continue
                    else:
                        break

                history_plus(
                        name,
                        '<h2>이 리비젼을 볼 수 없습니다.</h2>',
                        get_time(),
                        ip_check(),
                        '',
                        '0',
                        'insert,' + what + ',' + act + ',' + typ + ':' + permn + '으로 ACL 변경'
                    )
                end = int(number_check(exp))

                time = datetime.datetime.now()
                plus = datetime.timedelta(seconds = end)
                r_time = (time + plus).strftime("%Y-%m-%d %H:%M:%S")
                if exp == '0':
                    r_time = '0'
                #curs.execute("select id, type, perm, how, exp from seedacl where name = ? and what = 'wtc' order by id4 asc", [name])
                curs.execute("insert into seedacl (id, type, perm, how, exp, name, what, id4) values (?, ?, ?, ?, ?, ?, ?, ?)", [str(allid), typ, permn, act, r_time, name, what, str(allid).zfill(4)])

                tbodyData = ''
                curs.execute("select id, type, perm, how, exp from seedacl where name = ? and what = ? order by cast(id as integer) asc", [name, what])
                alt = curs.fetchall()
                if not(alt):
                    tbodyData = '''<tr class="ui-sortable-handle">
                            <td colSpan="5" style="text-align: center;">(규칙이 존재하지 않습니다. 이름공간 ACL이 적용됩니다.)</td>
                            </tr>'''
                else:
                    ic = 1

                    for acldata in alt:
                        if acldata[3] == 'allow':
                            tt = '허용'
                        elif acldata[3] == 'deny':
                            tt = '거부'
                        else:
                            tt = '없음'
                        if acldata[1] == "comment" and acldata[2] == '-':
                            tbodyData += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td colspan=4><hr></td><td>'''
                        else:
                            tbodyData += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td>''' + str(ic) + '''</td>
                                        <td>''' + acldata[1] + ':' + acldata[2] + '''</td>
                                        <td>''' + tt + '''</td>
                                        <td>''' + generateTime(acldata[4], f = 1) + '''</td>
                                        <td>'''

                        if perm == 1:
                            tbodyData += '''<button type="submit" class="btn btn-danger btn-sm">삭제</button>'''

                        tbodyData += '''</td>
                                </tr>'''
                        ic += 1
                conn.commit()
                return tbodyData
            elif flask.request.form['isNS'] == 'Y':
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'nsacl'])
                if not curs.fetchall():
                    return ''
                what = flask.request.form['type']
                allid = 1
                act = flask.request.form['action']
                exp = flask.request.form['expire']
                typ = flask.request.form['condType']
                permn = flask.request.form['condVal']
                curs.execute("select id from nsacl where ns = ? and what = ? order by cast(id as integer) desc limit 1", [ns, what])

                adsfdsf = curs.fetchall()
                if adsfdsf:
                    allid = int(adsfdsf[0][0])
                else:
                    allid = 1

                allid = 1
                while(1):
                    curs.execute("select id from nsacl where ns = ? and what = ? and id = ?", [ns, what, str(allid)])
                    if curs.fetchall():
                        allid += 1
                        continue
                    else:
                        break
                end = int(number_check(exp))

                time = datetime.datetime.now()
                plus = datetime.timedelta(seconds = end)
                r_time = (time + plus).strftime("%Y-%m-%d %H:%M:%S")
                if exp == '0':
                    r_time = '0'

                curs.execute("insert into nsacl (id, type, perm, how, exp, ns, what, id4) values (?, ?, ?, ?, ?, ?, ?, ?)", [str(allid), typ, permn, act, r_time, ns, what, str(allid).zfill(4)])

                tbodyData = ''
                curs.execute("select id, type, perm, how, exp from nsacl where ns = ? and what = ? order by cast(id as integer) asc", [ns, what])
                alt = curs.fetchall()
                if not(alt):
                    tbodyData = '''<tr class="ui-sortable-handle">
                            <td colSpan="5" style="text-align: center;">(규칙이 존재하지 않습니다. 모두 거부됩니다.)</td>
                            </tr>'''
                else:
                    ic = 1

                    for acldata in alt:
                        if acldata[3] == 'allow':
                            tt = '허용'
                        elif acldata[3] == 'deny':
                            tt = '거부'
                        else:
                            tt = '없음'
                        if acldata[1] == "comment" and acldata[2] == '-':
                            tbodyData += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td colspan=4><hr></td><td>'''
                        else:
                            tbodyData += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td>''' + str(ic) + '''</td>
                                        <td>''' + acldata[1] + ':' + acldata[2] + '''</td>
                                        <td>''' + tt + '''</td>
                                        <td>''' + generateTime(acldata[4], f = 1) + '''</td>
                                        <td>'''

                        if perm == 1:
                            tbodyData += '''<button type="submit" class="btn btn-danger btn-sm">삭제</button>'''

                        tbodyData += '''</td>
                                </tr>'''
                        ic += 1
                conn.commit()
                return tbodyData
        elif flask.request.form['mode'] == 'move':
            if flask.request.form['isNS'] != 'Y':
                id = flask.request.form['id']
                what = flask.request.form['type']
                after = flask.request.form['after_id']

                if int(id) > int(after):
                    if 3 == 12345678: #int(after) == 1:
                        for i in range(int(id), int(after), -1):
                            rndval = ''.join(random.choice("0123456789bcvzxsqrtyiplkjmn") for j in range(16))
                            curs.execute("update seedacl set id = ? where name = ? and what = ? and id = ?", [rndval, name, what, str(i - 1)])
                            curs.execute("update seedacl set id = ? where name = ? and what = ? and id = ?", [str(i - 1), name, what, str(i)])
                            curs.execute("update seedacl set id = ? where name = ? and what = ? and id = ?", [str(i), name, what, rndval])
                    else:
                        for i in range(int(id), int(after) + 1, -1):
                            rndval = ''.join(random.choice("0123456789bcvzxsqrtyiplkjmn") for j in range(16))
                            curs.execute("update seedacl set id = ? where name = ? and what = ? and id = ?", [rndval, name, what, str(i - 1)])
                            curs.execute("update seedacl set id = ? where name = ? and what = ? and id = ?", [str(i - 1), name, what, str(i)])
                            curs.execute("update seedacl set id = ? where name = ? and what = ? and id = ?", [str(i), name, what, rndval])
                else:
                    for i in range(int(id), int(after), 1):
                        rndval = ''.join(random.choice("0123456789bcvzxsqrtyiplkjmn") for j in range(16))
                        curs.execute("update seedacl set id = ? where name = ? and what = ? and id = ?", [rndval, name, what, str(i + 1)])
                        curs.execute("update seedacl set id = ? where name = ? and what = ? and id = ?", [str(i + 1), name, what, str(i)])
                        curs.execute("update seedacl set id = ? where name = ? and what = ? and id = ?", [str(i), name, what, rndval])


                tbodyData = ''
                curs.execute("select id, type, perm, how, exp from seedacl where name = ? and what = ? order by cast(id as integer) asc", [name, what])
                alt = curs.fetchall()
                if not(alt):
                    tbodyData = '''<tr class="ui-sortable-handle">
                            <td colSpan="5" style="text-align: center;">(규칙이 존재하지 않습니다. 이름공간 ACL이 적용됩니다.)</td>
                            </tr>'''
                else:
                    ic = 1

                    for acldata in alt:
                        if acldata[3] == 'allow':
                            tt = '허용'
                        elif acldata[3] == 'deny':
                            tt = '거부'
                        else:
                            tt = '없음'
                        if acldata[1] == "comment" and acldata[2] == '-':
                            tbodyData += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td colspan=4><hr></td><td>'''
                        else:
                            tbodyData += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td>''' + str(ic) + '''</td>
                                        <td>''' + acldata[1] + ':' + acldata[2] + '''</td>
                                        <td>''' + tt + '''</td>
                                        <td>''' + generateTime(acldata[4], f = 1) + '''</td>
                                        <td>'''

                        if perm == 1:
                            tbodyData += '''<button type="submit" class="btn btn-danger btn-sm">삭제</button>'''

                        tbodyData += '''</td>
                                </tr>'''
                        ic += 1
                conn.commit()
                return tbodyData
            elif flask.request.form['isNS'] == 'Y':
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'nsacl'])
                if not curs.fetchall():
                    return ''
                # return flask.jsonify( {"status": "지원하지 않는 기능입니다."} )
                id = flask.request.form['id']
                what = flask.request.form['type']
                after = flask.request.form['after_id']

                if int(id) > int(after):
                    if 3 == 12345678: #int(after) == 1:
                        for i in range(int(id), int(after), -1):
                            rndval = ''.join(random.choice("0123456789bcvzxsqrtyiplkjmn") for j in range(16))
                            curs.execute("update nsacl set id = ? where ns = ? and what = ? and id = ?", [rndval, ns, what, str(i - 1)])
                            curs.execute("update nsacl set id = ? where ns = ? and what = ? and id = ?", [str(i - 1), ns, what, str(i)])
                            curs.execute("update nsacl set id = ? where ns = ? and what = ? and id = ?", [str(i), ns, what, rndval])
                    else:
                        for i in range(int(id), int(after) + 1, -1):
                            rndval = ''.join(random.choice("0123456789bcvzxsqrtyiplkjmn") for j in range(16))
                            curs.execute("update nsacl set id = ? where ns = ? and what = ? and id = ?", [rndval, ns, what, str(i - 1)])
                            curs.execute("update nsacl set id = ? where ns = ? and what = ? and id = ?", [str(i - 1), ns, what, str(i)])
                            curs.execute("update nsacl set id = ? where ns = ? and what = ? and id = ?", [str(i), ns, what, rndval])
                else:
                    for i in range(int(id), int(after), 1):
                        rndval = ''.join(random.choice("0123456789bcvzxsqrtyiplkjmn") for j in range(16))
                        curs.execute("update nsacl set id = ? where ns = ? and what = ? and id = ?", [rndval, ns, what, str(i + 1)])
                        curs.execute("update nsacl set id = ? where ns = ? and what = ? and id = ?", [str(i + 1), ns, what, str(i)])
                        curs.execute("update nsacl set id = ? where ns = ? and what = ? and id = ?", [str(i), ns, what, rndval])


                tbodyData = ''
                curs.execute("select id, type, perm, how, exp from nsacl where ns = ? and what = ? order by cast(id as integer) asc", [ns, what])
                alt = curs.fetchall()
                if not(alt):
                    tbodyData = '''<tr class="ui-sortable-handle">
                            <td colSpan="5" style="text-align: center;">(규칙이 존재하지 않습니다. 모두 거부됩니다.)</td>
                            </tr>'''
                else:
                    ic = 1
                    for acldata in alt:
                        if acldata[3] == 'allow':
                            tt = '허용'
                        elif acldata[3] == 'deny':
                            tt = '거부'
                        else:
                            tt = '없음'
                        if acldata[1] == "comment" and acldata[2] == '-':
                            tbodyData += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td colspan=4><hr></td><td>'''
                        else:
                            tbodyData += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td>''' + str(ic) + '''</td>
                                        <td>''' + acldata[1] + ':' + acldata[2] + '''</td>
                                        <td>''' + tt + '''</td>
                                        <td>''' + generateTime(acldata[4], f = 1) + '''</td>
                                        <td>'''

                        if perm == 1:
                            tbodyData += '''<button type="submit" class="btn btn-danger btn-sm">삭제</button>'''

                        tbodyData += '''</td>
                                </tr>'''
                        ic += 1
                conn.commit()
                return tbodyData

        conn.commit()
        try:
            return tbodyData
        except:
            return '<tr class="ui-sortable-handle"><td colSpan="5" style="text-align: center;">(새로고침해 주세요.)</td></tr>'
    else:
        if nojs:
            data = '<h2 class="wiki-heading" style="border:none;cursor:pointer;">문서 ACL</h2><div>'
            #if re.search('^user:', name):
             #   acl_list = [['', 'normal'], ['user', 'member'], ['all', 'all']]
            #else:
            #acl_list = [['', '(없음)'], ['all', '모두'], ['user', '로그인된 사용자'], ['admin', '관리자'], ['50_edit', '50회 편집'], ['email', '인증자']]
            #if not re.search('^사용자:', name):
            #curs.execute("select dec from acl where title = ?", [name])
            #acl_data = curs.fetchall()

            dispType = ['읽기', '편집', '이동', '삭제', '토론 생성', '토론 댓글', '문서 댓글 읽기', '문서 댓글 쓰기', '편집요청', 'ACL']
            javaType = ['RED', 'EDT', 'MOV', 'DLT', 'CT', 'WTC', 'RDC', 'WDC', 'ERQ', 'ACL']
            seedType = ['read', 'edit', 'move', 'delete', 'create_thread', 'write_thread_comment', 'read_document_comment', 'write_document_comment', 'edit_request', 'acl']

            for i in range(0, len(dispType)):
                data += '<h4 class="wiki-heading" style="border:none;cursor:pointer;">' + dispType[i] + '</h4>'
                data += '''<div>
                            <table class="table" style="width:100%">
                            <colgroup>
                            <col style="width: 60px">
                            <col>
                            <col style="width: 80px">
                            <col style="width: 200px">
                            <col style="width: 60px;">
                            </colgroup>
                            <thead>
                            <tr style="border-top:1px solid #eceeef;border-bottom:2px solid #eceeef;">
                            <th>No</th>
                            <th>Condition</th>
                            <th>Action</th>
                            <th>Expiration</th>
                            <th></th>
                            </tr>
                            </thead>
                            <tbody class="seed-acl-tbody">
                            '''

                curs.execute("select id, type, perm, how, exp from seedacl where name = ? and what = ? order by id asc", [name, seedType[i]])
                alt = curs.fetchall()
                if not(alt):
                    data += '''<tr class="ui-sortable-handle">
                            <td colSpan="5" style="text-align: center;">(규칙이 존재하지 않습니다. 이름공간 ACL이 적용됩니다.)</td>
                            </tr>'''
                else:
                    ic = 1

                    for acldata in alt:
                        if acldata[3] == 'allow':
                            tt = '허용'
                        elif acldata[3] == 'deny':
                            tt = '거부'
                        else:
                            tt = '없음'
                        data += '''
                                    <tr style="; background-color: rgb(255, 255, 255);">
                                    <td>''' + str(ic) + '''</td>
                                    <td>''' + acldata[1] + ':' + acldata[2] + '''</td>
                                    <td>''' + tt + '''</td>
                                    <td>영구</td>
                                    <td style="width:125px">'''

                        if perm == 1:
                            data += '''<button type="button" class="btn btn-danger btn-sm" onclick="if(confirm('삭제하시겠습니까?'))location.href= '/aclman/del/''' + acldata[0] + '''/''' + seedType[i] + '''/''' + url_pas(name) + '''\';" style="font-weight:bolder;display:inline-block">-</button><button type="button" class="btn btn-secondary btn-sm" style="display: inline-block;" onclick="location.href='/aclup/''' + acldata[0] + '''/''' + seedType[i] + '''/''' + url_pas(name) + '''\';">▲</button><button type="button" class="btn btn-secondary btn-sm" style="display: inline-block;" onclick="location.href='/acldn/''' + acldata[0] + '''/''' + seedType[i] + '''/''' + url_pas(name) + '''\';">▼</button>'''

                        data += '''</td>
                                </tr>'''
                        ic += 1

                data += '''
                            </tbody>
                            </table>'''
                if perm == 1:
                    data += '''

                            <div class="form-inline">
                            <label class="control-label">Condition :</label>
                            <select class="seed-acl-add-condition-type form-control" id="permType''' + javaType[i] + '''" onclick="
                            document.getElementById('permType''' + javaType[i] + '''').onchange = function() {
                            	var val = document.getElementById('permType''' + javaType[i] + '''').value;
                            	if(val == 'perm') {
                            		document.getElementById('permText''' + javaType[i] + '''').style.display = 'inline-block';
                            		document.getElementById('memberText''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('ipText''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('geoipText''' + javaType[i] + '''').style.display = 'none';
                            	} else if(val == 'member') {
                            		document.getElementById('permText''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('memberText''' + javaType[i] + '''').style.display = 'inline-block';
                            		document.getElementById('ipText''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('geoipText''' + javaType[i] + '''').style.display = 'none';
                            	} else if(val == 'ip') {
                            		document.getElementById('permText''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('memberText''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('ipText''' + javaType[i] + '''').style.display = 'inline-block';
                            		document.getElementById('geoipText''' + javaType[i] + '''').style.display = 'none';
                            	} else if(val == 'geoip') {
                            		document.getElementById('permText''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('memberText''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('ipText''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('geoipText''' + javaType[i] + '''').style.display = 'inline-block';
                            	}

                            }">
                            <option value="perm">권한</option>
                            <option value="member">사용자</option>
                            <option value="ip">아이피</option>
                            <option value="geoip">GeoIP</option>
                            </select>
                            <select class="seed-acl-add-condition-value-perm form-control" name id="permText''' + javaType[i] + '''">
                            <option value="any">아무나</option>
                            <option value="member">로그인된 사용자 [*]</option>
                            <option value="admin">관리자</option>
                            <option value="member_signup_15days_ago">가입한지 15일 지난 사용자 [*]</option>
                            <option value="member_not_signup_15days_ago">가입한지 15일이 지나지 않은 사용자 [*]</option>
                            <option value="suspend_account">차단된 사용자</option>
                            <option value="blocked_ipacl">차단된 아이피</option>
                            <option value="document_creator">해당 문서를 만든 사용자 [*]</option>
                            <option value="document_last_contributed">해당 문서의 마지막 기여자 [*]</option>
                            <option value="document_contributor">해당 문서 기여자 [*]</option>
                            <option value="contributor">위키 기여자 [*]</option>
                            <option value="match_username_and_document_title">문서 제목과 사용자 이름이 일치</option>
                            <option value="match_ip_and_document_title">문서 제목과 아이피 주소가 일치</option>
                            <option value="email">이메일 인증된 사용자 [*]</option>
                            <option value="50_edit">기여 횟수가 50회 이상인 사용자 [*]</option>
                            <option value="ip">아이피 사용자</option>
                            <option value="developer">위키 소유자</option>
                            <option value="special">특수 사용자</option>
                            <option value="suspended_before">차단된 적이 있는 사용자</option>
                            <option value="document_starred">이 문서를 주시하는 사용자</option>
                            <option value="discussed_document">이 문서에서 토론한 적이 있는 사용자</option>
                            <option value="document_only_contributor">이 문서의 유일한 기여자</option>
                            <option value="discussed">토론한 적이 있는 사용자</option>


                            </select>
                            <input type="text" class="seed-acl-add-condition-value form-control" style="display: none; width:140px;" id="memberText''' + javaType[i] + '''">
                            <input type="text" class="seed-acl-add-condition-value form-control" style="display: none; width:140px;" id="ipText''' + javaType[i] + '''">
                            <input type="text" class="seed-acl-add-condition-value form-control" style="display: none; width:140px;" id="geoipText''' + javaType[i] + '''">
                            <label class="control-label">Action :</label>
                            <select class="seed-acl-add-action form-control" id="act''' + javaType[i] + '''">
                            <option value="allow">허용</option>
                            <option value="deny">거부</option>
                            </select>
                            <label class="control-label">Duration :</label>
                            <select class="form-control seed-acl-add-expire">
                            <option value="0" selected="">영구</option>
                            </select>
                            <button type="button" onclick="location.href= '/aclman/add/''' + seedType[i] + '''/' + document.getElementById('permType''' + javaType[i] + '''').value + '/' + document.getElementById(document.getElementById('permType''' + javaType[i] + '''').value + 'Text''' + javaType[i] + '''').value + '/' + document.getElementById('act''' + javaType[i] + '''').value + '/' + \'''' + url_pas(name) + '''\';" id="save">추가</button>
                            </div><small>[*] 차단된 사용자는 포함되지 않습니다.</small>'''
                data += '</div>'


            # ==================================================================================================
            # ==================================================================================================
            # ==================================================================================================
            # ==================================================================================================
            # ==================================================================================================
            # ==================================================================================================
            # ==================================================================================================

            curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'nsacl'])
            if curs.fetchall():
                perm = 1
            else:
                perm = 0
            data += '''</div><br><br><h2 class="wiki-heading" style="border:none;cursor:pointer;">이름공간 ACL</h2><div>'''

            for i in range(0, len(dispType)):
                data += '<h4 class="wiki-heading" style="border:none;cursor:pointer;">' + dispType[i] + '</h4><div>'
                data += '''<table class="table" style="width:100%">
                            <colgroup>
                            <col style="width: 60px">
                            <col>
                            <col style="width: 80px">
                            <col style="width: 200px">
                            <col style="width: 60px;">
                            </colgroup>
                            <thead>
                            <tr style="border-top:1px solid #eceeef;border-bottom:2px solid #eceeef;">
                            <th>No</th>
                            <th>Condition</th>
                            <th>Action</th>
                            <th>Expiration</th>
                            <th></th>
                            </tr>
                            </thead>
                            <tbody class="seed-acl-tbody">
                            '''

                curs.execute("select id, type, perm, how, exp from nsacl where ns = ? and what = ? order by id asc", [ns, seedType[i]])
                alt = curs.fetchall()
                if not(alt):
                    data += '''<tr class="ui-sortable-handle">
                            <td colSpan="5" style="text-align: center;">(규칙이 존재하지 않습니다. 모두 거부됩니다.)</td>
                            </tr>'''
                else:
                    ic = 1

                    for acldata in alt:
                        if acldata[3] == 'allow':
                            tt = '허용'
                        elif acldata[3] == 'deny':
                            tt = '거부'
                        else:
                            tt = '없음'
                        data += '''
                                    <tr style="; background-color: rgb(255, 255, 255);">
                                    <td>''' + str(ic) + '''</td>
                                    <td>''' + acldata[1] + ':' + acldata[2] + '''</td>
                                    <td>''' + tt + '''</td>
                                    <td>영구</td>
                                    <td style="width:125px">'''

                        if perm == 1:
                            data += '''<button type="button" class="btn btn-danger btn-sm" onclick="if(confirm('삭제하시겠습니까?'))location.href= '/nsacl/del/''' + acldata[0] + '''/''' + seedType[i] + '''/''' + url_pas(ns) + '''\';" style="font-weight:bolder;display:inline-block">-</button><button type="button" class="btn btn-secondary btn-sm" style="display: inline-block;" onclick="location.href='/nsup/''' + acldata[0] + '''/''' + seedType[i] + '''/''' + url_pas(ns) + '''\';">▲</button><button type="button" class="btn btn-secondary btn-sm" style="display: inline-block;" onclick="location.href='/nsdn/''' + acldata[0] + '''/''' + seedType[i] + '''/''' + url_pas(ns) + '''\';">▼</button>'''

                        data += '''</td>
                                </tr>'''
                        ic += 1

                data += '''
                            </tbody>
                            </table>'''
                if perm == 1:
                    data += '''

                            <div class="form-inline">
                            <label class="control-label">Condition :</label>
                            <select class="seed-acl-add-condition-type form-control" id="permTypeNS''' + javaType[i] + '''" onclick="
                            document.getElementById('permTypeNS''' + javaType[i] + '''').onchange = function() {
                            	var val = document.getElementById('permTypeNS''' + javaType[i] + '''').value;
                            	if(val == 'perm') {
                            		document.getElementById('permTextNS''' + javaType[i] + '''').style.display = 'inline-block';
                            		document.getElementById('memberTextNS''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('ipTextNS''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('geoipTextNS''' + javaType[i] + '''').style.display = 'none';
                            	} else if(val == 'member') {
                            		document.getElementById('permTextNS''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('memberTextNS''' + javaType[i] + '''').style.display = 'inline-block';
                            		document.getElementById('ipTextNS''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('geoipTextNS''' + javaType[i] + '''').style.display = 'none';
                            	} else if(val == 'ip') {
                            		document.getElementById('permTextNS''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('memberTextNS''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('ipTextNS''' + javaType[i] + '''').style.display = 'inline-block';
                            		document.getElementById('geoipTextNS''' + javaType[i] + '''').style.display = 'none';
                            	} else if(val == 'geoip') {
                            		document.getElementById('permTextNS''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('memberTextNS''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('ipTextNS''' + javaType[i] + '''').style.display = 'none';
                            		document.getElementById('geoipTextNS''' + javaType[i] + '''').style.display = 'inline-block';
                            	}

                            }">
                            <option value="perm">권한</option>
                            <option value="member">사용자</option>
                            <option value="ip">아이피</option>
                            <option value="geoip">GeoIP</option>
                            </select>
                            <select class="seed-acl-add-condition-value-perm form-control" name id="permTextNS''' + javaType[i] + '''">
                            <option value="any">아무나</option>
                            <option value="member">로그인된 사용자 [*]</option>
                            <option value="admin">관리자</option>
                            <option value="member_signup_15days_ago">가입한지 15일 지난 사용자 [*]</option>
                            <option value="member_not_signup_15days_ago">가입한지 15일이 지나지 않은 사용자 [*]</option>
                            <option value="suspend_account">차단된 사용자</option>
                            <option value="blocked_ipacl">차단된 아이피</option>
                            <option value="document_creator">해당 문서를 만든 사용자 [*]</option>
                            <option value="document_last_contributed">해당 문서의 마지막 기여자 [*]</option>
                            <option value="document_contributor">해당 문서 기여자 [*]</option>
                            <option value="contributor">위키 기여자 [*]</option>
                            <option value="match_username_and_document_title">문서 제목과 사용자 이름이 일치</option>
                            <option value="match_ip_and_document_title">문서 제목과 아이피 주소가 일치</option>
                            <option value="email">이메일 인증된 사용자 [*]</option>
                            <option value="50_edit">기여 횟수가 50회 이상인 사용자 [*]</option>
                            <option value="ip">아이피 사용자</option>
                            <option value="developer">위키 소유자</option>
                            <option value="special">특수 사용자</option>
                            <option value="suspended_before">차단된 적이 있는 사용자</option>
                            <option value="document_starred">이 문서를 주시하는 사용자</option>
                            <option value="discussed_document">이 문서에서 토론한 적이 있는 사용자</option>
                            <option value="document_only_contributor">이 문서의 유일한 기여자</option>
                            <option value="discussed">토론한 적이 있는 사용자</option>
                            </select>
                            <input type="text" class="seed-acl-add-condition-value form-control" style="display: none; width:140px;" id="memberTextNS''' + javaType[i] + '''">
                            <input type="text" class="seed-acl-add-condition-value form-control" style="display: none; width:140px;" id="ipTextNS''' + javaType[i] + '''">
                            <input type="text" class="seed-acl-add-condition-value form-control" style="display: none; width:140px;" id="geoipTextNS''' + javaType[i] + '''">
                            <label class="control-label">Action :</label>
                            <select class="seed-acl-add-action form-control" id="actNS''' + javaType[i] + '''">
                            <option value="allow">허용</option>
                            <option value="deny">거부</option>
                            </select>
                            <label class="control-label">Duration :</label>
                            <select class="form-control seed-acl-add-expire">
                            <option value="0" selected="">영구</option>
                            </select>
                            <button type="button" onclick="location.href= '/nsacl/add/''' + seedType[i] + '''/' + document.getElementById('permTypeNS''' + javaType[i] + '''').value + '/' + document.getElementById(document.getElementById('permTypeNS''' + javaType[i] + '''').value + 'TextNS''' + javaType[i] + '''').value + '/' + document.getElementById('actNS''' + javaType[i] + '''').value + '/' + \'''' + url_pas(ns) + '''\';" id="save">추가</button>
                            </div><small>[*] 차단된 사용자는 포함되지 않습니다.</small>'''
                data += '</div>'
            data += '</div>'
        else:
            isadmin = getacl(name, 'acl')
            if getperm('nsacl') == 1:
                isadmin = 1
            if isadmin != 1:
                dis = ' disabled'
            else:
                dis = ''
            if isadmin != 1:
                dea = 'false'
            else:
                dea = 'true'
            data = '<h2 class="wiki-heading" style="border:none;cursor:pointer;">문서 ACL</h2><div>'
            #if re.search('^user:', name):
             #   acl_list = [['', 'normal'], ['user', 'member'], ['all', 'all']]
            #else:
            #acl_list = [['', '(없음)'], ['all', '모두'], ['user', '로그인된 사용자'], ['admin', '관리자'], ['50_edit', '50회 편집'], ['email', '인증자']]
            #if not re.search('^사용자:', name):
            #curs.execute("select dec from acl where title = ?", [name])
            #acl_data = curs.fetchall()

            dispType = ['읽기', '편집', '이동', '삭제', '토론 생성', '토론 댓글', '편집요청', 'ACL']
            javaType = ['RED', 'EDT', 'MOV', 'DLT', 'CT', 'WTC', 'ERQ', 'ACL']
            seedType = ['read', 'edit', 'move', 'delete', 'create_thread', 'write_thread_comment', 'edit_request', 'acl']
            for i in range(0, len(dispType)):
                data += '<h4 class="wiki-heading" style="border:none;cursor:pointer;">' + dispType[i] + '</h4>'
                data += '''<div class="seed-acl-div" data-type="''' + seedType[i] + '''" data-editable="''' + dea + '''" data-isns="false">
                            <div class="table-wrap">
                            <table class="table">
                            <colgroup>
                            <col style="width: 60px">
                            <col>
                            <col style="width: 80px">
                            <col style="width: 200px">
                            <col style="width: 60px;">
                            </colgroup>
                            <thead>
                            <tr>
                            <th>No</th>
                            <th>Condition</th>
                            <th>Action</th>
                            <th>Expiration</th>
                            <th></th>
                            </tr>
                            </thead>
                            <tbody class="seed-acl-tbody ui-sortable">
                            '''

                curs.execute("select id, type, perm, how, exp from seedacl where name = ? and what = ? order by cast(id as integer) asc", [name, seedType[i]])
                alt = curs.fetchall()
                if not(alt):
                    data += '''<tr class="ui-sortable-handle">
                            <td colSpan="5" style="text-align: center;">(규칙이 존재하지 않습니다. 이름공간 ACL이 적용됩니다.)</td>
                            </tr>'''
                else:
                    ic = 1

                    for acldata in alt:
                        if acldata[3] == 'allow':
                            tt = '허용'
                        elif acldata[3] == 'deny':
                            tt = '거부'
                        else:
                            tt = '없음'
                        if acldata[1] == "comment" and acldata[2] == '-':
                            data += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td colspan=4><hr></td><td>'''
                        else:
                            data += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td>''' + str(ic) + '''</td>
                                        <td>''' + acldata[1] + ':' + acldata[2] + '''</td>
                                        <td>''' + tt + '''</td>
                                        <td>''' + generateTime(acldata[4], f = 1) + '''</td>
                                        <td>'''

                        if perm == 1:
                            data += '''<button type="submit" class="btn btn-danger btn-sm">삭제</button>'''

                        data += '''</td>
                                </tr>'''
                        ic += 1

                data += '''
                            </tbody>
                            </table>'''
                if perm == 1:
                    data += '''
                            <div class="form-inline">
            <div class="form-group">
            <label class="control-label">Condition :</label>
            <div>
            <select class="seed-acl-add-condition-type form-control" id=permType''' + javaType[i] + '''>
            <option value="perm">권한</option>
            <option value="member">사용자</option>
            <option value="ip">아이피</option>
            <option value="geoip">GeoIP</option>
            <option value="comment">주석</option>
            </select>
            <select class="seed-acl-add-condition-value-perm form-control" id="permText''' + javaType[i] + '''">
            <option value="any">아무나</option>
                            <option value="member">로그인된 사용자 [*]</option>
                            <option value="admin">관리자</option>
                            <option value="member_signup_15days_ago">가입한지 15일 지난 사용자 [*]</option>
                            <option value="member_not_signup_15days_ago">가입한지 15일이 지나지 않은 사용자 [*]</option>
                            <option value="suspend_account">차단된 사용자</option>
                            <option value="blocked_ipacl">차단된 아이피</option>
                            <option value="document_creator">해당 문서를 만든 사용자 [*]</option>
                            <option value="document_last_contributed">해당 문서의 마지막 기여자 [*]</option>
                            <option value="document_contributor">해당 문서 기여자 [*]</option>
                            <option value="contributor">위키 기여자 [*]</option>
                            <option value="match_username_and_document_title">문서 제목과 사용자 이름이 일치</option>
                            <option value="match_ip_and_document_title">문서 제목과 아이피 주소가 일치</option>
                            <option value="email">이메일 인증된 사용자 [*]</option>
                            <option value="50_edit">기여 횟수가 50회 이상인 사용자 [*]</option>
                            <option value="ip">아이피 사용자</option>
                            <option value="developer">위키 소유자</option>
                            <option value="special">특수 사용자</option>
                            <option value="suspended_before">차단된 적이 있는 사용자</option>
                            <option value="document_starred">이 문서를 주시하는 사용자</option>
                            <option value="discussed_document">이 문서에서 토론한 적이 있는 사용자</option>
                            <option value="document_only_contributor">이 문서의 유일한 기여자</option>
                            <option value="discussed">토론한 적이 있는 사용자</option>
            </select>
            <input type="text" class="seed-acl-add-condition-value form-control" style="display: none;">
            </div>
            </div>
            <div class="form-group">
            <label class="control-label">Action :</label>
            <div>
            <select class="seed-acl-add-action form-control"\>
            <option value="allow">허용</option>
            <option value="deny">거부</option>
            <option value="none">없음</option>
            </select>
            </div>
            </div>
            <div class="form-group">
            <label class="control-label">Duration :</label>
            <div>
            <select class="form-control seed-acl-add-expire">
            <option value="0" selected="">영구</option>
            <option value="300">5분</option>
            <option value="600">10분</option>
            <option value="1800">30분</option>
            <option value="3600">1시간</option>
            <option value="7200">2시간</option>
            <option value="86400">하루</option>
            <option value="259200">3일</option>
            <option value="432000">5일</option>
            <option value="604800">7일</option>
            <option value="1209600">2주</option>
            <option value="1814400">3주</option>
            <option value="2419200">4주</option>
            <option value="4838400">2개월</option>
            <option value="7257600">3개월</option>
            <option value="14515200">6개월</option>
            <option value="29030400">1년</option>
            </select>
            </div>
            </div>
            <button type=submit class="btn btn-primary seed-acl-add-btn">추가</button>
            </div>
            <small>[*] 차단된 사용자는 포함되지 않습니다.</small>
            </div></div>'''


            # ==================================================================================================
            # ==================================================================================================
            # ==================================================================================================
            # ==================================================================================================
            # ==================================================================================================
            # ==================================================================================================
            # ==================================================================================================
            isadmin = getperm('nsacl')
            if isadmin != 1:
                dis = ' disabled'
            else:
                dis = ''
            if isadmin != 1:
                dea = 'false'
            else:
                dea = 'true'

            curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'nsacl'])
            if curs.fetchall():
                perm = 1
            else:
                perm = 0
            data += '''</div><h2 class="wiki-heading" style="border:none;cursor:pointer;">이름공간 ACL</h2><div>'''

            for i in range(0, len(dispType)):
                data += '<h4 class="wiki-heading" style="border:none;cursor:pointer;">' + dispType[i] + '</h4>'

                data += '''<div class="seed-acl-div" data-type="''' + seedType[i] + '''" data-editable="''' + dea + '''" data-isns="true">
                    <table class="table">
                            <colgroup>
                            <col style="width: 60px">
                            <col>
                            <col style="width: 80px">
                            <col style="width: 200px">
                            <col style="width: 60px;">
                            </colgroup>
                            <thead>
                            <tr style="border-top:1px solid #eceeef;border-bottom:2px solid #eceeef;">
                            <th>No</th>
                            <th>Condition</th>
                            <th>Action</th>
                            <th>Expiration</th>
                            <th></th>
                            </tr>
                            </thead>
                            <tbody class="seed-acl-tbody ui-sortable">
                            '''

                curs.execute("select id, type, perm, how, exp from nsacl where ns = ? and what = ? order by cast(id as integer) asc", [ns, seedType[i]])
                alt = curs.fetchall()
                if not(alt):
                    data += '''<tr class="ui-sortable-handle">
                            <td colSpan="5" style="text-align: center;">(규칙이 존재하지 않습니다. 모두 거부됩니다.)</td>
                            </tr>'''
                else:
                    ic = 1

                    for acldata in alt:
                        if acldata[3] == 'allow':
                            tt = '허용'
                        elif acldata[3] == 'deny':
                            tt = '거부'
                        else:
                            tt = '없음'
                        if acldata[1] == "comment" and acldata[2] == '-':
                            data += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td colspan=4><hr></td><td>'''
                        else:
                            data += '''
                                        <tr style="background-color: rgb(255, 255, 255);" class="ui-sortable-handle" data-id="''' + acldata[0] + '''">
                                        <td>''' + str(ic) + '''</td>
                                        <td>''' + acldata[1] + ':' + acldata[2] + '''</td>
                                        <td>''' + tt + '''</td>
                                        <td>''' + generateTime(acldata[4], f = 1) + '''</td>
                                        <td>'''

                        if perm == 1:
                            data += '''<button type="submit" class="btn btn-danger btn-sm">삭제</button>'''

                        data += '''</td>
                                </tr>'''
                        ic += 1

                data += '''
                            </tbody>
                            </table>'''
                if perm == 1:
                    data += '''

                            <div class="form-inline">
            <div class="form-group">
            <label class="control-label">Condition :</label>
            <div>
            <select class="seed-acl-add-condition-type form-control" id=permType''' + javaType[i] + '''>
            <option value="perm">권한</option>
            <option value="member">사용자</option>
            <option value="ip">아이피</option>
            <option value="geoip">GeoIP</option>
            <option value="comment">주석</option>
            </select>
            <select class="seed-acl-add-condition-value-perm form-control" id="permText''' + javaType[i] + '''">
            <option value="any">아무나</option>
                            <option value="member">로그인된 사용자 [*]</option>
                            <option value="admin">관리자</option>
                            <option value="member_signup_15days_ago">가입한지 15일 지난 사용자 [*]</option>
                            <option value="member_not_signup_15days_ago">가입한지 15일이 지나지 않은 사용자 [*]</option>
                            <option value="suspend_account">차단된 사용자</option>
                            <option value="blocked_ipacl">차단된 아이피</option>
                            <option value="document_creator">해당 문서를 만든 사용자 [*]</option>
                            <option value="document_last_contributed">해당 문서의 마지막 기여자 [*]</option>
                            <option value="document_contributor">해당 문서 기여자 [*]</option>
                            <option value="contributor">위키 기여자 [*]</option>
                            <option value="match_username_and_document_title">문서 제목과 사용자 이름이 일치</option>
                            <option value="match_ip_and_document_title">문서 제목과 아이피 주소가 일치</option>
                            <option value="email">이메일 인증된 사용자 [*]</option>
                            <option value="50_edit">기여 횟수가 50회 이상인 사용자 [*]</option>
                            <option value="ip">아이피 사용자</option>
                            <option value="developer">위키 소유자</option>
                            <option value="special">특수 사용자</option>
                            <option value="suspended_before">차단된 적이 있는 사용자</option>
                            <option value="document_starred">이 문서를 주시하는 사용자</option>
                            <option value="discussed_document">이 문서에서 토론한 적이 있는 사용자</option>
                            <option value="document_only_contributor">이 문서의 유일한 기여자</option>
                            <option value="discussed">토론한 적이 있는 사용자</option>
            </select>
            <input type="text" class="seed-acl-add-condition-value form-control" style="display: none;">
            </div>
            </div>
            <div class="form-group">
            <label class="control-label">Action :</label>
            <div>
            <select class="seed-acl-add-action form-control"\>
            <option value="allow">허용</option>
            <option value="deny">거부</option>
            <option value="none">없음</option>
            </select>
            </div>
            </div>
            <div class="form-group">
            <label class="control-label">Duration :</label>
            <div>
            <select class="form-control seed-acl-add-expire">
            <option value="0" selected="">영구</option>
            <option value="300">5분</option>
            <option value="600">10분</option>
            <option value="1800">30분</option>
            <option value="3600">1시간</option>
            <option value="7200">2시간</option>
            <option value="86400">하루</option>
            <option value="259200">3일</option>
            <option value="432000">5일</option>
            <option value="604800">7일</option>
            <option value="1209600">2주</option>
            <option value="1814400">3주</option>
            <option value="2419200">4주</option>
            <option value="4838400">2개월</option>
            <option value="7257600">3개월</option>
            <option value="14515200">6개월</option>
            <option value="29030400">1년</option>
            </select>
            </div>
            </div>
            <button type=submit class="btn btn-primary seed-acl-add-btn">추가</button>
            </div>
            <small>[*] 차단된 사용자는 포함되지 않습니다.</small>
            </div>'''
            data += '</div>'



        data += '''

        '''#'''    <h4 class="wiki-heading" style="border:none">''' + load_lang('explanation') + '''</h4>
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
            data += ''

        return easy_minify(flask.render_template(skin_check(),
            imp = [name, wiki_set(), custom(), other2([' (' + load_lang('acl') + ')', 0])],
            data = data,
            menu = [['w/' + url_pas(name), load_lang('document')], ['manager', load_lang('admin')]],
            st = 8
        ))

def acladd_2(conn, what, typ, permn, name, act):
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
    perm = getacl(name, 'acl')
    curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'nsacl'])
    if curs.fetchall():
        perm = 1
    if perm == 0:
        return re_error('/error/3')

    allid = 1
    while(1):
        curs.execute("select id from seedacl where name = ? and what = ? and id = ?", [name, what, str(allid)])
        if curs.fetchall():
            allid += 1
            continue
        else:
            break

    history_plus(
            name,
            '',
            get_time(),
            ip_check(),
            '',
            '0',
            'insert,' + what + ',' + act + ',' + typ + ':' + permn + '으로 ACL 변경'
        )

    #curs.execute("select id, type, perm, how, exp from seedacl where name = ? and what = 'wtc' order by id4 asc", [name])
    curs.execute("insert into seedacl (id, type, perm, how, exp, name, what, id4) values (?, ?, ?, ?, ?, ?, ?, ?)", [str(allid), typ, permn, act, '0', name, what, str(allid).zfill(4)])

    return redirect('/acl/' + name)

def acldel_2(conn, id, name, what):
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
    perm = getacl(name, 'acl')
    curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'nsacl'])
    if curs.fetchall():
        perm = 1
    if perm == 0:
        return re_error('/error/3')

    curs.execute("select id, type, perm, how, exp, what from seedacl where name = ? and id = ? and what = ? order by id asc", [name, id, what])
    dat = curs.fetchall()
    if dat:
        history_plus(
                name,
                '',
                get_time(),
                ip_check(),
                '',
                '0',
                'delete,' + dat[0][5] + ',' + dat[0][3] + ',' + dat[0][1] + ':' + dat[0][2] + '으로 ACL 변경'
            )

        #curs.execute("select id, type, perm, how, exp from seedacl where name = ? and what = 'wtc' order by id4 asc", [name])
        curs.execute("delete from seedacl where name = ? and id = ? and what = ?", [name, id, what])

    return redirect('/acl/' + name)

def nsadd_2(conn, what, typ, permn, name, act):
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
    elif re.search('^토론:', name):
        ns = '토론'
    elif re.search('^' + wiki_set()[0] + ':', name):
        ns = wiki_set()[0]
    else:
        ns = '문서'
    curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'nsacl'])
    if curs.fetchall():
        perm = 1
    else:
        perm = 0
    if perm == 0:
        return re_error('/error/3')

    allid = 1
    while(1):
        curs.execute("select id from nsacl where ns = ? and what = ? and id = ?", [name, what, str(allid)])
        if curs.fetchall():
            allid += 1
            continue
        else:
            break


    #curs.execute("select id, type, perm, how, exp from seedacl where name = ? and what = 'wtc' order by id4 asc", [name])
    curs.execute("insert into nsacl (id, type, perm, how, exp, ns, what, id4) values (?, ?, ?, ?, ?, ?, ?, ?)", [str(allid), typ, permn, act, '0', name, what, str(allid).zfill(4)])

    return redirect('/acl/' + name + ':-')

def nsdel_2(conn, id, name, what):
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
    elif re.search('^토론:', name):
        ns = '토론'
    elif re.search('^' + wiki_set()[0] + ':', name):
        ns = wiki_set()[0]
    else:
        ns = '문서'

    curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'nsacl'])
    if curs.fetchall():
        perm = 1
    else:
        perm = 0
    if perm == 0:
        return re_error('/error/3')



    #curs.execute("select id, type, perm, how, exp from seedacl where name = ? and what = 'wtc' order by id4 asc", [name])
    curs.execute("delete from nsacl where ns = ? and id = ? and what = ?", [name, id, what])

    return redirect('/acl/' + name + ':-')

def aclup_2(conn, id, name, what):
    if id == '1':
        return redirect('/acl/' + name)
    curs = conn.cursor()
    rndval = ''.join(random.choice("0123456789bcvzxsqrtyiplkjmn") for i in range(16))
    curs.execute("update seedacl set id = ?, id4 = ? where name = ? and what = ? and id = ?", [rndval, rndval, name, what, str(int(id) - 1)])
    curs.execute("update seedacl set id = ?, id4 = ? where name = ? and what = ? and id = ?", [str(int(id) - 1), str(int(id) - 1).zfill(4), name, what, id])
    curs.execute("update seedacl set id = ?, id4 = ? where name = ? and what = ? and id = ?", [id, id.zfill(4), name, what, rndval])

    return redirect('/acl/' + name)

def acldn_2(conn, id, name, what):
    curs = conn.cursor()
    curs.execute("select id from seedacl where name = ? and what = ? order by id desc limit 1", [name, what])
    idData = curs.fetchall()

    if not idData or (idData and idData[0][0] == id):
        return redirect('/acl/' + name)
    curs = conn.cursor()
    rndval = ''.join(random.choice("0123456789bcvzxsqrtyiplkjmn") for i in range(16))
    curs.execute("update seedacl set id = ?, id4 = ? where name = ? and what = ? and id = ?", [rndval, rndval, name, what, str(int(id) + 1)])
    curs.execute("update seedacl set id = ?, id4 = ? where name = ? and what = ? and id = ?", [str(int(id) + 1), str(int(id) - 1).zfill(4), name, what, id])
    curs.execute("update seedacl set id = ?, id4 = ? where name = ? and what = ? and id = ?", [id, id.zfill(4), name, what, rndval])

    return redirect('/acl/' + name)

def nsup_2(conn, id, name, what):
    if id == '1':
        return redirect('/acl/' + name + ':-')
    curs = conn.cursor()
    rndval = ''.join(random.choice("0123456789bcvzxsqrtyiplkjmn") for i in range(16))
    curs.execute("update nsacl set id = ?, id4 = ? where ns = ? and what = ? and id = ?", [rndval, rndval, name, what, str(int(id) - 1)])
    curs.execute("update nsacl set id = ?, id4 = ? where ns = ? and what = ? and id = ?", [str(int(id) - 1), str(int(id) - 1).zfill(4), name, what, id])
    curs.execute("update nsacl set id = ?, id4 = ? where ns = ? and what = ? and id = ?", [id, id.zfill(4), name, what, rndval])

    return redirect('/acl/' + name + ':-')

def nsdn_2(conn, id, name, what):
    curs = conn.cursor()
    curs.execute("select id from nsacl where ns = ? and what = ? order by id4 desc limit 1", [name, what])
    idData = curs.fetchall()

    if not idData or (idData and idData[0][0] == id):
        return redirect('/acl/' + name + ':-')
    curs = conn.cursor()
    rndval = ''.join(random.choice("0123456789bcvzxsqrtyiplkjmn") for i in range(16))
    curs.execute("update nsacl set id = ?, id4 = ? where ns = ? and what = ? and id = ?", [rndval, rndval, name, what, str(int(id) + 1)])
    curs.execute("update nsacl set id = ?, id4 = ? where ns = ? and what = ? and id = ?", [str(int(id) + 1), str(int(id) - 1).zfill(4), name, what, id])
    curs.execute("update nsacl set id = ?, id4 = ? where ns = ? and what = ? and id = ?", [id, id.zfill(4), name, what, rndval])

    return redirect('/acl/' + name + ':-')