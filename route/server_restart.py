from .tool.func import *

def server_restart_2(conn):
    curs = conn.cursor()

    if admin_check() != 1:
        return re_error('/error/3')

    if flask.request.method == 'POST':
        admin_check(None, 'restart')

        print('----')
        print('Restart')

        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        return easy_minify(flask.render_template(skin_check(), 
            imp = [load_lang('wiki_restart'), wiki_set(), custom(), other2([0, 0])],
            data =  '''
                    <form method="post">
                        위키 엔진을 재시동합니다.<br><br>
                        <button type="submit" id="save">''' + load_lang('restart') + '''</button>
                        <button type="button" onclick="location.href = '/manager';">취소</button>
                    </form>
                    ''',
            menu = [['manager', load_lang('return')]]
        ))