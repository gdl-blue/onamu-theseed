from .tool.func import *

def login_logout_2(conn):
    curs = conn.cursor()

    flask.session.pop('state', None)
    flask.session.pop('id', None)

    return redirect(flask.request.args.get('redirect', '/'))