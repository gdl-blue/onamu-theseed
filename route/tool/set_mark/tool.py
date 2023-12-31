import flask
import urllib.parse
import datetime
import re
import hashlib

def get_time():
    return str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))

def ip_check(d_type = 0):
    if d_type == 0:
        if flask.session and ('state' and 'id') in flask.session:
            ip = flask.session['id']
        else:
            try:
                ip = flask.request.environ.get('HTTP_X_REAL_IP', flask.request.environ.get('HTTP_X_FORWARDED_FOR', flask.request.remote_addr))

                if ip == ('::1' or '127.0.0.1'):
                    ip = flask.request.environ.get('HTTP_X_FORWARDED_FOR', flask.request.remote_addr)
            except:
                ip = '-'
    else:
        try:
            ip = flask.request.environ.get('HTTP_X_REAL_IP', flask.request.environ.get('HTTP_X_FORWARDED_FOR', flask.request.remote_addr))

            if ip == ('::1' or '127.0.0.1'):
                ip = flask.request.environ.get('HTTP_X_FORWARDED_FOR', flask.request.remote_addr)
        except:
            ip = '-'

    return str(ip)

def my_ip():
    try:
        ip = flask.request.environ.get('HTTP_X_REAL_IP', flask.request.environ.get('HTTP_X_FORWARDED_FOR', flask.request.remote_addr))

        if ip == ('::1' or '127.0.0.1'):
            ip = flask.request.environ.get('HTTP_X_FORWARDED_FOR', flask.request.remote_addr)
    except:
        ip = '-'

    return str(ip)

def perms_has(permname):
    perm = permname
    if perm == 'update_thread_status':
        perm = 'uts'
    elif perm == 'update_thread_topic':
        perm = 'utt'
    elif perm == 'update_thread_document':
        perm = 'utd'
    elif perm == 'delete_thread':
        perm = 'dt'
    elif perm == 'editable_other_user_document':
        perm = 'eou'

    curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), perm])

    if curs.fetchall():
        return True
    else:
        return None

def savemark(data):
    data = re.sub("\[date\(now\)\]", get_time(), data)

    ip = ip_check()
    if not re.search("\.", ip):
        name = '[[파일:' + ip + '|' + ip + ']]'
    else:
        name = ip

    data = re.sub("\[name\]", name, data)

    return data

def url_pas(data):
    return urllib.parse.quote(data).replace('/','%2F')

def sha224(data):
    return hashlib.sha224(bytes(data, 'utf-8')).hexdigest()

def md5_replace(data):
    return hashlib.md5(data.encode()).hexdigest()