from .tool.func import *

def list_user_topic_2(conn, name):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0
    
    one_admin = admin_check(1)

    div =   '''<div style="padding: .75rem 1rem;margin-bottom: 1rem;list-style: none;background-color: #eceeef;border-radius: .25rem;"><a href="/contribution/author/''' + url_pas(name) + '''/document">[문서]</a><a href="/contribution/author/''' + url_pas(name) + '''/discuss"> [토론]</a></div>
            <table id="main_table_set" class="table table-hover" style="width:100%"> <colgroup> <col> <col style="width: 25%;"> <col style="width: 22%;"> </colgroup>
                <tbody>
                    <tr style="border-top:1px solid #eceeef;border-bottom:2px solid #eceeef;line-height:30px">
                        <td id="main_table_width"><b>''' + '항목' + '''</b></td>
                        <td id="main_table_width"><b>''' + '수정자' + '''</b></td>
                        <td id="main_table_width"><b>''' + '수정 시간' + '''</b></td>
                    </tr>
            '''
    
    curs.execute("select title, id, sub, ip, date from topic where ip = ? order by date desc limit ?, '50'", [name, str(sql_num)])
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
        
        div += '<tr style="line-height:30px" onmouseover="this.style.backgroundColor=\'#efefef\';" onmouseout="this.style.backgroundColor=\'#ffffff\';"><td><a href="/topic/' + url_pas(data[0]) + '/sub/' + url_pas(data[2]) + '#' + data[1] + '">' + '#' + data[1] + ' ' + sub + '</a> (' + '<a href="/w/' + url_pas(title) + '">' + title + '</a>)</td>'
        #div += '<tr style="line-height:30px" onmouseover="this.style.backgroundColor=\'#efefef\';" onmouseout="this.style.backgroundColor=\'#ffffff\';"><td><a href="/topic/' + url_pas(data[0]) + '/sub/' + url_pas(data[2]) + '#' + data[1] + '">' + title + '#' + data[1] + '</a> (' + sub + ')</td>'
        div += '<td>' + ip_pas(data[3]) + ban + '</td><td>' + data[4] + '</td></tr>'

    div += '</tbody></table>'
    div += next_fix('/topic_record/' + url_pas(name) + '?num=', num, data_list)      
    
    curs.execute("select end from ban where block = ?", [name])
    if curs.fetchall():
        sub = ' (' + load_lang('blocked') + ')'
    else:
        sub = 0 
    
    return easy_minify(flask.render_template(skin_check(), 
        imp = ['"' + ip_pas_raw(data[3]) + '" ' + '기여 목록', wiki_set(), custom(), other2([sub, 0])],
        data = div,
        menu = [['other', load_lang('other')], ['user', load_lang('user')], ['count/' + url_pas(name), load_lang('count')], ['record/' + url_pas(name), load_lang('record')]]
    ))