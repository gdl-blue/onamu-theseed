from .tool.func import *

def topic_2(conn, name, sub):
    tit = name + ' (토론) - ' + sub + ' - ' + wiki_set()[0]
    curs = conn.cursor()
    
    ban = topic_check(name, sub)
    admin = admin_check(3)
    
    if acl_check(name, 'render') == 1:
        return re_error('/error/3')
    

    curs.execute("select id from topic where title = ? and sub = ? limit 1", [name, sub])
    topic_exist = curs.fetchall()
    if not topic_exist and len(sub) > 256:
        return re_error('/error/11')
    
    if flask.request.method == 'POST':
        if captcha_post(flask.request.form.get('g-recaptcha-response', '')) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)

        ip = ip_check()
        today = get_time()
        
        if ban == 1:
            return re_error('/ban')
        
        curs.execute("select id from topic where title = ? and sub = ? order by id + 0 desc limit 1", [name, sub])
        old_num = curs.fetchall()
        if old_num:
            num = int(old_num[0][0]) + 1
        else:
            num = 1

        match = re.search('^사용자:([^/]+)', name)
        if match:
            y_check = 0
            if ip_or_user(match.groups()[0]) == 1:
                curs.execute("select ip from history where ip = ? limit 1", [match.groups()[0]])
                u_data = curs.fetchall()
                if u_data:
                    y_check = 1
                else:
                    curs.execute("select ip from topic where ip = ? limit 1", [match.groups()[0]])
                    u_data = curs.fetchall()
                    if u_data:
                        y_check = 1
            else:
                curs.execute("select id from user where id = ?", [match.groups()[0]])
                u_data = curs.fetchall()
                if u_data:
                    y_check = 1

            if y_check == 1:
                curs.execute('insert into alarm (name, data, date) values (?, ?, ?)', [
                    match.groups()[0], 
                    ip + ' - <a href="/topic/' + url_pas(name) + '/sub/' + url_pas(sub) + '">' + load_lang('user_discussion', 1) + '</a>', 
                    today
                ])
        
        cate_re = re.compile('\[\[((?:분류|category):(?:(?:(?!\]\]).)*))\]\]', re.I)
        data = cate_re.sub('[br]', flask.request.form.get('content', 'Test'))
        
        for rd_data in re.findall("(?:#([0-9]+))", data):
            curs.execute("select ip from topic where title = ? and sub = ? and id = ?", [name, sub, rd_data])
            ip_data = curs.fetchall()
            if ip_data and ip_or_user(ip_data[0][0]) == 0:
                curs.execute('insert into alarm (name, data, date) values (?, ?, ?)', [ip_data[0][0], ip + ' - <a href="/topic/' + url_pas(name) + '/sub/' + url_pas(sub) + '#' + str(num) + '">' + load_lang('discussion', 1) + '</a>', today])
            
        data = re.sub("(?P<in>#(?:[0-9]+))", '[[\g<in>]]', data)

        data = savemark(data)

        rd_plus(name, sub, today)

        curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm) values (?, ?, ?, ?, ?, ?, '', '', ?)", [str(num), name, sub, data, today, ip, admin])
        conn.commit()
        
        return redirect('/topic/' + url_pas(name) + '/sub/' + url_pas(sub) + '#reload')
    else:
        curs.execute("select title from rd where title = ? and sub = ? and stop = 'O'", [name, sub])
        close_data = curs.fetchall()
        
        curs.execute("select title from rd where title = ? and sub = ? and stop = 'S'", [name, sub])
        stop_data = curs.fetchall()
        
        display = ''
        all_data = ''
        data = ''
        number = 1
        
        if (close_data or stop_data) and admin != 1:
            display = 'display: none;'
        
        curs.execute("select data, id, date, ip, block, top from topic where title = ? and sub = ? order by id + 0 asc", [name, sub])
        topic = curs.fetchall()
        
        curs.execute("select data, id, date, ip from topic where title = ? and sub = ? and top = 'O' order by id + 0 asc", [name, sub])
        for topic_data in curs.fetchall():                   
            who_plus = ''
            
            curs.execute("select who from re_admin where what = ? order by time desc limit 1", ['notice (' + name + ' - ' + sub + '#' + topic_data[1] + ')'])
            topic_data_top = curs.fetchall()
            if topic_data_top:
                who_plus += ' <span style="margin-right: 5px;">@' + topic_data_top[0][0] + ' </span>'
                                
            all_data += '''
                <div style="overflow-x: scroll;"><table id="toron">
                    <tbody>
                        <tr>
                            <td id="toron_color_red">
                                <a href="#''' + topic_data[1] + '''">
                                    #''' + topic_data[1] + '''
                                </a> ''' + ip_pas_t(topic_data[3]) + who_plus + ''' <span style="float: right;">''' + topic_data[2] + '''</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px 10px 15px;background:#e8e8e8;color:#4a4a4a; border:none; border-radius:0; box-sizing:inherit; display:block; box-sizing:inherit; box-sizing:inherit; font-size:1rem; font-weight:400;">''' + render_set(data = topic_data[0]) + '''</td>
                        </tr>
                    </tbody>
                </table></div><br>
                <hr class=\"main_hr\"><br>
            '''    
        nn = 1
        for topic_data in topic:
            curs.execute("select block, ip, date from topic where title = ? and sub = ? and id = ?", [url_pas(name), url_pas(sub), str(number)])
            admdswiwdiataa = curs.fetchall()
            user_write = topic_data[0]
            user_write = render_set(data = user_write)
            ip = ip_pas_t(topic_data[3])
            curs.execute('select acl from user where id = ?', [topic_data[3]])
            user_acl = curs.fetchall()
            blablabla = 0
            
            

            if number == 1:
                start = topic_data[3]
            if topic_data[4] == 'O':
                blind_data = 'id="toron_color_grey"'
                
                if admin != 1:
                    curs.execute("select who from re_admin where what = ? order by time desc limit 1", ['blind (' + name + ' - ' + sub + '#' + str(number) + ')'])
                    who_blind = curs.fetchall()
                    if who_blind:
                        user_write = '[' + who_blind[0][0] + '에 의해 숨겨진 글입니다.]'
                        blablabla = 1
                    else:
                        user_write = '[숨겨진 글입니다.]'
                        blablabla = 1
                if admin == 1:
                    curs.execute("select who from re_admin where what = ? order by time desc limit 1", ['blind (' + name + ' - ' + sub + '#' + str(number) + ')'])
                    who_blind = curs.fetchall()
                    if who_blind:
                        user_write ='[' + who_blind[0][0] + '에 의해 숨겨진 글입니다.]<br><div class="text-line-break" style="margin: 25px 0px 0px -10px; color: #fff; display:block" id="shc' + str(number) + '"><a class="text" onclick="getElementById(\'hc' + str(number) + '\').style.display = \'block\';getElementById(\'shc' + str(number) + '\').style.display = \'none\';" style=" color: #fff;">[ADMIN] Show hidden content</a><div class="line"></div></div><div id="hc' + str(number) + '" style="display:none"><br>' + user_write + '</div>'
                        blablabla = 1
                    else:
                        user_write = '[숨겨진 글입니다.]<br><br>' + user_write
                        blablabla = 1
            else:
                blind_data = ''
            
            admminadina = 'ds'
            curs.execute("select adm from topic where id = ?", [str(number)])
            aasadadddaadda = curs.fetchall()
            if topic_data[3] == start:
                 if user_acl and user_acl[0][0] != 'user':
                    if aasadadddaadda and aasadadddaadda[0][0] == '1':
                        admminadina = 'ad'
                        ip = '<strong>' + ip
                        ip += '</strong>'
                        #ip += ' <a href="javascript:void(0);" title="' + load_lang('admin') + '">★</a>'
            else:
                #if user_acl and user_acl[0][0] != 'user':
                if aasadadddaadda and aasadadddaadda[0][0] == '1':
                    admminadina = 'ad'
                    ip = '<strong>' + ip
                    ip += '</strong>'
                    #ip += ' <a href="javascript:void(0);" title="' + load_lang('admin') + '">★</a>'
                
            curs.execute("select end from ban where block = ?", [topic_data[3]])
            if curs.fetchall():
                if re.search(".*\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}.*", ip):
                    ip += ' <sub>(차단된 아이피)</sub>'
                else:
                    ip += ' <sub>(차단된 사용자)</sub>'
                    
            curs.execute("select date from topic where title = ? and sub = ? and id = ?", [name, sub, str(number)])
            dt = curs.fetchall()
            
            
            

            #if admin == 1 or blind_data == '':
                #ip += '<a href="/topic/' + url_pas(name) + '/sub/' + url_pas(sub) + '/admin/' + str(number) + '"> [도구]</a>'
                
            


            
            oraoraorgaanna = 0
                    
            if topic_data[5] == '1':
                oraoraorgaanna = 1
                color = '_blue'
            elif topic_data[3] == start:
                color = '_green'
            else:
                color = ''
                
            if user_write == '':
                user_write = '<br>'
            
            if dt:
                all_data += '''
                    <div style="overflow-x: scroll;"><table id="toron" style="background: transparent;overflow-x: scroll;">
                        <tbody>
                            <tr>
                                <td id="toron_color''' + color + '''">
                                    <a href="javascript:void(0);" id="''' + str(number) + '">#' + str(number) + '</a> ' + ip + '''<span style="float:right">''' + dt[0][0] + '''</span></span>
                                </td>
                            </tr>
                            <tr ''' + blind_data + '''>
                                <td style="padding:5px 10px 10px 15px; '''
                
          
            if oraoraorgaanna == 1:
                if blablabla == 1:
                    all_data += '''background:orange;color:#fff'''
                else:
                    all_data += '''background:orange'''
            else:
                if blablabla == 1:
                    all_data += '''background:#000;color:#fff'''
                else:
                    all_data += '''background:#e8e8e8;color:#4a4a4a'''
            
            all_data += '''; border:none;border-radius:0; box-sizing:inherit; display:block; box-sizing:inherit; box-sizing:inherit; font-size:1rem; font-weight:400;">''' + user_write + '''</td>
                        </tr>
                    </tbody>
                    
                </table></div>
                '''
            if admin == 1:
                all_data += '''
                <span style="color:#fff; background-color:#d9534f; border-color:#d9534f; display:inline-block; font-weight:400; text-align:center; border:1px solid transparent; padding:.25rem .5rem; font-size:.875rem; border-radius:.2rem;"><span class="wiki-color" style="color:#FFFFFF"><a href="/topic/''' + url_pas(name) + '''/sub/''' + url_pas(sub) + '''/b/''' + str(number) + '''" style="color:#fff">'''
                if blablabla == 1:
                    all_data += '''[ADMIN] 숨기기 해제'''
                else:
                    all_data += '''[ADMIN] 숨기기'''
                all_data += '''</a></span></span>
                    

            '''
            all_data += '''<br><br>'''

            number += 1
            
        nn = str(number)
            

        if ban != 1 or admin == 1:
            data += '''
                </div><input type="hidden" id="isa" value="''' + str(admin) + '''">
                <div id="plus_topic"></div>
                <script>topic_plus_load("''' + str(name) + '''", "''' + str(sub) + '''", ''' + nn + ''');</script>
                
                <br><h2 style="cursor: pointer; border: none;" onclick="var dc = document.getElementById(\'dcf\'); if(dc.style.display == \'block\') dc.style.display = \'none\'; else dc.style.display = \'block\'; ">댓글 달기</h2><div id="dcf" style="display: block; ">'''
            if admin == 1:
                data += '''
                    [ADMIN] 쓰레드 상태 변경 <select name="status" id="sttssu">
                        <option value="close" selected>close</option>
                        <option value="close">open</option>
                        <option value="agree">합의</option>
                        <option value="agree">normal</option>
                        <option value="stop">stop</option>
                        <option value="stop">restart</option>
		
                    </select>  <button type="button" onclick="location.href = '/topic/''' + url_pas(name) + '''/sub/''' + url_pas(sub) + '''/tool/' + getElementById('sttssu').value;">변경</button><br />
                '''
                
            data += '''
                    [ADMIN] 댓글 도구 <input id="ttl" placeholder="#N" style="width:160px">
		
                    </input>  <button type="button" onclick="location.href = '/topic/''' + url_pas(name) + '''/sub/''' + url_pas(sub) + '''/admin/' + getElementById('ttl').value;">확인</button><br />
                    [ADMIN] 스레드 도구 <input id="sb" placeholder="#N" style="width:160px" value="''' + sub + '''">
		
                    </input>  <button type="button" onclick="location.href = '/topic/''' + url_pas(name) + '''/sub/' + document.getElementById('sb').value + '/tool';">확인</button><br />
                '''
            
            data += '''
                <form style="''' + display + '''" method="post">
                    <textarea style="height: 100px;" name="content"></textarea>
                    ''' + captcha_get() + (ip_warring() if display == '' else '') + '''
                    <button type="submit" id="save" style="width:120px">''' + load_lang('send') + '''</button>
                </form></div>
            '''

        return easy_minify(flask.render_template(skin_check(), 
            imp = [name, wiki_set(), custom(), other2([' (' + load_lang('discussion') + ') - ' + sub, 0])],
            data = '<h2 id="topic_top_title" style="cursor: pointer; border: none;" onclick="var ddd = document.getElementById(\'tb\'); if(ddd.style.display == \'block\') ddd.style.display = \'none\'; else ddd.style.display = \'block\'; ">' + sub + '</h2><div style="display:block" id="tb">' + all_data + data,
            menu = [['topic/' + url_pas(name), load_lang('list')]],
            st = 3
        ))
