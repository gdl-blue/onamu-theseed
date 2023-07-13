from .tool.func import *

def regc_2(conn, name):
    curs = conn.cursor()
    
    return easy_minify(flask.render_template(skin_check(), 
        imp = ['계정 만들기', wiki_set(), custom(), other2(['', 0])],
        data =  '''
                환영합니다! <b>''' + name + '''</b>님 계정 생성이 완료되었습니다.''',
        menu = 0
    ))