from .tool.func import *

def topic_ren_2(conn, tnum, new):
    curs = conn.cursor()
    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')

    curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'utt'])
    if not(curs.fetchall()):
        return re_error('/error/3')

    curs.execute("select id from topic where tnum = ? order by id + 0 desc limit 1", [tnum])
    old_num = curs.fetchall()
    if old_num:
        num = int(old_num[0][0]) + 1
    else:
        num = 1

    curs.execute("update topic set sub = ? where tnum = ?", [new, tnum])
    curs.execute("update rd set sub = ? where tnum = ?", [new, tnum])
    for i in range(1, int(num)):
        curs.execute("update re_admin set what = ? where what = ?", ['blind (' + name + ' - ' + new + '#' + str(i) + ')', 'blind (' + name + ' - ' + sub + '#' + str(i) + ')'])
    if admin_check(5) == 1 or getperm('tribune') == 1 or getperm('arbiter') == 1:
        adm = 1
    else:
        adm = 0
    curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm, tnum) values (?, ?, ?, ?, ?, ?, '', '1', ?, ?)", [str(num), name, new, '스레드 주제를 \'\'\'' + sub + '\'\'\'에서 \'\'\'' + new + '\'\'\'으로 변경', get_time(), ip_check(), adm, tnum])
    conn.commit()

    rd_plus(name, sub, get_time(), tnum)

    return redirect('/thread/' + url_pas(tnum) + '#reload')

def topic_move_2(conn, tnum, title):
    curs = conn.cursor()
    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')

    if getacl(name, 'read') == 0:
        return showError('읽기 권한이 부족하므로 토론을 다른 문서로 이동할 수 없습니다.')

    curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'utd'])
    if not(curs.fetchall()):
        return re_error('/error/3')

    curs.execute("select id from topic where tnum = ? order by id + 0 desc limit 1", [tnum])
    old_num = curs.fetchall()
    if old_num:
        num = int(old_num[0][0]) + 1
    else:
        num = 1

    curs.execute("update topic set title = ? where tnum = ?", [title, tnum])
    curs.execute("update rd set title = ? where tnum = ?", [title, tnum])
    for i in range(1, int(num)):
        curs.execute("update re_admin set what = ? where what = ?", ['blind (' + title + ' - ' + sub + '#' + str(i) + ')', 'blind (' + name + ' - ' + sub + '#' + str(i) + ')'])
    if admin_check(5) == 1 or getperm('tribune') == 1 or getperm('arbiter') == 1:
        adm = 1
    else:
        adm = 0
    curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm, tnum) values (?, ?, ?, ?, ?, ?, '', '1', ?, ?)", [str(num), title, sub, '스레드를 \'\'\'' + name + '\'\'\'에서 \'\'\'' + title + '\'\'\' 문서로 이동', get_time(), ip_check(), adm, tnum])
    conn.commit()

    rd_plus(name, sub, get_time(), tnum)

    return redirect('/thread/' + url_pas(tnum) + '#reload')