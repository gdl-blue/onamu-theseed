from .tool.func import *

def func_title_random_2(conn):
    curs = conn.cursor()
    data = [[0]]
    curs.execute("select title from data order by random() limit 1")
    data = curs.fetchall()
    if data:
        while (re.search('^사용자:([^/]*)', data[0][0]) or re.search('^분류:([^/]*)', data[0][0]) or re.search('^파일:([^/]*)', data[0][0]) or re.search('^틀:([^/]*)', data[0][0]) or re.search('^더미:([^/]*)', data[0][0])):
            curs.execute("select title from data order by random() limit 1")
            data = curs.fetchall()

    if data:
        return redirect('/w/' + url_pas(data[0][0]))
    else:
        return redirect()

def randompage_2(conn):
    curs = conn.cursor()
    div = ''
    ns = flask.request.args.get('namespace', '')
    if ns == '문서' or ns == '':
        curs.execute("select title from data where not title like '%:%' order by random() limit 20")
    else:
        curs.execute("select title from data where title like ? || ':%' order by random() limit 20", [ns])

    for i in curs.fetchall():
        div += '<li><a href="/w/' + url_pas(i[0]) + '">' + i[0] + '</a></li>'

    if 3 == 3:
        return easy_minify(flask.render_template(skin_check(),
            imp = ['RandomPage', wiki_set(), custom(), other2([0, 0])],
            data = '''<fieldset class="recent-option">
                <form class="form-inline">
                <div class="form-group">
                <label class="control-label">이름공간 :</label>
                <select class="form-control" id="namespace">
                ''' + getNamespaces('as combobox options') + '''
                </select>
                <script>document.getElementById('namespace').value = \'''' + flask.request.args.get('namespace', '문서') + '''\';</script>
                </div>
                <div class="form-group btns">
                <button type="button" class="btn btn-primary" style="width: 5rem;" onclick="location.href = '/RandomPage?namespace=' + document.getElementById('namespace').value; ">제출</button>
                </div>
                </form>
                </fieldset><ul>''' + div + '''</ul>''',
            menu = 0
        ))