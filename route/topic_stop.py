from .tool.func import *

def topic_stop_2(conn, name, sub, tool):
    curs = conn.cursor()

    if admin_check(3, 'topic ' + tool + ' (' + name + ' - ' + sub + ')') != 1:
        return re_error('/error/3')

    ip = ip_check()
    time = get_time()
    curs.execute("select id from topic where title = ? and sub = ? order by id + 0 desc limit 1", [name, sub])
    topic_check = curs.fetchall()
    if topic_check:
        if tool == 'agree':
            curs.execute("select title from rd where title = ? and sub = ? and agree = 'O'", [name, sub])
            if curs.fetchall():
                curs.execute("insert into topic (id, title, sub, data, date, ip, block, top) values (?, ?, ?, '스레드 상태를 normal로 변경', ?, ?, '', '1')", [str(int(topic_check[0][0]) + 1), name, sub, time, ip])
                curs.execute("update rd set agree = '' where title = ? and sub = ?", [name, sub])
            else:
                curs.execute("insert into topic (id, title, sub, data, date, ip, block, top) values (?, ?, ?, '스레드 상태를 합의로 변경', ?, ?, '', '1')", [str(int(topic_check[0][0]) + 1), name, sub, time, ip])
                curs.execute("update rd set agree = 'O' where title = ? and sub = ?", [name, sub])
        else:
            if tool == 'close':
                why = flask.request.form.get('why', '')
                set_list = [
                    'O', 
                    'S', 
                    '스레드 상태를 \'\'\'close\'\'\'로 변경' + (('[br][br]' + why) if why else ''), 
                    '스레드 상태를 \'\'\'open\'\'\'로 변경' + (('[br][br]' + why) if why else '')
                ]
            elif tool == 'stop':
                set_list = ['', 'O', '스레드 상태를 \'\'\'stop\'\'\'로 변경', '스레드 상태를 \'\'\'restart\'\'\'로 변경']
            else:
                return redirect('/topic/' + url_pas(name) + '/sub/' + url_pas(sub))

            curs.execute("select title from rd where title = ? and sub = ? and stop = ?", [name, sub, set_list[0]])
            if curs.fetchall():
                curs.execute("insert into topic (id, title, sub, data, date, ip, block, top) values (?, ?, ?, ?, ?, ?, '', '1')", [str(int(topic_check[0][0]) + 1), name, sub, set_list[3], time, ip])
                curs.execute("update rd set stop = '' where title = ? and sub = ?", [name, sub])
            else:
                curs.execute("insert into topic (id, title, sub, data, date, ip, block, top) values (?, ?, ?, ?, ?, ?, '', '1')", [str(int(topic_check[0][0]) + 1), name, sub, set_list[2], time, ip])
                curs.execute("update rd set stop = ? where title = ? and sub = ?", [set_list[0], name, sub])
        
        rd_plus(name, sub, time)
        
        conn.commit()

    return redirect('/topic/' + url_pas(name) + '/sub/' + url_pas(sub))    
