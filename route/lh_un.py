from .tool.func import *

def lh_un_2(conn):
    curs = conn.cursor()
    
    if admin_check(4) != 1:
        return re_error('/error/3')
    
    return easy_minify(flask.render_template(skin_check(), 
        imp = ['로그인 내역', wiki_set(), custom(), other2(['', 0])],
        data =  '''
                <form>
                    유저 이름 : <br>
                    <input id="un" style="width: 250px;"></input><br>
                    <button type="button" onclick="location.href = '/login_history/' + document.getElementById('un').value;" style="color:#fff; width:120px;    background-color: #5bc0de; border-color: #5bc0de;display: inline-block;font-weight: 400; line-height: 1.25;text-align: center;   white-space: nowrap;vertical-align: middle;user-select: none; border: 1px solid transparent;   padding: .5rem 1rem;    font-size: 1rem;   border-radius: .25rem;    transition: all .2s ease-in-out;">확인</button>
                </form>
                ''',
        menu = 0
    ))
