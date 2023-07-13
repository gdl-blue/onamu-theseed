from .tool.func import *

def give_admin_un_2(conn):
    curs = conn.cursor()

    if admin_check(7) != 1:
        return re_error('/error/3')

    return easy_minify(flask.render_template(skin_check(),
        imp = ['권한 부여', wiki_set(), custom(), other2(['', 0])],
        data =  '''
                <form>
                    유저 이름 : <br>
                    <input type=text id="un" style="width: 250px;"></input><br>
                    <button type="button" onclick="location.href = '/admin/grant/' + document.getElementById('un').value;" style="width:120px; " class="btn btn-info">확인</button>
                </form>
                ''',
        menu = 0
    ))
