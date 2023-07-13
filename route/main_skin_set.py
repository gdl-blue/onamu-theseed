from .tool.func import *

def main_skin_set_2(conn):
    curs = conn.cursor()
    
    data = flask.make_response(sks('/error/5000'))

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