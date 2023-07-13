from .tool.func import *

def main_skin_set_2(conn):
    curs = conn.cursor()
    try:
        open('./views/' + skin_check(1) + '/settings.html', 'r').read()
    except:
        return easy_minify(flask.render_template(skin_check(),
                    imp = ['스킨 설정', wiki_set(), custom(), other2([0, 0])],
                    data = '이 스킨은 설정 기능을 지원하지 않습니다.',
                    menu = 0
        ))
    data = flask.make_response(
        easy_minify(flask.render_template(skin_check(None),
            imp = ['스킨 설정', wiki_set(), custom(), other2([0, 0])],
            menu = 0
        ))
    )

    curs.execute("select data from other where name = 'language'")
    main_data = curs.fetchall()

    data.set_cookie('language', main_data[0][0])

    curs.execute('select data from user_set where name = "lang" and id = ?', [ip_check()])
    user_data = curs.fetchall()
    if user_data:
        data.set_cookie('user_language', user_data[0][0])
    else:
        data.set_cookie('user_language', main_data[0][0])



    return data

def main_skin_set_r_2(conn):

    return redirect('/settings')