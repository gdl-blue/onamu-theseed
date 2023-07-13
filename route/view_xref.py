from .tool.func import *

def view_xref_2(conn, name):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0

    curs.execute("select link, type from back where title = ? and not type = 'cat' and not type = 'no' order by link asc limit ?, '50'", [name, str(sql_num)])
    data_list = curs.fetchall()

    ns = flask.request.args.get('namespace', '')
    typ = flask.request.args.get('flag', '0')

    nsopt = ''

    div = '''<fieldset class="recent-option">
                <form class="form-inline" method="get">
                    <div class="form-group">
                        <label class="control-label">이름공간 :</label>
                        <select class="form-control" name="namespace">
                            <option value="전체" selected="">(전체)</option>
                        </select>
                        <select class="form-control" name="flag">
                            <option value="all">(전체)</option>
                            <option value="link">link</option>
                            <option value="file">file</option>
                            <option value="include">include</option>
                            <option value="redirect">redirect</option>
                        </select>
                    </div>
                    <div class="form-group btns">
                        <button type="submit" class="btn btn-primary" style="width: 5rem;">제출</button>
                    </div>
                </form>
            </fieldset>'''

    div += next_fix('/xref/' + url_pas(name) + '?num=', num, data_list) + '<ul>'

    for data in data_list:
        if flask.request.args.get('flag', 'all') != 'all':
            if data[1]:
                if data[1] == flask.request.args.get('flag', '') or (flask.request.args.get('flag', '') == 'link' and data[1] == ''):
                    div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a>'
            if flask.request.args.get('flag', '') == 'link':
                if not(data[1]):
                    div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a>'
        else:
            div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a>'

        if flask.request.args.get('flag', 'all') != 'all':
            if data[1]:
                if data[1] == flask.request.args.get('flag', ''):
                    div += ' (' + data[1] + ')'
            else:
                div += ' (link)'
        else:
            if not(data[1]):
                div += ' (link)'

        curs.execute("select title from back where title = ? and type = 'include'", [data[0]])
        db_data = curs.fetchall()
        if db_data:
            div += ' <a id="inside" href="/xref/' + url_pas(data[0]) + '">(' + load_lang('backlink') + ')</a>'

        div += '</li>'

    div += '</ul>' + next_fix('/xref/' + url_pas(name) + '?num=', num, data_list)

    return easy_minify(flask.render_template(skin_check(),
        imp = [name, wiki_set(), custom(), other2(['의 ' + load_lang('backlink'), 0])],
        data = div,
        menu = [['w/' + url_pas(name), load_lang('return')]],
        st = 6,
        smsub = ' (역링크)'
    ))