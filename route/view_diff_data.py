from .tool.func import *

def view_diff_data_2(conn, name):
    curs = conn.cursor()

    if acl_check(name, 'render') == 1:
        return re_error('/error/3')

    first = flask.request.args.get('olderrev', '1')
    second = flask.request.args.get('rev', '1')

    curs.execute("select data from history where id = ? and title = ?", [first, name])
    first_raw_data = curs.fetchall()
    curs.execute("select data from history where id = ? and title = ?", [second, name])
    second_raw_data = curs.fetchall()
    if not first_raw_data:
        first_raw_data = ''
    else:
        first_raw_data = html.escape(first_raw_data[0][0])
    if not second_raw_data:
        second_raw_data = ''
    else:
        second_raw_data = html.escape(second_raw_data[0][0])


    content = '''
        <input type=hidden id=contextSize value="5">
        <input type=hidden id=rev value="''' + second + '''">
        <input type=hidden id=olderrev value="''' + first + '''">
        <div id=diffoutput></div>
        <textarea id=baseText style="display: none;">''' + first_raw_data + '''</textarea>
        <textarea id=newText style="display: none;">''' + second_raw_data + '''</textarea>
        <script>
            $(function() {
                diffUsingJS(1);
            });
        </script>
    '''

    return easy_minify(flask.render_template(skin_check(),
            imp = [name, wiki_set(), custom(), other2([' (' + load_lang('compare') + ')', 0])],
            data = content,
            menu = [['history/' + url_pas(name), load_lang('return')]],
            st = 0
        ))

    curs.execute("select data from history where id = ? and title = ?", [first, name])
    first_raw_data = curs.fetchall()
    if first_raw_data:
        curs.execute("select data from history where id = ? and title = ?", [second, name])
        second_raw_data = curs.fetchall()
        if second_raw_data:
            first_data = html.escape(first_raw_data[0][0])
            second_data = html.escape(second_raw_data[0][0])

            if first == second:
                result = '-'
            else:
                diff_data = difflib.SequenceMatcher(None, first_data, second_data)
                result = re.sub('\r', '', diff(diff_data))

            return easy_minify(flask.render_template(skin_check(),
                imp = [name, wiki_set(), custom(), other2([' (' + load_lang('compare') + ')', 0])],
                data = '<pre>' + result + '</pre>',
                menu = [['history/' + url_pas(name), load_lang('return')]],
                st = 0
            ))

    return redirect('/history/' + url_pas(name))