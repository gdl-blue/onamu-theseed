from .tool.func import *

def star_2(conn, name):
    curs = conn.cursor()

    if islogin() != 1:
        return redirect('/member/login?redirect=' + url_pas("/member/star/" + name))

    curs.execute("select title from data where title = ?", [name])
    if not(curs.fetchall()):
        return re_error('/error/8000')

    curs.execute("select doc from star where user = ? and doc = ?", [ip_check(), name])
    if curs.fetchall():
        return re_error('/error/1000')

    curs.execute("insert into star (user, doc) values (?, ?)", [ip_check(), name])

    return redirect('/w/' + url_pas(name))

def unstar_2(conn, name):
    curs = conn.cursor()

    if islogin() != 1:
        return redirect('/member/login?redirect=' + url_pas("/member/star/" + name))

    curs.execute("select title from data where title = ?", [name])
    if not(curs.fetchall()):
        return re_error('/error/8000')

    curs.execute("select doc from star where user = ? and doc = ?", [ip_check(), name])
    if not(curs.fetchall()):
        return re_error('/error/1001')

    curs.execute("delete from star where doc = ? and user = ?", [name, ip_check()])
    conn.commit()

    return redirect('/w/' + url_pas(name))

def stardoc_2(conn):
    curs = conn.cursor()

    if islogin() != 1:
        return redirect('/member/login?redirect=' + url_pas("/member/star/" + name))

    curs.execute("select doc, user from star order by lstedt desc")
    lst = curs.fetchall()
    div = '<ul>'
    sub = 0
    if lst:
        for dc in lst:
            if dc[1] == ip_check():
                curs.execute("select date from data where title = ?", [dc[0]])
                edt = '알 수 없음'
                edtf = curs.fetchall()
                if edtf:
                    if edtf[0][0] == '':
                        edt = '알 수 없음'
                    else:
                        edt = edtf[0][0]
                else:
                    edt = '알 수 없음'

                div += '<li><a href="/w/' + url_pas(dc[0]) + '">' + dc[0] + '</a> (수정 시각:' + edt + ')</li>'

    div += '</ul>'

    return easy_minify(flask.render_template(skin_check(),
            imp = ['내 문서함', wiki_set(), custom(), other2([sub, 0])],
            data = div,
            menu = 0
        ))