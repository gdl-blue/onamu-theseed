from .tool.func import *

def list_please_2(conn):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0
    ns = flask.request.args.get('namespace', '')
    if ns == '문서' or ns == '':
        curs.execute("select distinct title from back where type = 'no' and not title like '%:%'order by title asc limit ?, '50'", [str(sql_num)])
    else:
        curs.execute("select distinct title from back where type = 'no' and title like ? || ':%' order by title asc limit ?, '50'", [ns, str(sql_num)])
    data_list = curs.fetchall()

    div = '''<fieldset class="recent-option">
                <form class="form-inline">
                <div class="form-group">
                <label class="control-label">이름공간 :</label>
                <select class="form-control" id="namespace">
                ''' + getNamespaces('as combobox options') + '''
                </select>
                <script>document.getElementById('namespace').value = \'''' + flask.request.args.get('namespace', '문서') + '''\';</script>
                </div>
                <div class="form-group btns">
                <button type="button" class="btn btn-primary" style="width: 5rem;" onclick="location.href = '/NeededPages?namespace=' + document.getElementById('namespace').value; ">제출</button>
                </div>
                </form>
                </fieldset><p>역 링크는 존재하나 아직 작성이 되지 않은 문서 목록입니다.</p>
    <p>이 페이지는 하루에 한번 업데이트 됩니다.</p>''' + next_fix('/NeededPages?num=', num, data_list) + '''<ul class=wiki-list>'''
    var = ''


    for data in data_list:
        if var != data[0]:
            div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a> <a href="/xref/' + url_pas(data[0]) + '">[역링크]</a></li>'

            var = data[0]

    div += '</ul>' + next_fix('/NeededPages?num=', num, data_list)

    return easy_minify(flask.render_template(skin_check(),
        imp = ['작성이 필요한 문서', wiki_set(), custom(), other2([0, 0])],
        data = div,
        menu = [['other', load_lang('return')]]
    ))

def list_orf_2(conn):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0

    ns = flask.request.args.get('namespace', '')
    if ns == '문서' or ns == '':
        curs.execute("select title from data where not title like '%:%' order by title limit ?, '50'", [str(sql_num)])
    else:
        curs.execute("select title from data where title like ? || ':%' order by title limit ?, '50'", [ns, str(sql_num)])
    data_list = curs.fetchall()

    div = '''
    <fieldset class="recent-option">
                <form class="form-inline">
                <div class="form-group">
                <label class="control-label">이름공간 :</label>
                <select class="form-control" id="namespace">
                ''' + getNamespaces('as combobox options') + '''
                </select>
                <script>document.getElementById('namespace').value = \'''' + flask.request.args.get('namespace', '문서') + '''\';</script>
                </div>
                <div class="form-group btns">
                <button type="button" class="btn btn-primary" style="width: 5rem;" onclick="location.href = '/OrphanedPages?namespace=' + document.getElementById('namespace').value; ">제출</button>
                </div>
                </form>
                </fieldset><p>다음은 [[<a href="/w/''' + wiki_set()[0] + ''':대문">''' + wiki_set()[0] + ''':대문</a>]]에서 링크로 도달할 수 없는 문서로, 역링크가 없거나 자기네들끼리만 링크가 되어 있는 경우입니다.</p>
    <p>이 페이지는 하루에 한번 업데이트 됩니다.</p>''' + next_fix('/OrphanedPages?num=', num, data_list) + '''
    <ul class=wiki-list>'''
    var = ''


    for data in data_list:
        curs.execute("select title from back where title = ?", [data[0]])
        if not(curs.fetchall()):
            div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a> <a href="/xref/' + url_pas(data[0]) + '">[역링크]</a></li>'

    div += '</ul>' + next_fix('/OrphanedPages?num=', num, data_list)

    return easy_minify(flask.render_template(skin_check(),
        imp = ['고립된 문서', wiki_set(), custom(), other2([0, 0])],
        data = div,
        menu = [['other', load_lang('return')]]
    ))

def list_unc_2(conn):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0

    ns = flask.request.args.get('namespace', '')
    if ns == '문서' or ns == '':
        curs.execute("select title from data where not title like '%:%' order by title limit ?, '50'", [str(sql_num)])
    else:
        curs.execute("select title from data where title like ? || ':%' order by title limit ?, '50'", [ns, str(sql_num)])
    data_list = curs.fetchall()

    div = '''
    <fieldset class="recent-option">
                <form class="form-inline">
                <div class="form-group">
                <label class="control-label">이름공간 :</label>
                <select class="form-control" id="namespace">
                ''' + getNamespaces('as combobox options') + '''
                </select>
                <script>document.getElementById('namespace').value = \'''' + flask.request.args.get('namespace', '문서') + '''\';</script>
                </div>
                <div class="form-group btns">
                <button type="button" class="btn btn-primary" style="width: 5rem;" onclick="location.href = '/UncategorizedPages?namespace=' + document.getElementById('namespace').value; ">제출</button>
                </div>
                </form>
                </fieldset>''' + next_fix('/UncategorizedPages?num=', num, data_list) + '''
    <ul class=wiki-list>'''
    var = ''


    for data in data_list:
        curs.execute("select link from back where link = ? and type = 'cat'", [data[0]])
        if not(curs.fetchall()):
            div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a></li>'

    div += '</ul>' + next_fix('/UncategorizedPages?num=', num, data_list)

    return easy_minify(flask.render_template(skin_check(),
        imp = ['분류가 되지 않은 문서', wiki_set(), custom(), other2([0, 0])],
        data = div,
        menu = [['other', load_lang('return')]]
    ))

def list_old_2(conn):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0

    curs.execute("select title, data, date from data order by date asc limit ?, '50'", [str(sql_num)])
    data_list = curs.fetchall()

    div = '''
    <p>편집된 지 오래된 문서의 목록입니다. (리다이렉트 제외)
    </p>''' + next_fix('/OldPages?num=', num, data_list) + '''
    <ul class=wiki-list>'''
    var = ''

    for data in data_list:
        if re.search('^#redirect ', data[1]) or re.search('^#넘겨주기 ', data[1]):
            continue
        ddd = data[2].split(' ')[0]
        try:
            ttt = data[2].split(' ')[1]
        except:
            ttt = '00:00:00'

        div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a> (수정 시각:<time datetime="' + ddd + 'T' + ttt + '.000Z" data-format="Y-m-d H:i:s">' + data[2] + '</time>)</li>'

    div += '</ul>' + next_fix('/OldPages?num=', num, data_list)

    return easy_minify(flask.render_template(skin_check(),
        imp = ['편집된 지 오래된 문서', wiki_set(), custom(), other2([0, 0])],
        data = div,
        menu = [['other', load_lang('return')]]
    ))

def list_short_2(conn):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0

    curs.execute("select title, data from data where not title like '%:%' order by length(data) asc limit ?, '50'", [str(sql_num)])
    data_list = curs.fetchall()

    div = '''
    <p>내용이 짧은 문서 (문서 이름공간, 리다이렉트 제외)
    </p>''' + next_fix('/ShortestPages?num=', num, data_list) + '''
    <ul class=wiki-list>'''
    var = ''

    for data in data_list:
        if re.search('^#redirect ', data[1]) or re.search('^#넘겨주기 ', data[1]):
            continue

        div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a> (' + str(len(data[1])) + '글자)</li>'

    div += '</ul>' + next_fix('/ShortestPages?num=', num, data_list)

    return easy_minify(flask.render_template(skin_check(),
        imp = ['내용이 짧은 문서', wiki_set(), custom(), other2([0, 0])],
        data = div,
        menu = [['other', load_lang('return')]]
    ))

def list_long_2(conn):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0

    curs.execute("select title, data from data where not title like '%:%' order by length(data) desc limit ?, '50'", [str(sql_num)])
    data_list = curs.fetchall()

    div = next_fix('/LongestPages?num=', num, data_list) + '''
    <ul class=wiki-list>'''
    var = ''

    for data in data_list:
        if re.search('^#redirect ', data[1]) or re.search('^#넘겨주기 ', data[1]):
            continue

        div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a> (' + str(len(data[1])) + '글자)</li>'

    div += '</ul>' + next_fix('/LongestPages?num=', num, data_list)

    return easy_minify(flask.render_template(skin_check(),
        imp = ['내용이 긴 문서', wiki_set(), custom(), other2([0, 0])],
        data = div,
        menu = [['other', load_lang('return')]]
    ))