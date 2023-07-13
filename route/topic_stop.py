from .tool.func import *

def topic_stop_2(conn, tnum, tool):
    curs = conn.cursor()
    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')

    curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'uts'])
    if not(curs.fetchall()):
        return re_error('/error/3')

    if tool == 'pause':
        curs.execute("select stop from rd where tnum = ?", [tnum])
        cl = curs.fetchall()
        if cl and cl[0][0] == 'O':
            curs.execute("update rd set stop = '' where tnum = ?", [tnum])

        curs.execute("select id from topic where tnum = ? order by id + 0 desc limit 1", [tnum])
        topic_check_2 = curs.fetchall()
        topic_check = [['']]
        if topic_check_2:
            topic_check = topic_check_2
        curs.execute("select pause from rd where tnum = ?", [tnum])
        ifpause_arr = curs.fetchall()
        ifpause = ''
        if ifpause_arr:
            ifpause = ifpause_arr[0][0]
        if admin_check(5) == 1 or getperm('tribune') == 1 or getperm('arbiter') == 1:
            adm = 1
        else:
            adm = 0
        if ifpause == 'O':
            curs.execute("update rd set pause = '' where tnum = ?", [tnum])
            curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm, tnum) values (?, ?, ?, ?, ?, ?, '', '1', ?, ?)", [str(int(topic_check[0][0]) + 1), name, sub, '스레드 상태를 \'\'\'normal\'\'\'로 변경', get_time(), ip_check(), adm, tnum])
        else:
            curs.execute("update rd set pause = 'O' where tnum = ?", [tnum])
            curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm, tnum) values (?, ?, ?, ?, ?, ?, '', '1', ?, ?)", [str(int(topic_check[0][0]) + 1), name, sub, '스레드 상태를 \'\'\'pause\'\'\'로 변경', get_time(), ip_check(), adm, tnum])
        conn.commit()
        return redirect('/thread/' + url_pas(tnum) + '#reload')
    if admin_check(5) == 1 or getperm('tribune') == 1 or getperm('arbiter') == 1:
        adm = 1
    else:
        adm = 0
    ip = ip_check()
    time = get_time()
    curs.execute("select id from topic where tnum = ? order by id + 0 desc limit 1", [tnum])
    topic_check = curs.fetchall()
    if topic_check:
        if tool == 'agree':
            curs.execute("select title from rd where tnum = ? and agree = 'O'", [tnum])
            if curs.fetchall():
                curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm, tnum) values (?, ?, ?, ?, ?, ?, '', '1', ?, ?)", [str(int(topic_check[0][0]) + 1), name, sub, '스레드 상태를 \'\'\'continue\'\'\'로 변경', time, ip, adm, tnum])
                curs.execute("update rd set agree = '' where tnum = ?", [tnum])
            else:
                curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm, tnum) values (?, ?, ?, ?, ?, ?, '', '1', ?, ?)", [str(int(topic_check[0][0]) + 1), name, sub, '스레드 상태를 \'\'\'agree\'\'\'로 변경', time, ip, adm, tnum])
                curs.execute("update rd set agree = 'O' where tnum = ?", [tnum])
        else:
            if tool == 'close':
                curs.execute("update rd set pause = '' where tnum = ?", [tnum])
                why = flask.request.form.get('why', '')
                set_list = [
                    'O',
                    'S',
                    '스레드 상태를 \'\'\'close\'\'\'로 변경' + (('[br][br]' + why) if why else ''),
                    '스레드 상태를 \'\'\'normal\'\'\'로 변경' + (('[br][br]' + why) if why else '')
                ]
            elif tool == 'stop':
                set_list = ['', 'O', '스레드 상태를 \'\'\'stop\'\'\'로 변경', '스레드 상태를 \'\'\'restart\'\'\'로 변경']
            else:
                return redirect('/thread/' + url_pas(tnum) + '#reload')

            curs.execute("select title from rd where tnum = ? and stop = ?", [tnum, set_list[0]])
            if curs.fetchall():
                curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm, tnum) values (?, ?, ?, ?, ?, ?, '', '1', ?, ?)", [str(int(topic_check[0][0]) + 1), name, sub, set_list[3], time, ip, adm, tnum])
                curs.execute("update rd set stop = '' where tnum = ?", [tnum])
            else:
                curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm, tnum) values (?, ?, ?, ?, ?, ?, '', '1', ?, ?)", [str(int(topic_check[0][0]) + 1), name, sub, set_list[2], time, ip, adm, tnum])
                curs.execute("update rd set stop = ? where tnum = ?", [set_list[0], tnum])

        rd_plus(name, sub, time, tnum)

        conn.commit()

    return redirect('/thread/' + url_pas(tnum) + '#reload')

def threadTools(conn, tnum, toolname):
    curs = conn.cursor()

    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')
    curs.execute("select id from topic where tnum = ? order by id + 0 desc limit 1", [tnum])
    topic_check = curs.fetchall()
    if not(topic_check):
        topic_check = [['0']]
    if toolname == 'status':
        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'uts'])
        if not(curs.fetchall()):
            return flask.jsonify({ "status": '권한이 부족합니다.' }), 403
        #아니 파이썬에는 SELECTCASE문이 없어 C는 물론 폿트란에도 있는데
        if getForm('status') == 'normal':
            curs.execute("update rd set agree = '', stop = '', pause = '' where tnum = ?", [tnum])
        elif getForm('status') == 'close':
            curs.execute("update rd set agree = '', stop = 'O', pause = '' where tnum = ?", [tnum])
        elif getForm('status') == 'pause':
            curs.execute("update rd set agree = '', stop = '', pause = 'O' where tnum = ?", [tnum])
        elif getForm('status') == 'agree':
            curs.execute("update rd set agree = 'O', stop = '', pause = '' where tnum = ?", [tnum])

        curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm, tnum) values (?, ?, ?, ?, ?, ?, '', '1', ?, ?)", [str(int(topic_check[0][0]) + 1), name, sub, '스레드 상태를 \'\'\'' + getForm('status', '') + '\'\'\'로 변경', get_time(), ip_check(), admin_check(5), tnum])
    elif toolname == 'document':
        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'utd'])
        if not(curs.fetchall()):
            return flask.jsonify({ "status": '권한이 부족합니다.' }), 403
        if getacl(name, 'read') == 0:
            return flask.jsonify({ "status": '읽기 권한이 부족하므로 토론을 다른 문서로 이동할 수 없습니다.' }), 403
        curs.execute("select id from topic where tnum = ? order by id + 0 desc limit 1", [tnum])
        old_num = curs.fetchall()
        if old_num:
            num = int(old_num[0][0]) + 1
        else:
            num = 1

        curs.execute("update topic set title = ? where tnum = ?", [getForm('document', ''), tnum])
        curs.execute("update rd set title = ? where tnum = ?", [getForm('document', ''), tnum])
        for i in range(1, int(num)):
            curs.execute("update re_admin set what = ? where what = ?", ['blind (' + getForm('document', '') + ' - ' + sub + '#' + str(i) + ')', 'blind (' + name + ' - ' + sub + '#' + str(i) + ')'])
        if admin_check(5) == 1 or getperm('tribune') == 1 or getperm('arbiter') == 1:
            adm = 1
        else:
            adm = 0
        curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm, tnum) values (?, ?, ?, ?, ?, ?, '', '1', ?, ?)", [str(num), getForm('document', ''), sub, '스레드를 \'\'\'' + getForm('document', '') + '\'\'\' 문서로 이동', get_time(), ip_check(), adm, tnum])
    elif toolname == 'topic':
        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'utt'])
        if not(curs.fetchall()):
            return flask.jsonify({ "status": '권한이 부족합니다.' }), 403

        curs.execute("select id from topic where tnum = ? order by id + 0 desc limit 1", [tnum])
        old_num = curs.fetchall()
        if old_num:
            num = int(old_num[0][0]) + 1
        else:
            num = 1

        curs.execute("update topic set sub = ? where tnum = ?", [getForm('topic', ''), tnum])
        curs.execute("update rd set sub = ? where tnum = ?", [getForm('topic', ''), tnum])
        for i in range(1, int(num)):
            curs.execute("update re_admin set what = ? where what = ?", ['blind (' + name + ' - ' + getForm('topic', '') + '#' + str(i) + ')', 'blind (' + name + ' - ' + sub + '#' + str(i) + ')'])
        if admin_check(5) == 1 or getperm('tribune') == 1 or getperm('arbiter') == 1:
            adm = 1
        else:
            adm = 0
        curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm, tnum) values (?, ?, ?, ?, ?, ?, '', '1', ?, ?)", [str(num), name, getForm('topic', ''), '스레드 주제를 \'\'\'' + getForm('topic', '') + '\'\'\'로 변경', get_time(), ip_check(), adm, tnum])

    rd_plus(name, sub, get_time(), tnum)
    conn.commit()

    if flask.request.args.get("nojs", None) == '1':
        return redirect('/thread/' + tnum)
    else:
        return flask.jsonify({})