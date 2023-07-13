from .tool.func import *

def recent_discuss_2(conn):
    curs = conn.cursor()

    div = ''
    
    if flask.request.args.get('what', 'normal') == 'normal':
        div += '<div style="padding: .75rem 1rem;margin-bottom: 1rem;list-style: none;background-color: #eceeef;border-radius: .25rem;"><a href="/recent_discuss">[' + load_lang('open_discussion') + ']</a>　<a href="/recent_discuss?what=close">[' + load_lang('close_discussion') + ']</a></div>'
       
        m_sub = 0
    else:
        div += '<div style="padding: .75rem 1rem;margin-bottom: 1rem;list-style: none;background-color: #eceeef;border-radius: .25rem;"><a href="/recent_discuss">[' + load_lang('open_discussion') + ']</a>　<a href="/recent_discuss?what=close">[' + load_lang('close_discussion') + ']</a></div>'
        
        m_sub = ' [' + load_lang('closed') + ']'

    div +=  '''
           
            <table class="table table-hover" style="width:100%">
<colgroup>
<col>
<col style="width: 22%; min-width: 100px;">
</colgroup>
                <tbody>
                    <tr style="border-top:1px solid #eceeef;border-bottom:2px solid #eceeef;line-height:30px">
                        <td id="main_table_width"><b>''' + '항목' + '''</b></td>
                        <td id="main_table_width"><b>''' + '수정 시간' + '''</b></td>
                    </tr>
            '''
    
    if m_sub == 0:
        curs.execute("select title, sub, date from rd where not stop = 'O' order by date desc limit 50")
    else:
        curs.execute("select title, sub, date from rd where stop = 'O' order by date desc limit 50")
        
    for data in curs.fetchall():
        title = html.escape(data[0])
        sub = html.escape(data[1])

        div += '<tr style="line-height:30px" onmouseover="this.style.backgroundColor=\'#efefef\';" onmouseout="this.style.backgroundColor=\'#ffffff\';"><td><a href="/topic/' + url_pas(data[0]) + '/sub/' + url_pas(data[1]) + '">' + sub + '</a> (<a href="/topic/' + url_pas(title) + '">' + title + '</a>)</td><td>' + data[2] + '</td></tr>'
    
    curs.execute("select num, name, time from erq where state = 'open' order by time desc limit 25")
    for data in curs.fetchall():
        div += '<tr style="line-height:30px" onmouseover="this.style.backgroundColor=\'#efefef\';" onmouseout="this.style.backgroundColor=\'#ffffff\';"><td><a href="/edit_request/' + url_pas(data[0]) + '">편집 요청 ' + data[0] + '</a> (<a href="/topic/' + url_pas(data[1]) + '">' + data[1] + '</a>)</td><td>' + data[2] + '</td></tr>'
    
    div += '</tbody></table>'
            
    return easy_minify(flask.render_template(skin_check(), 
        imp = [load_lang('recent_discussion'), wiki_set(), custom(), other2([m_sub, 0])],
        data = div,
        menu = 0
    ))