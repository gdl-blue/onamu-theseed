from .tool.func import *

def give_user_check_2(conn, name):
    curs = conn.cursor()

    curs.execute("select acl from user where id = ? or id = ?", [name, flask.request.args.get('plus', '-')])
    user = curs.fetchall()
    if user and user[0][0] != 'user':
        if admin_check(4) != 1:
            return re_error('/error/3')

    if admin_check(4, 'check (' + name + ')') != 1:
        return re_error('/error/3')

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0

    oyd = (datetime.datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")

    curs.execute("delete from ua_d where today < ?", [oyd])

    curs.execute("select name, ip, ua, today from ua_d where name = ? COLLATE NOCASE order by today desc limit ?, '50'", [name, sql_num])

    record = curs.fetchall()
    if not(record):
        record = [[]]

    if not flask.request.args.get('plus', None):
        dfdsaf = ''
        #div = '<a href="/manager/14?plus=' + url_pas(name) + '">(' + load_lang('compare') + ')</a><hr class=\"main_hr\">'
    else:
        dsfdsg = ''
        #div = '<a href="/check/' + url_pas(name) + '">(' + name + ')</a> <a href="/check/' + url_pas(flask.request.args.get('plus', None)) + '">(' + flask.request.args.get('plus', None) + ')</a><hr class=\"main_hr\">'
    ua = ''
    div = ''
    div +=  '''<div class=wiki-table-wrap>
            <table class="wiki-table">
                <tbody>
                    <tr>
                        <th>Date</th>
                        <th>IP</th>
                    </tr>
            '''

    for data in record:
        try:
            if data[2]:
                ua = data[2]
            else:
                ua = '<br>'
        except:
            return showError('사용자가 존재하지 않습니다.')

        div +=  '''
                <tr>
                    <td>''' + data[3] + '''</td>
                    <td>''' + data[1] + '''</td>
                </tr>

                '''
    curs.execute("select data from user_set where name = 'email' and id = ? COLLATE NOCASE", [name])
    try:
        userEmail = curs.fetchall()[0][0]
    except:
        userEmail = '없음'
    div = '''<p>마지막 로그인 UA : ''' + record[0][2] + '''</p><p>이메일 : ''' + userEmail + '''</p>''' + div

    div +=  '''
                </tbody>
            </table></div>
            '''

    div += next_fix('/admin/login_history/' + url_pas(name) + '?num=', num, record)

    ban_lh(
        data[0],
        'lh',
        '',
        'false',
        ip_check()
    )

    return easy_minify(flask.render_template(skin_check(),
        imp = [data[0] + ' 로그인 내역', wiki_set(), custom(), other2([0, 0])],
        data = div,
        menu = 0
    ))