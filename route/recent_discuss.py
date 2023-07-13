from .tool.func import *

def recent_discuss_2(conn):
    curs = conn.cursor()

    div = ''

    div += '''
    <ol class="breadcrumb link-nav">
        <li><a href="?logtype=normal_thread">[열린 토론]</a></li>
        <li><a href="?logtype=old_thread">[오래된 토론]</a></li>
        <li><a href="?logtype=agreed_thread">[합의된 토론]</a></li>
    '''
    if admin_check() == 1:
        div += '<li><a href="?logtype=deleted_thread">[삭제된 토론]</a></li>'
    div += '''
        <li><a href="?logtype=closed_thread">[닫힌 토론]</a></li>
        <li><a href="?logtype=open_editrequest">[열린 편집 요청]</a></li>
        <li><a href="?logtype=accepted_editrequest">[승인된 편집 요청]</a></li>
        <li><a href="?logtype=closed_editrequest">[닫힌 편집 요청]</a></li>
    </ol>
    '''

    m_sub = 0
    logtype = flask.request.args.get('logtype', '')

    div +=  '''

        <table class="table table-hover">
                    <colgroup>
        <col>
        <col style="width: 25%;">
        </colgroup><thead>

                    <tr class="nohov" style="border-bottom: 2px solid #eceeef;">
                        <td><b>''' + '항목' + '''</b></td>
                        <td><b>''' + '수정 시간' + '''</b></td>
                    </tr></thead><tbody id>
            '''
    typ_erq = 0

    #if admin_check() == 1:
        #ccmd = ''
    #else:
    ccmd = " and not removed = '1'"

    if logtype == 'normal_thread':
        curs.execute("select title, sub, date, tnum from rd where not stop = 'O' and not agree = 'O'" + ccmd + " order by date desc limit 120")
    elif logtype == 'deleted_thread' and admin_check() == 1:
        curs.execute("select title, sub, date, tnum from rd where removed = '1' order by date desc limit 120")
    elif logtype == 'old_thread':
        curs.execute("select title, sub, date, tnum from rd where not stop = 'O' and not agree = 'O'" + ccmd + " order by date asc limit 120")
    elif logtype == 'closed_thread':
        curs.execute("select title, sub, date, tnum from rd where stop = 'O'" + ccmd + " order by date desc limit 120")
    elif logtype == 'agreed_thread':
        curs.execute("select title, sub, date, tnum from rd where agree = 'O'" + ccmd + " order by date desc limit 120")
    elif logtype == 'open_editrequest':
        typ_erq = 1
        curs.execute("select num, name, time from erq where state = 'open' order by time desc limit 120")
    elif logtype == 'accepted_editrequest':
        typ_erq = 1
        curs.execute("select num, name, time from erq where state = 'accept' order by time desc limit 120")
    elif logtype == 'closed_editrequest':
        typ_erq = 1
        curs.execute("select num, name, time from erq where state = 'close' order by time desc limit 120")
    else:
        curs.execute("select title, sub, date, tnum from rd where not stop = 'O' and not agree = 'O'" + ccmd + " order by date desc limit 100")

    if logtype == '':
        for data in curs.fetchall():
            title = html.escape(data[0])
            sub = html.escape(data[1])

            ddd = data[2].split(' ')[0]
            ttt = data[2].split(' ')[1]
            date = '<time datetime="' + ddd + 'T' + ttt + '.000Z" data-format="Y-m-d H:i:s">' + data[2] + '</time>'

            div += '<tr><td><a href="/thread/' + url_pas(data[3]) + '">' + sub + '</a> (<a href="/discuss/' + url_pas(title) + '">' + title + '</a>)</td><td>' + date + '</td></tr>'

        curs.execute("select num, name, time from erq where state = 'open' order by time desc limit 20")
        for data in curs.fetchall():
            ddd = data[2].split(' ')[0]
            ttt = data[2].split(' ')[1]
            date = '<time datetime="' + ddd + 'T' + ttt + '.000Z" data-format="Y-m-d H:i:s">' + data[2] + '</time>'
            div += '<tr><td><a href="/edit_request/' + url_pas(data[0]) + '">편집 요청 ' + data[0] + '</a> (<a href="/discuss/' + url_pas(data[1]) + '">' + data[1] + '</a>)</td><td>' + date + '</td></tr>'
    else:
        if typ_erq == 1:
            for data in curs.fetchall():
                ddd = data[2].split(' ')[0]
                ttt = data[2].split(' ')[1]
                date = '<time datetime="' + ddd + 'T' + ttt + '.000Z" data-format="Y-m-d H:i:s">' + data[2] + '</time>'
                div += '<tr><td><a href="/edit_request/' + url_pas(data[0]) + '">편집 요청 ' + data[0] + '</a> (<a href="/discuss/' + url_pas(data[1]) + '">' + data[1] + '</a>)</td><td>' + date + '</td></tr>'
        else:
            for data in curs.fetchall():
                title = html.escape(data[0])
                sub = html.escape(data[1])

                ddd = data[2].split(' ')[0]
                ttt = data[2].split(' ')[1]
                date = '<time datetime="' + ddd + 'T' + ttt + '.000Z" data-format="Y-m-d H:i:s">' + data[2] + '</time>'

                div += '<tr><td><a href="/thread/' + url_pas(data[3]) + '">' + sub + '</a> (<a href="/discuss/' + url_pas(title) + '">' + title + '</a>)</td><td>' + date + '</td></tr>'

    div += '</tbody></table>'

    return easy_minify(flask.render_template(skin_check(),
        imp = [load_lang('recent_discussion'), wiki_set(), custom(), other2([m_sub, 0])],
        data = div,
        menu = 0,
        rd = 1
    ))