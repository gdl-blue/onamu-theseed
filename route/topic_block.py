from .tool.func import *
# 'blind (' + name + ' - ' + sub + '#' + str(num) + ')'

def topic_block_2(conn, tnum, num, typ):
    curs = conn.cursor()
    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')

    curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'htc'])
    if not(curs.fetchall()):
        return re_error('/error/3')

    curs.execute("select block from topic where tnum = ? and id = ?", [tnum, str(num)])
    block = curs.fetchall()
    if block:
        if typ == 'x':
            if block[0][0] == 'O':
                curs.execute("update topic set block = '' where tnum = ? and id = ?", [tnum, str(num)])
            else:
                curs.execute("update topic set block = 'O' where tnum = ? and id = ?", [tnum, str(num)])
                curs.execute("insert into re_admin (who, what, time) values (?, ?, ?)", [ip_check(), 'blind (' + name + ' - ' + sub + '#' + str(num) + ')', get_time()])
        else:
            if typ == 'show':
                if block[0][0] == 'O':
                    curs.execute("update topic set block = '' where tnum = ? and id = ?", [tnum, str(num)])
                else:
                    return showError("요청이 틀립니다.")
            else:
                if block[0][0] != 'O':
                    curs.execute("update topic set block = 'O' where tnum = ? and id = ?", [tnum, str(num)])
                    curs.execute("insert into re_admin (who, what, time) values (?, ?, ?)", [ip_check(), 'blind (' + name + ' - ' + sub + '#' + str(num) + ')', get_time()])
                else:
                    return showError("요청이 틀립니다.")
        #rd_plus(name, sub, get_time())

        conn.commit()

    return redirect('/thread/' + url_pas(tnum) + '#' + str(num))