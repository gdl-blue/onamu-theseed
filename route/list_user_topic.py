from .tool.func import *

def list_user_topic_2(conn, name, ismember = 'author'):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 1000 > 0:
        sql_num = num * 1000 - 1000
    else:
        sql_num = 0

    one_admin = admin_check(1)

    curs.execute("select count(title) from topic where ip = ? and ismember = ? COLLATE NOCASE", [name, ismember])
    cntData = curs.fetchall()
    if cntData:
        cntData = cntData[0][0]
    else:
        cntData = 0
    #endif

    div = '<p>이 사용자의 토론 기여 횟수는 ' + str(cntData) + ' 입니다.</p>'

    div +=   '''<ol class="breadcrumb link-nav">
            <li><a href="./document">[문서]</a></li>
            <li><strong>[토론]</strong></li>
            </ol>
            <table class="table table-hover"> <colgroup> <col> <col style="width: 25%;"> <col style="width: 22%;"> </colgroup>'''





    div += '''  <thead>              <tr class="nohov" style="border-bottom: 2px solid #eceeef;">
                        <td><b>''' + '항목' + '''</b></td>
                        <td><b>''' + '수정자' + '''</b></td>
                        <td><b>''' + '수정 시간' + '''</b></td>
                    </tr></thead><tbody id>
            '''

    curs.execute("select title, id, sub, ip, date, tnum from topic where ip = ? and ismember = ? COLLATE NOCASE order by date desc limit ?, '1000'", [name, ismember, str(sql_num)])
    data_list = curs.fetchall()
    for data in data_list:
        title = html.escape(data[0])
        sub = html.escape(data[2])

        if one_admin == 1:
            curs.execute("select * from ban where block = ?", [data[3]])
            if curs.fetchall():
                ban = ' <a href="/ban/' + url_pas(data[3]) + '">[' + load_lang('release') + ']</a>'
            else:
                ban = ' <a href="/ban/' + url_pas(data[3]) + '">[' + load_lang('ban') + ']</a>'
        else:
            ban = ''

        div += '<tr><td><a href="/thread/' + url_pas(data[5]) + '#' + data[1] + '">' + '#' + data[1] + ' ' + sub + '</a> (' + '<a href="/w/' + url_pas(title) + '">' + title + '</a>)</td>'
        #div += '<tr><td><a href="/topic/' + url_pas(data[0]) + '/sub/' + url_pas(data[2]) + '#' + data[1] + '">' + title + '#' + data[1] + '</a> (' + sub + ')</td>'
        div += '<td>' + ip_pas(data[3]) + ban + '</td><td>' + data[4] + '</td></tr>'

    div += '</tbody></table>'
    div += next_fix('/topic_record/' + url_pas(name) + '?num=', num, data_list, 1000)

    curs.execute("select end from ban where block = ?", [name])
    if curs.fetchall():
        sub = ' (' + load_lang('blocked') + ')'
    else:
        sub = 0

    return easy_minify(flask.render_template(skin_check(),
        imp = ['"' + ip_pas_raw(name) + '" ' + '기여 목록', wiki_set(), custom(), other2([sub, 0])],
        data = div,
        menu = [['other', load_lang('other')], ['user', load_lang('user')], ['count/' + url_pas(name), load_lang('count')], ['record/' + url_pas(name), load_lang('record')]],
        cont = 1,
        un = name,
        contm = ''
    ))