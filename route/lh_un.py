from .tool.func import *

def lh_un_2(conn):
    curs = conn.cursor()

    if admin_check(4) != 1:
        return re_error('/error/3')

    if flask.request.method == 'POST':
        return redirect('/admin/login_history/' + getForm('username'))
    else:
        return easy_minify(flask.render_template(skin_check(),
            imp = ['로그인 내역', wiki_set(), custom(), other2(['', 0])],
            data =  '''
                    <form method=post>
                        <div>
                        <label>유저 이름 :</label><br>
                        <input type="text" class="form-control" id="usernameInput" name="username" style="width: 250px;" value="">
                        </div>
                        <button type=submit class="btn btn-info pull-right" style="width: 100px;" id=moveBtn>확인</button>
                    </form>
                    ''',
            menu = 0
        ))
