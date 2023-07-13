from .tool.func import *

def ccs_2(conn):
    curs = conn.cursor()

    return easy_minify(flask.render_template(skin_check(), 
        imp = ['Candy Crush', wiki_set(), custom(), other2([0, 0])],
        data = open('./views/main_css/ccs.html', 'r').read(),
        menu = 0
    ))
    
def baduk_2(conn):
    curs = conn.cursor()

    return re_error('/error/99')
    
def janggi_2(conn):
    curs = conn.cursor()

    return re_error('/error/99')
    
def web_2(conn):
    curs = conn.cursor()

    return easy_minify(flask.render_template(skin_check(), 
        imp = ['웹서핑', wiki_set(), custom(), other2([0, 0])],
        data = '<label style="width:10%">주소 : </label><input id="addr" style="width:80%" value="https://www.daum.net/"> <button style="width:10%" type="button" onclick="document.getElementById(\'frm\').src = document.getElementById(\'addr\').value;">Go!</button><br><br><div style="padding: .5rem .75rem;font-size: 1rem;line-height: 1.25;color: #464a4c;background-color: #fff;background-image: none;background-clip: padding-box;border: 1px solid rgba(0,0,0,.15);border-radius: .25rem;transition: border-color ease-in-out .15s,box-shadow ease-in-out .15s;"><iframe src="https://www.daum.net/" style="width:100%;height:550px" id="frm" name="ifrm" onLoad="document.getElementById(\'addr\').value = document.getElementById(\'frm\').contentWindow.location.href;"></iframe></div><script>ifrm.onbeforeunload = function () {document.getElementById(\'addr\').value = document.getElementById(\'frm\').contentWindow.location.href;};</script>',
        menu = 0
    ))