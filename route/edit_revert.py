from .tool.func import *
import urllib

def view_raw_2_hg(conn, name, sub_title, num):
    curs = conn.cursor()

    v_name = name
    
    if not num:
        num = flask.request.args.get('num', None)
        if num:
            num = int(number_check(num))
    
    curs.execute("select data from history where title = ? and id = ?", [name, str(num)])
    data = curs.fetchall()
    if data:
        p_data = html.escape(data[0][0])
        
        return p_data
    else:
        return '(미리보기를 불러올 수 없음)'

def edit_revert_2(conn, name):
    curs = conn.cursor()
    
    if acl_check(name, 'render') == 1:
        return re_error('/error/3')

    num = int(number_check(flask.request.args.get('num', '1')))

    curs.execute("select title from history where title = ? and id = ? and hide = 'O'", [name, str(num)])
    if curs.fetchall() and admin_check(6) != 1:
        return re_error('/error/3')

    if acl_check(name) == 1:
        return re_error('/ban')

    if flask.request.method == 'POST':
        if captcha_post(flask.request.form.get('g-recaptcha-response', '')) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)
    
        curs.execute("select data from history where title = ? and id = ?", [name, str(num)])
        data = curs.fetchall()
        if data:
            if edit_filter_do(data[0][0]) == 1:
                return re_error('/error/21')

        curs.execute("delete from back where link = ?", [name])
        conn.commit()
        
        if data:                                
            curs.execute("select data from data where title = ?", [name])
            data_old = curs.fetchall()
            if data_old:
                leng = leng_check(len(data_old[0][0]), len(data[0][0]))
                curs.execute("update data set data = ? where title = ?", [data[0][0], name])
            else:
                leng = '+' + str(len(data[0][0]))
                curs.execute("insert into data (title, data) values (?, ?)", [name, data[0][0]])
                
            history_plus(
                name, 
                data[0][0], 
                get_time(), 
                ip_check(), 
                flask.request.form.get('send', ''), 
                leng,
                'r' + str(num) + '으로 되돌림'
            )

            render_set(
                title = name,
                data = data[0][0],
                num = 1
            )
            
            conn.commit()
            
        return redirect('/w/' + url_pas(name))
    else:
        curs.execute("select title from history where title = ? and id = ?", [name, str(num)])
        if not curs.fetchall():
            return redirect('/w/' + url_pas(name))
#<span>r''' + flask.request.args.get('num', '0') + '''</span>
        return easy_minify(flask.render_template(skin_check(), 
            imp = [name, wiki_set(), custom(), other2([' (r' + str(int(flask.request.args.get('num', '0'))) + '로 ' + load_lang('revert') + ')', 0])],
            data =  '''
                    <form method="post">
                        <textarea rows="25" name="content" readonly="" disabled="" style="background:#eceeef;width:100% !important;">''' + view_raw_2_hg(conn, urllib.parse.unquote(url_pas(name)), urllib.parse.unquote(url_pas(name)), int(flask.request.args.get('num', '0'))) + '''</textarea>
                        
                        <b>''' + ip_warring() + '''</b><br><br>
                        요약<br><input name="send" type="text" style="width:100% !important;">
                        ''' + captcha_get() + '''
                        <button type="submit" sid="save">''' + load_lang('revert') + '''</button>
                    </form>
                    ''',
            menu = [['history/' + url_pas(name), load_lang('history')], ['recent_changes', '최근 변경']],
            st = 0
        ))