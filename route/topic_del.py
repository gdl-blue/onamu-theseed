from .tool.func import *

def topic_del_2(conn, tnum):
    curs = conn.cursor()
    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')

    curs.execute("select stop from rd where tnum = ? and removed = '1'", [tnum])
    if curs.fetchall():
        return showError("삭제된 토론입니다.")

    curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'dt'])
    if not(curs.fetchall()):
        return re_error('/error/3')

    curs.execute("update rd set removed = '1' where tnum = ?", [tnum])

    curs.execute("update rd set sub = ? where tnum = ?", [sub + ' (삭제됨)', tnum])
    curs.execute("update topic set sub = ? where tnum = ?", [sub + ' (삭제됨)', tnum])

    conn.commit()

    return redirect('/discuss/' + url_pas(name))

def topic_rdel_2(conn, tnum):
    curs = conn.cursor()
    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')

    curs.execute("select stop from rd where tnum = ? and removed = '0'", [tnum])
    if curs.fetchall():
        return showError("삭제되지 않은 토론입니다.")

    if admin_check() != 1:
        return re_error('/error/3')

    curs.execute("update rd set removed = '0' where tnum = ?", [tnum])

    curs.execute("update rd set sub = ? where tnum = ?", [re.sub('\s[(]삭제됨[)]$', '', sub), tnum])
    curs.execute("update topic set sub = ? where tnum = ?", [re.sub('\s[(]삭제됨[)]$', '', sub), tnum])

    conn.commit()

    return redirect('/discuss/' + url_pas(name))

def topic_pdel_2(conn, tnum):
    curs = conn.cursor()
    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')

    if admin_check() != 1:
        return re_error('/error/3')

    curs.execute("delete from topic where tnum = ?", [tnum])
    curs.execute("delete from rd where tnum = ?", [tnum])

    conn.commit()

    return redirect('/discuss/' + url_pas(name))
