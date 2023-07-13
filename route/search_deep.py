from .tool.func import *
import datetime

def search_deep_2(conn, name):
    curs = conn.cursor()
    query = name

    if query == "아기공룡 둘리는 초능력 내친구":
        flask.session['easteregg1'] = 1

    #와일드카드
    query = re.sub('[?]', '_', query)
    query = re.sub('[*]', '%', query)

    if re.search('^\s', query) or re.search('\s$', query) or query == '':
        return showError('searchd_fail')
    bet = datetime.datetime.today()

    num = int(number_check(flask.request.args.get('page', '1')))
    if num * 10 > 0:
        sql_num = num * 10 - 10
    else:
        sql_num = 0

    content = '''
        <div class="alert alert-info search-help" role="alert">
            <div class="pull-left">
                <span class="icon ion-chevron-right"></span>&nbsp;
                찾는 문서가 없나요? 문서로 바로 갈 수 있습니다.
            </div>
            <div class="pull-right">
                <a href="/w/''' + url_pas(name) + '''" class="btn btn-secondary btn-sm">\'''' + html.escape(name) + '''\' 문서로 가기</a>
            </div>
            <div style="clear: both;"></div>
        </div>
    '''

    sByTitle = 0
    sByContent = 0
    curs.execute("select count(title) from data where title like '%' || ? || '%'", [query])
    sByTitle = curs.fetchall()
    if sByTitle:
        sByTitle = int(sByTitle[0][0])
    curs.execute("select count(title) from data where data like '%' || ? || '%'", [query])
    sByContent = curs.fetchall()
    if sByContent:
        sByContent = int(sByContent[0][0])

    resultList = '<section class=search-section>'

    # SQL에서 '문자열1 || 문자열 2'은 파이선/VB/JS 등에서 '문자열1 + 문자열2'와 같음
    curs.execute("select title, data from data where title like '%' || ? || '%' limit ?, '10'", [query, sql_num])
    tlist = curs.fetchall()

    curs.execute("select title, data from data where data like '%' || ? || '%' limit ?, '10'", [query, sql_num])
    clist = curs.fetchall()

    for i in tlist:
        scontent = i[1][i[1].find(query)-250:i[1].find(query)+ 250]
        resultList += '''
            <div class="search-item">
                <h4>
                    <i class="ion-document"></i>
                    <a href="/w/''' + url_pas(i[0]) + '''">
                        ''' + html.escape(i[0]) + '''
                    </a>
                </h4>
                <div>
                    ''' + html.escape(scontent).replace(query, '<span class="search-highlight">' + query + '</span>') + '''
                </div>
            </div>
        '''
    for i in clist:
        scontent = i[1][i[1].find(query)-250:i[1].find(query)+ 250]
        resultList += '''
            <div class="search-item">
                <h4>
                    <i class="ion-document"></i>
                    <a href="/w/''' + url_pas(i[0]) + '''">
                        ''' + html.escape(i[0]) + '''
                    </a>
                </h4>
                <div>
                    ''' + html.escape(scontent).replace(query, '<span class="search-highlight">' + query + '</span>') + '''
                </div>
            </div>
        '''

    resultList += '''
        <nav class="pull-right">
        <ul class="pagination">
        <li class="page-item"><a class="page-link" href="?page=''' + str(num - 1) + '''">&lt;</a></li>
    '''

    curs.execute("select title, data from data where title like '%' || ? || '%'", [query])
    tlist2 = curs.fetchall()

    curs.execute("select title, data from data where data like '%' || ? || '%'", [query])
    clist2 = curs.fetchall()

    for i in range(1, int((sByTitle + sByContent) / 20) + 2):
        if i > 10:
            break

        if i == num:
            resultList += '<li class="page-item active"><a class="page-link" href="?page=' + str(i) + '">' + str(i) + '</a></li>'
        else:
            resultList += '<li class="page-item"><a class="page-link" href="?page=' + str(i) + '">' + str(i) + '</a></li>'

    resultList += '<li class="page-item"><a class="page-link" href="?page=' + str(num + 1) + '">&gt;</a></li></ul></nav></section>'

    aet = datetime.datetime.today()

    searchSummary = '<div class=search-summary>전체 ' + str(sByTitle + sByContent) + ' 건 / 처리 시간 ' + str(round((aet - bet).total_seconds(), 3)) + '초</div>'

    content = content + searchSummary + resultList


    return easy_minify(flask.render_template(skin_check(),
        imp = ['"' + name + '"', wiki_set(), custom(), other2([' 검색 결과', 0])],
        data = content,
        menu = 0
    ))

def search_deep__onamu_2(conn, name):
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
        link_id = 'class="wiki-link-internal"'
    else:
        link_id = 'class="wiki-link-internal not-exist"'

    div =   '''
            <div class="alert alert-info search-help" role="alert" style="padding:0.5rem 0.8rem;color:#31708f;background-color:#d9edf7;border-color:#bcdff1;padding-right: 30px;padding:10px;margin-bottom:1rem;border:1px solid #bcdff1;border-radius:.25rem;">
<div class="pull-left">
<span class="icon ion-chevron-right"></span>&nbsp;
찾는 문서가 없나요? 문서로 바로 갈 수 있습니다.
</div>
<div class="pull-right">
<a href="/w/''' + url_pas(name) + '''" class="btn btn-secondary btn-sm">\'''' + name + '''\' 문서로 가기</button>
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
        imp = ['"' + name + '"', wiki_set(), custom(), other2([' ' + load_lang('search') + ' 결과', 0])],
        data = div,
        menu = 0
    ))

def searchAutoComplete(conn, name):
    curs = conn.cursor()

    jdata = ''

    curs.execute("select title from data where title like ? || '%'", [name])
    for resultData in curs.fetchall():
        jdata += ',"' + resultData[0] + '"'

    jdata = re.sub('^[,]', '', jdata)

    return '[' + jdata + ']'