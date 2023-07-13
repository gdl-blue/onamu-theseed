from .tool.func import *

def ipacl_2(conn):
    curs = conn.cursor()
    name = None
    if name and ip_or_user(name) == 0:
        curs.execute("select acl from user where id = ?", [name])
        user = curs.fetchall()
        if not user:
            return re_error('/error/2')

        if user and user[0][0] != 'user':
            if admin_check() != 1:
                return re_error('/error/4')

    #if ban_check(ip = ip_check(), tool = 'login') == 1:
        #return re_error('/ban')
                
    if flask.request.method == 'POST':
        name = name if name else flask.request.form.get('name', 'test')

        if admin_check(1, 'ban' + ((' (' + name + ')') if name else '')) != 1:
            return re_error('/error/3')

        end = flask.request.form.get('second', '0')
        end = end if end else '0'

        if flask.request.form.get('regex', None):
            type_d = 'regex'

            try:
                re.compile(name)
            except:
                return re_error('/error/23')
        else:
            type_d = None

        ban_insert(
            name, 
            flask.request.form.get('second', '0'), 
            flask.request.form.get('why', ''), 
            flask.request.form.get('login', ''), 
            ip_check(),
            type_d
        )

        return redirect('/suspend_account')     
    else:
        if admin_check(1) != 1:
            return re_error('/error/3')

        curs.execute("select end, why from ban where block = ?", [name])
        end = curs.fetchall()
        if end:
            main_name = name
            b_now = load_lang('release')
            now = '(' + b_now + ')'

            if end[0][0] == '':
                data = '<ul><li>' + load_lang('limitless') + '</li>'
            else:
                data = '<ul><li>' + load_lang('period') + ' : ' + end[0][0] + '</li>'
                
            curs.execute("select block from ban where block = ? and login = 'O'", [name])
            if curs.fetchall():
                data += '<li>' + load_lang('login_able') + '</li>'

            if end[0][1] != '':
                data += '<li>' + load_lang('why') + ' : ' + end[0][1] + '</li></ul><hr class=\"main_hr\">'
            else:
                data += '</ul><hr class=\"main_hr\">'
        else:
            if name:
                main_name = name
                
                if name and re.search("^([0-9]{1,3}\.[0-9]{1,3})$", name):
                    b_now = load_lang('band_ban')
                else:
                    b_now = load_lang('ban')

                now = ' (' + b_now + ')'
                    
                if name and ip_or_user(name) == 1:
                    plus = load_lang('login_able') + ' : <input type="checkbox" name="login"> Yes'
                else:
                    plus = ''

                name += '<hr class=\"main_hr\">'
                regex = ''
            else:
                main_name = load_lang('ban')
                name = '유저 이름 : <br><input name="name" type="text">'
                regex = '<input type="checkbox" name="regex"> ' + load_lang('regex')
                plus = load_lang('login_able') + ' : <input type="checkbox" name="login"> Yes'
                now = 0
                b_now = load_lang('ban')
                
            time_data = [
                ['0', '영구'],
                ['-1', '해제'],
                ['60', '1분'],
                ['300', '5분'],
                ['600', '10분'],
                ['1800', '30분'],
                ['3600', '1시간'],
                ['7200', '2시간'],
                ['86400', '하루'],
                ['259200', '3일'],
                ['432000', load_lang('5_day')],
                ['604800', '7일'],
                ['1209600', '2주'],
                ['1814400', '3주'],
                ['2592000', '1개월'],
                ['15552000', '6개월'],
                ['31104000', '1년']
            ]
            insert_data = ''
            combo = ''
            for i in time_data:
                insert_data += '<a href="javascript:insert_v(\'second\', \'' + i[0] + '\')">(' + i[1] + ')</a> '
            for i in time_data:
                combo += '<option value="' + i[0] + '">' + i[1] + '</option>'
            # 언어 적용 필요
#<input placeholder="''' + load_lang('ban_period') + ''' (''' + load_lang('second') + ''')" name="second" id="second" type="text">
#<script>function insert_v(name, data) { document.getElementById(name).value = data; }</script>''' + insert_data + ''' 
            data = name + '''
                <br><br>
                차단 기간 : <br>
                <select name="second" id="second" style="width: 100%">
                    ''' + combo + '''
                </select>
                
                
                <br><br>메모 : <br><input name="why" type="text">
            ''' + plus

        return easy_minify(flask.render_template(skin_check(), 
            imp = ['사용자 ' + main_name, wiki_set(), custom(), other2([now, 0])],
            data = '''
                <form method="post">
                    ''' + data + '''
                    <br><br><button type="submit" style="color:#fff;    width:120px;    background-color: #5bc0de; border-color: #5bc0de;display: inline-block;font-weight: 400; line-height: 1.25;text-align: center;   white-space: nowrap;vertical-align: middle;user-select: none; border: 1px solid transparent;   padding: .5rem 1rem;    font-size: 1rem;   border-radius: .25rem;    transition: all .2s ease-in-out;">확인</button>
                </form>
            ''',
            menu = 0
        ))   