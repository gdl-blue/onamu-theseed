from .tool.func import *

def search_deep_2(conn, name):
    curs = conn.cursor()
    cnt = 0
    if name == '':
        return redirect()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0

    div = '<ul>'
    
    div_plus = ''
    test = ''
    
    curs.execute("select title from data where title = ?", [name])
    if curs.fetchall():
        link_id = ''
    else:
        link_id = 'id="not_thing"'
    
    div =   '''
            <div class="alert alert-info search-help" role="alert" style="padding:0.5rem 0.8rem;color:#31708f;background-color:#d9edf7;border-color:#bcdff1;padding-right: 30px;padding:10px;margin-bottom:1rem;border:1px solid #bcdff1;border-radius:.25rem;">
<div class="pull-left">
<span class="icon ion-chevron-right"></span>&nbsp;
찾는 문서가 없나요? 문서로 바로 갈 수 있습니다.
</div>
<div class="pull-right">
<button onclick="location.href = \'/w/''' + url_pas(name) + '''\';" type="button" style="padding: 0.25rem 0.5rem;font-size: 0.875rem;">\'''' + name + '''\' 문서로 가기</button>
</div>
<div style="clear: both;"></div>
</div>
'''
    div_plus += '<ul>'
            

    curs.execute(
        "select distinct title, case when title like ? then '제목' else '내용' \
        end from data where title like ? or data like ? order by case \
        when title like ? then 1 else 2 end limit ?, '50'",
        ['%' + name + '%', '%' + name + '%', '%' + name + '%', '%' + name + '%', str(sql_num)]
    )
    all_list = curs.fetchall()
    if all_list:
        test = all_list[0][1]
        
        for data in all_list:
            if data[1] != test:
                div_plus += '</ul><hr class=\"main_hr\"><ul>'
                
                test = data[1]
            if re.search("^더미:([^/]*)", data[0]):
                dsfadfsd = 1
            else:
                cnt = cnt + 1
                div_plus += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a> (' + data[1] + ')</li>'

    div += '전체 ' + str(cnt) + ' 건<br>' + div_plus + '</ul>'
    div += next_fix('/search/' + url_pas(name) + '?num=', num, all_list)

    return easy_minify(flask.render_template(skin_check(), 
        imp = [name, wiki_set(), custom(), other2([' (' + load_lang('search') + ')', 0])],
        data = div,
        menu = 0
    ))