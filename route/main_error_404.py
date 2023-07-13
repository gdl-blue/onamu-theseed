from .tool.func import *

def main_error_404_2(conn):
    curs = conn.cursor()

    # return re_error('/error/3000')
    return '''
<HEADER>
<title>Page is not found!</title>
<style>
section {
	position: fixed;
	top: 0;
	right: 0;
	bottom: 0;
	left: 0;
	padding: 80px 0 0;
	background-color:#EFEFEF;
	font-family: "Open Sans", sans-serif;
	text-align: center;
}
h1 {
	margin: 0 0 19px;
	font-size: 40px;
	font-weight: normal;
	color: #E02B2B;
	line-height: 40px;
}
p {
margin: 0 0 57px;
	font-size: 16px;
	color:#444;
	line-height: 23px;
}
</style>
</HEADER>
<section>
<h1>404</h1>
<p>Page is not found!<br><a href="/">Back to home</a></p>
</section>
    '''

def rtrt_2(conn):
    curs = conn.cursor()

    return redirect('/w/' + wiki_set(2))

def notav_2(conn):
    curs = conn.cursor()

    return re_error('/error/3001')

def sql_2(conn):
    curs = conn.cursor()



    if flask.request.method == 'POST':
        if admin_check() != 1:
            return re_error('/error/3')
        return redirect("/SQLexec/" + pw_encode(flask.request.form.get('pin', 'x')))
    else:
        if admin_check() != 1:
            return re_error('/error/3')
        pin = ''.join(random.choice("0123456789BCVXSQRDFGTHNPK") for i in range(4))
        pin += '-'
        pin += ''.join(random.choice("0123456789BCVXSQRDFGTHNPK") for i in range(4))
        pin += '-'
        pin += ''.join(random.choice("0123456789BCVXSQRDFGTHNPK") for i in range(4))
        pin += '-'
        pin += ''.join(random.choice("0123456789BCVXSQRDFGTHNPK") for i in range(4))
        pin += '-'
        pin += ''.join(random.choice("0123456789BCVXSQRDFGTHNPK") for i in range(4))
        pin += '-'
        pin += ''.join(random.choice("0123456789BCVXSQRDFGTHNPK") for i in range(4))
        pin += '-'
        pin += ''.join(random.choice("0123456789BCVXSQRDFGTHNPK") for i in range(4))
        pin += '-'
        pin += ''.join(random.choice("0123456789BCVXSQRDFGTHNPK") for i in range(4))
        pin += '-'
        pin += ''.join(random.choice("0123456789BCVXSQRDFGTHNPK") for i in range(4))
        pin += '-'
        pin += ''.join(random.choice("0123456789BCVXSQRDFGTHNPK") for i in range(4))
        pin += '-'
        pin += ''.join(random.choice("0123456789BCVXSQRDFGTHNPK") for i in range(4))
        pin += '-'
        pin += ''.join(random.choice("0123456789BCVXSQRDFGTHNPK") for i in range(4))

        flask.session['exeid'] = ''.join(random.choice("0123456789BCVXSQRDFGTHNPKfdertyijklb") for i in range(64))

        flask.session['sqlpin'] = pin;

        print('SQL 실행에 사용할 암호(식별자 ' + flask.session['exeid'] + '): ' + pin)
        data = '''<form method=post>
            SQL 실행 PIN : <br>식별자 : ''' + flask.session['exeid'] + '''<br>
            <input type=text name=pin class=form-control><br><strong>[경고!]</strong> PIN 말고도 개발자 권한이 요구됩니다.<br>
            <button type=submit class="btn btn-info">확인</button>
            </form>
        '''

        return easy_minify(flask.render_template(skin_check(),
            imp = ['SQL 실행', wiki_set(), custom(), other2(['', 0])],
            data = data,
            menu = 0
        ))

def sqlexec_2(conn, key):
    curs = conn.cursor()

    if not('sqlpin' in flask.session):
        return re_error('/error/3')
    if key != pw_encode(flask.session['sqlpin']):
        return re_error('/error/3')

    if flask.request.method == 'POST':
        if not('sqlpin' in flask.session):
            return re_error('/error/3')
        if key != pw_encode(flask.session['sqlpin']):
            return re_error('/error/3')
        if admin_check() != 1:
            return re_error('/error/3')
        curs.execute(flask.request.form.get('cmd', ''))
        conn.commit();
        return redirect("/SQLexec/" + pw_encode(flask.session['sqlpin']))
    else:
        if admin_check() != 1:
            return re_error('/error/3')
        data = '''<form method=post>
            SQL 명령 : <br>
            <input type=text class=form-control name=cmd><br><strong>[경고!]</strong> 개발자 권한이 요구됩니다.<br>
            <button type=submit class="btn btn-info">확인</button>
            </form>
        '''

        return easy_minify(flask.render_template(skin_check(),
            imp = ['SQL 실행', wiki_set(), custom(), other2(['', 0])],
            data = data,
            menu = 0
        ))

def biaf(conn):
    curs = conn.cursor()

    return re_error('/error/99')