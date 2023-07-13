from .tool.func import *

def list_title_index_2(conn):
    curs = conn.cursor()

    page = int(number_check(flask.request.args.get('page', '1')))
    num = int(number_check(flask.request.args.get('num', '100')))
    if page * num > 0:
        sql_num = page * num - num
    else:
        sql_num = 0

    all_list = sql_num + 1

    if num > 1000:
        return showError("너무 큽니다.")

    data = '''<ol class="breadcrumb link-nav">
                <li><a href="?num=100">[100개]</a></li>
                <li><a href="?num=250">[250개]</a></li>
                <li><a href="?num=500">[500개]</a></li>
                <li><a href="?num=1000">[1000개]</a></li>
               </ol>'''

    curs.execute("select title from data order by title asc limit ?, ?", [str(sql_num), str(num)])
    title_list = curs.fetchall()

    for list_data in title_list:
        data += '<li>' + str(all_list) + '. <a href="/w/' + url_pas(list_data[0]) + '">' + list_data[0] + '</a></li>'
        all_list += 1

    if page == 1:
        count_end = []

        curs.execute("select count(title) from data")
        count = curs.fetchall()
        if count:
            count_end += [count[0][0]]
        else:
            count_end += [0]

        sql_list = ['틀:', '분류:', '사용자:', '파일:']
        for sql in sql_list:
            curs.execute("select count(title) from data where title like ?", [sql + '%'])
            count = curs.fetchall()
            if count:
                count_end += [count[0][0]]
            else:
                count_end += [0]

        count_end += [count_end[0] - count_end[1]  - count_end[2]  - count_end[3]  - count_end[4]]

        data += '''
                </ul>
                <hr class=\"main_hr\">
                <ul>
                    <li>전체 ''' + str(count_end[0]) + '''개 문서</li>
                </ul>
                <hr class=\"main_hr\">
                <ul>
                    <li>''' + load_lang('template') + ': ' + str(count_end[1]) + '''</li>
                    <li>''' + load_lang('category') + ': ' + str(count_end[2]) + '''</li>
                    <li>''' + load_lang('user') + ': ' + str(count_end[3]) + '''</li>
                    <li>''' + load_lang('file') + ': ' + str(count_end[4]) + '''</li>
                    <li>기타: ''' + str(count_end[5]) + '''</li>
                '''

    data += '</ul>' + next_fix('?num=' + str(num) + '&page=', page, title_list, num)
    sub = ' (' + str(num) + ')'

    return easy_minify(flask.render_template(skin_check(),
        imp = [load_lang('all_document_list'), wiki_set(), custom(), other2([0, 0])],
        data = data,
        menu = [['other', load_lang('return')]]
    ))
