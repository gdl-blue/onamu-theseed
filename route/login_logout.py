from .tool.func import *

def login_logout_2(conn):
    curs = conn.cursor()

    resp = flask.make_response(flask.redirect(flask.request.args.get('redirect', '/')))

    resp.set_cookie('dooly', '', expires=0)
    resp.set_cookie('doornot', '', expires=0)

    curs.execute("delete from token where username = ?", [ip_check()])

    flask.session.pop('state', None)
    flask.session.pop('id', None)

    return resp