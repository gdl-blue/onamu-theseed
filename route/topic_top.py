from .tool.func import *

def topic_top_2(conn, tnum, num):
    curs = conn.cursor()
    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')

    if getperm('htc') != 1:
        return re_error('/error/3')

    curs.execute("select title from topic where tnum = ? and id = ?", [tnum, str(num)])
    if curs.fetchall():
        curs.execute("select top from topic where id = ? and tnum = ?", [str(num),tnum])
        top_data = curs.fetchall()
        if top_data:
            if top_data[0][0] == '1':
                return showError('해당 댓글을 고정할 수 없습니다.')

            if top_data[0][0] == 'O':
                curs.execute("update topic set top = '' where tnum = ? and id = ?", [tnum, str(num)])
            else:
                curs.execute("update topic set top = 'O' where tnum = ? and id = ?", [tnum, str(num)])

        #rd_plus(name, sub, get_time(), tnum)

        conn.commit()

    return redirect('/thread/' + url_pas(tnum))
