from .tool.func import *

def main_file_2(conn, data):
    curs = conn.cursor()

    if re.search('\.txt$', data):
        return flask.send_from_directory('./', data)
    elif data == 'onamu-theseed.zip':
        if ip_check() == '':
            return flask.send_from_directory('./', data)
        else:
            return 'invalid'
    else:
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

def cap_img_2(conn, ci):
    return flask.send_from_directory('./cat', ci)