from .tool.func import *
from flask import Flask, request, render_template

def topic_close_list_2(conn, name, tool):
    curs = conn.cursor()

    if getacl(name, 'read') == 0:
        return noread(conn, name)

    if re.search('^사용자:', name):
        ns = '사용자'
    elif re.search('^분류:', name):
        ns = '분류'
    elif re.search('^틀:', name):
        ns = '틀'
    elif re.search('^휴지통:', name):
        ns = '휴지통'
    elif re.search('^파일:', name):
        ns = '파일'
    elif re.search('^' + wiki_set()[0] + ':', name):
        ns = wiki_set()[0]
    else:
        ns = '문서'

    div = ''

    if flask.request.method == 'POST':
        cny = format(request.form['conty'])

        perm = getacl(name, 'create_thread')
        if perm == 0:
            return re_error('/error/3')

        adm = admin_check(5)

        tntyp = ''.join(random.choice("0123456789aaaaaaaaaabbbbbbbbbbaaaaaaaaaabbbbbbbbbbaaaaaaaaaabbbbbbbbbbaaaaaaaaaabbbbbbbbbbaaaaaaaaaa") for i in range(1))
        if tntyp == '0' or tntyp == '1' or tntyp == '2' or tntyp == '3' or tntyp == '4': #5%의 확률
            tn = generateRandomWords()
        else:
            tn = ''.join(random.choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(22))
        curs.execute("select tnum from rd where tnum = ?", [tn])
        tnex = curs.fetchall()
        while tnex:
            tn = ''.join(random.choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(22))
            curs.execute("select tnum from rd where tnum = ?", [tn])
            tnex = curs.fetchall()

        try:
            curs.execute("select last from lastrd where m = '1'")
            tnumber = str(int(curs.fetchall()[0][0]) + 1)
            curs.execute("update lastrd set last = ? where m = '1'", [tnumber])
        except:
            tnumber = '1'
            curs.execute("insert into lastrd (last, m) values ('1', '1')")

        curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm, tnum, tnumber) values (?, ?, ?, ?, ?, ?, '', '', ?, ?, ?)", [1, name, flask.request.form.get('topic'), cny, get_time(), ip_check(), adm, tn, tnumber])
        curs.execute("insert into rd (title, sub, date, tnum, tnumber) values (?, ?, ?, ?, ?)", [name, flask.request.form.get('topic'), get_time(), tn, tnumber])
        conn.commit()

        return redirect('/thread/' + url_pas(tn))
    else:
        plus = ''
        menu = [['discuss/' + url_pas(name), load_lang('return')]]

        eq = ['']
        curs.execute("select num from erq where name = ? and state = 'open' order by time asc", [name])
        eq = curs.fetchall()

        if tool == 'close':
            if admin_check() == 1:
                curs.execute("select sub, tnum from rd where title = ? and stop = 'O' order by sub asc", [name])
            else:
                curs.execute("select sub, tnum from rd where title = ? and stop = 'O' and not removed = '1' order by sub asc", [name])

            sub = load_lang('close') + ''
        elif tool == 'agree':
            if admin_check() == 1:
                curs.execute("select sub, tnum from rd where title = ? and agree = 'O' order by sub asc", [name])
            else:
                curs.execute("select sub, tnum from rd where title = ? and agree = 'O' and not removed = '1' order by sub asc", [name])

            sub = load_lang('agreement') + ''
        elif tool == 'eqclose':
            curs.execute("select num from erq where name = ? and state = 'close' order by time asc", [name])

            sub = '닫힌 편집 요청'
        else:
            if admin_check() == 1:
                curs.execute("select sub, tnum from rd where title = ? and not agree = 'O' order by date desc", [name])
            else:
                curs.execute("select sub, tnum from rd where title = ? and not agree = 'O' and not removed = '1' order by date desc", [name])

            sub = load_lang('discussion_list') + ''

            menu = [['w/' + url_pas(name), load_lang('document')]]

            warn = ''
            if name == wiki_set()[0] or name == wiki_set()[0] + ':대문':
                warn = '''<div class="alert alert-success alert-dismissible" role=alert><strong>[경고!]</strong> 이 토론은 ''' + name + ''' 문서의 토론입니다. ''' + name + ''' 문서와 관련 없는 토론은 각 문서의 토론에서 진행해 주시기 바랍니다. ''' + name + ''' 문서와 관련 없는 토론은 삭제될 수 있습니다.</div><br>'''

            plus =  '''
                    <br><br><h3 style="font-weight: 600; font-size: 1.6em; cursor: pointer; border: none; margin-top:12px; " class="wiki-heading">새 주제 생성</h3>''' + warn + '''<div id="newt" style="display:block;">주제 : <br>
                    <input class="form-control" name="topic" type="text"><br>
                    내용 : <br>
                    <textarea class="form-control" name="conty" rows="5"></textarea>
                    <div class="btns pull-right"><button type="submit" class="btn btn-primary" style="width:120px">전송</button></div></div>
                    '''
        cnt = 1
        if tool == 'close' or tool == 'agree' or tool == 'eqclose':
            div = '<ul>'
            edv = '<ul>'
        else:
            div = '<h3 class="wiki-heading" style="font-weight: 600; font-size: 1.6em; cursor: pointer; border: none; ">토론</h3><ul id="tl" style="display:block;">'
            edv = '<h3 class="wiki-heading" style="font-weight: 600; font-size: 1.6em; cursor: pointer; border: none; ">편집 요청</h3><ul id="el" style="display:block;">'
        for data in curs.fetchall():
            if not(tool == 'eqclose'):
                curs.execute("select data, date, ip, block from topic where title = ? and sub = ? and id = '1'", [name, data[0]])
                if curs.fetchall():
                    it_p = 0

                    if sub == load_lang('discussion_list'):
                        curs.execute("select title from rd where title = ? and sub = ? and stop = 'O' order by sub asc", [name, data[0]])
                        if curs.fetchall():
                            it_p = 1

                    if it_p != 1:
                        div += '<li><a href="#tp' + str(cnt) + '">' + str(cnt) + '</a>. <a href="/thread/' + url_pas(data[1]) + '">' + data[0] + '</a></li>'
            else:
                div += '<li><a href="/edit_request/' + url_pas(data[0]) + '">편집 요청 ' + data[0] + '</a></li>'

            cnt += 1
        vct = '''<a href="/discuss/''' + url_pas(name) + '''/close">[''' + load_lang('close') + ''' 목록 보기]</a>'''
        vct += ''' <a href="/discuss/''' + url_pas(name) + '''/agree">[합의된 토론 목록 보기]</a>'''
        for data in eq:
            edv += '<li><a href="/edit_request/' + url_pas(data[0]) + '">편집 요청 ' + data[0] + '</a></li>'
        div += '</ul>'
        edv += '</ul><a href="/discuss/''' + url_pas(name) + '/eqclose">[닫힌 편집 요청 보기]</a><br><br>'
        if div == '':
            plus = re.sub('^<br>', '', plus)
        if tool == 'close':
            edv = ''
            vct = ''
        elif tool == 'agree':
            edv = ''
            vct = ''
        elif tool == 'eqclose':
            edv = ''
            vct = ''

        tp = ''
        cnt = 1
        if admin_check() == 1:
            curs.execute("select sub, tnum from rd where title = ? and stop = '' and not agree = 'O' order by date desc", [name])
        else:
            curs.execute("select sub, tnum from rd where title = ? and stop = '' and not agree = 'O' and not removed = '1' order by date desc", [name])
        for data in curs.fetchall():
            tp += '''<br><h2 id="tp''' + str(cnt) + '''" style="border:0;cursor: pointer;" class="wiki-heading"><a href="/thread/''' + url_pas(data[1]) + '''">''' + data[0] + '''</a></h2><div class=topic-discuss id="tpt''' + str(cnt) + '''" style="display:block">
            '''
            tn = data[0]
            tid = data[1]

            curs.execute("select title from rd where title = ? and sub = ? and stop = 'O'", [name, sub])
            close_data = curs.fetchall()

            curs.execute("select title from rd where title = ? and sub = ? and stop = 'S'", [name, sub])
            stop_data = curs.fetchall()

            display = ''
            all_data = ''
            data = ''
            number = 1

            curs.execute("select id from topic where title = ? and sub = ? order by id + 0 desc limit 1", [name, tn])
            old_num = curs.fetchall()
            if old_num:
                num = int(old_num[0][0])
            else:
                num = 0

            ctct = 1

            curs.execute("select data, id, date, ip, block, top, ismember from topic where tnum = ? order by id + 0 asc", [tid])
            ttbgt = curs.fetchall()
            nn = 1
            for topic_data in ttbgt:
                if (num > 4) and (1 < number < num - 2):
                    if number == num - 3 :
                        all_data += '''<a class=more-box href="/thread/''' + url_pas(tid) + '''">more...</a>'''
                    number += 1
                    continue
                if num > 4 and ctct >= num:
                    break
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
                    curs.execute("select who from re_admin where what = ? order by time desc limit 1", ['blind (' + name + ' - ' + tn + '#' + str(number) + ')'])
                    who_blind = curs.fetchall()
                    if who_blind:
                        user_write = '[' + who_blind[0][0] + '에 의해 숨겨진 글입니다.]'
                        blablabla = 1
                    else:
                        user_write = '[숨겨진 글입니다.]'
                        blablabla = 1
                    curs.execute("select perm from grant where perm = ? and user = ?", ['htc', ip_check()])
                    if curs.fetchall():
                        user_write += '''
                        <ctl>
                            <br>
                            <div class="text-line-break" style="margin: 25px 0px 0px -10px; display:block">
                                <a class="text" onclick="$(this).parent().parent().children(\'.hidden-content\').show(); return false;" style="display: block; color: #fff;">[ADMIN] Show hidden content</a>
                                <div class="line"></div>
                            </div>
                            <div class="hidden-content" style="display:none">''' + render_set(data = topic_data[0]) + '''</div>
                        </ctl>'''

                dt = [['']]
                curs.execute("select date from topic where title = ? and sub = ? and id = ?", [name, tn, str(number)])
                dt = curs.fetchall()

                oraoraorgaanna = 0

                if topic_data[5] == '1':
                    oraoraorgaanna = 1
                    if topic_data[3] == start:
                        color = '_green'
                    else:
                        color = ''
                elif topic_data[3] == start:
                    color = '_green'
                else:
                    color = ''

                if user_write == '':
                    user_write = '<br>'

                if oraoraorgaanna == 1:
                    rt = 'status'
                else:
                    rt = 'normal'

                if oraoraorgaanna == 1 and re.search('스레드 상태를 <strong>.*</strong>로 변경', user_write):
                    user_write = (user_write.replace('스레드 상태를 <strong>', '')).replace('</strong>로 변경', '')

                if dt:
                    ddd = dt[0][0].split(' ')[0]
                    ttt = dt[0][0].split(' ')[1]

                    if topic_data[3] == start:
                        fa = ' first-author'
                    else:
                        fa = ''

                    all_data += '''
                        <div class="res-wrapper">
                            <div class="res res-type-''' + rt + '''">
                                <div class="r-head''' + fa + '''">
                                    <span class="num">#''' + str(number) + '&nbsp;</span>' + ip + '''<span style="float:right; margin-left: 25px;"><time datetime="''' + ddd + 'T' +  ttt + '''.000Z" data-format="Y-m-d H:i:s">''' + dt[0][0] + '''</time></span>
                                </div>
                                <div class="r-body'''
                else:
                    break;


                if blablabla == 1:
                    all_data += ' r-hidden-body'

                all_data += '''">''' + user_write + '''
                            </div>
                        </div>
                    </div>
                '''

                number += 1
                ctct += 1

            tp += all_data + '</div>'
            cnt += 1

        if tool == 'close':
            tp = ''
        elif tool == 'agree':
            tp = ''
        elif tool == 'eqclose':
            tp = ''

        if sub == '토론 목록':
            sub = '토론'

        if sub == load_lang('agreement') + '':
            sub = '합의된 토론'

        return easy_minify(flask.render_template(skin_check(),
            imp = [name, wiki_set(), custom(), other2([' (' + sub + ')', 0])],
            data =  '<form method="post">' + edv + div + vct + tp + plus + '</form>',
            menu = menu,
            st = 3,
            smsub = ' (' + sub + ')'
        ))
