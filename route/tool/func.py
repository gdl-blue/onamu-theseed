import os
import sys
import platform

import urllib

for i in range(0, 2):
    try:
        import werkzeug.routing
        import werkzeug.debug
        import flask_compress
        import flask_reggie
        import tornado.ioloop
        import tornado.httpserver
        import tornado.wsgi
        import urllib.request
        import email.mime.text
        import sqlite3
        import hashlib
        import smtplib
        import bcrypt
        import zipfile
        import difflib
        import shutil
        import request
        import threading
        import logging
        import random
        import flask
        import json
        import html
        import re

        try:
            import css_html_js_minify
        except:
            pass

        if sys.version_info < (3, 6):
            import sha3

        from .set_mark.tool import *
        from .mark import *
    except ImportError as e:
        if i == 0:
            if platform.system() == 'Linux':
                ok = os.system('python3 -m pip install --user -r requirements.txt')
                if ok == 0:
                    print('----')
                    os.execl(sys.executable, sys.executable, *sys.argv)
                else:
                    raise
            elif platform.system() == 'Windows':
                ok = os.system('python -m pip install --user -r requirements.txt')
                if ok == 0:
                    print('----')
                    os.execl(sys.executable, sys.executable, *sys.argv)
                else:
                    raise
            else:
                print('----')
                print(e)
                raise
        else:
            print('----')
            print(e)
            raise

app_var = json.loads(open('data/app_variables.json', encoding='utf-8').read())

def load_conn(data):
    global conn
    global curs

    conn = data
    curs = conn.cursor()

    load_conn2(data)

def send_email(who, title, data):
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    try:
        curs.execute('select name, data from other where name = "g_email" or name = "g_pass"')
        rep_data = curs.fetchall()
        if rep_data:
            g_email = ''
            g_pass = ''
            for i in rep_data:
                if i[0] == 'g_email':
                    g_email = i[1]
                else:
                    g_pass = i[1]

            smtp.login(g_email, g_pass)

        msg = email.mime.text.MIMEText(data)
        msg['Subject'] = title
        smtp.sendmail(g_email, who, msg.as_string())

        smtp.quit()
    except:
        print('----')
        print('Error : Email send error')

def last_change(data):
    json_address = re.sub("(((?!\.|\/).)+)\.html$", "set.json", skin_check())
    try:
        json_data = json.loads(open(json_address).read())
    except:
        json_data = 0

    if json_data != 0:
        for j_data in json_data:
            if "class" in json_data[j_data]:
                if "require" in json_data[j_data]:
                    re_data = re.compile("<((?:" + j_data + ")( (?:(?!>).)*)?)>")
                    s_data = re_data.findall(data)
                    for i_data in s_data:
                        e_data = 0

                        for j_i_data in json_data[j_data]["require"]:
                            re_data_2 = re.compile("( |^)" + j_i_data + " *= *[\'\"]" + json_data[j_data]["require"][j_i_data] + "[\'\"]")
                            if not re_data_2.search(i_data[1]):
                                re_data_2 = re.compile("( |^)" + j_i_data + "=" + json_data[j_data]["require"][j_i_data] + "(?: |$)")
                                if not re_data_2.search(i_data[1]):
                                    e_data = 1

                                    break

                        if e_data == 0:
                            re_data_3 = re.compile("<" + i_data[0] + ">")
                            data = re_data_3.sub("<" + i_data[0] + " class=\"" + json_data[j_data]["class"] + "\">", data)        
                else:
                    re_data = re.compile("<(?P<in>" + j_data + "(?: (?:(?!>).)*)?)>")
                    data = re_data.sub("<\g<in> class=\"" + json_data[j_data]["class"] + "\">", data)

    return data

def easy_minify(data, tool = None):
    try:
        if not tool:
            data = css_html_js_minify.html_minify(data)
        else:
            if tool == 'css':
                data = css_html_js_minify.css_minify(data)
            elif tool == 'js':
                data = css_html_js_minify.js_minify(data)
    except:
        data = re.sub('\n +<', '\n<', data)
        data = re.sub('>(\n| )+<', '> <', data)
    
    return last_change(data)

def render_set(title = '', data = '', num = 0, s_data = 0):
    if acl_check(title, 'render') == 1:
        return 'HTTP Request 401.3'
    elif s_data == 1:
        return data
    else:
        if data != None:
            return namumark(title, data, num)
        else:
            return 'HTTP Request 404'

def captcha_get():
    data = ''

    if custom()[2] == 0:
        curs.execute('select data from other where name = "recaptcha"')
        recaptcha = curs.fetchall()
        if recaptcha and recaptcha[0][0] != '':
            curs.execute('select data from other where name = "sec_re"')
            sec_re = curs.fetchall()
            if sec_re and sec_re[0][0] != '':
                data += recaptcha[0][0] + '<hr class=\"main_hr\">'

    return data

def update():
    # v3.0.8 rd, agreedis, stop 테이블 통합
    try:
        curs.execute("select title, sub, close from stop")
        for i in curs.fetchall():
            if i[2] == '':
                curs.execute("update rd set stop = 'S' where title = ? and sub = ?", [i[0], i[1]])
            else:
                curs.execute("update rd set stop = 'O' where title = ? and sub = ?", [i[0], i[1]])
    except:
        pass
        
    try:
        curs.execute("select title, sub from agreedis")
        for i in curs.fetchall():
            curs.execute("update rd set agree = 'O' where title = ? and sub = ?", [i[0], i[1]])
    except:
        pass
         
    try:
        curs.execute("drop table if exists stop")
        curs.execute("drop table if exists agreedis")
    except:
        pass

    # Start : Data migration code
    app_var = json.loads(open(os.path.abspath('./data/app_variables.json'), encoding='utf-8').read())

    if os.path.exists('image'):
        os.rename('image', app_var['path_data_image'])

    if os.path.exists('oauthsettings.json'):
        os.rename('oauthsettings.json', app_var['path_oauth_setting'])

    try:
        load_oauth('discord')
    except KeyError:
        old_oauth_data = json.loads(open(app_var['path_oauth_setting'], encoding='utf-8').read())

        if 'discord' not in old_oauth_data['_README']['support']:
            old_oauth_data['_README']['support'] += ['discord']

        old_oauth_data['discord'] = {}
        old_oauth_data['discord']['client_id'] = ''
        old_oauth_data['discord']['client_secret'] = ''

        with open(app_var['path_oauth_setting'], 'w') as f:
            f.write(json.dumps(old_oauth_data, sort_keys = True, indent = 4))

    # End

def pw_encode(data, data2 = '', type_d = ''):
    if type_d == '':
        curs.execute('select data from other where name = "encode"')
        set_data = curs.fetchall()

        type_d = set_data[0][0]

    if type_d == 'sha256':
        return hashlib.sha256(bytes(data, 'utf-8')).hexdigest()
    elif type_d == 'sha3':
        if sys.version_info < (3, 6):
            return sha3.sha3_256(bytes(data, 'utf-8')).hexdigest()
        else:
            return hashlib.sha3_256(bytes(data, 'utf-8')).hexdigest()
    else:
        if data2 != '':
            salt_data = bytes(data2, 'utf-8')
        else:
            salt_data = bcrypt.gensalt(11)
            
        return bcrypt.hashpw(bytes(data, 'utf-8'), salt_data).decode()

def pw_check(data, data2, type_d = 'no', id_d = ''):
    curs.execute('select data from other where name = "encode"')
    db_data = curs.fetchall()

    if type_d != 'no':
        if type_d == '':
            set_data = 'bcrypt'
        else:
            set_data = type_d
    else:
        set_data = db_data[0][0]
    
    while 1:
        if set_data in ['sha256', 'sha3']:
            data3 = pw_encode(data = data, type_d = set_data)
            if data3 == data2:
                re_data = 1
            else:
                re_data = 0

            break
        else:
            try:
                if pw_encode(data, data2, 'bcrypt') == data2:
                    re_data = 1
                else:
                    re_data = 0

                break
            except:
                set_data = db_data[0][0]

    if db_data[0][0] != set_data and re_data == 1 and id_d != '':
        curs.execute("update user set pw = ?, encode = ? where id = ?", [pw_encode(data), db_data[0][0], id_d])

    return re_data

def captcha_post(re_data, num = 1):
    if num == 1:
        if custom()[2] == 0 and captcha_get() != '':
            curs.execute('select data from other where name = "sec_re"')
            sec_re = curs.fetchall()
            if sec_re and sec_re[0][0] != '':
                try:
                    data = urllib.request.urlopen('https://www.google.com/recaptcha/api/siteverify?secret=' + sec_re[0][0] + '&response=' + re_data)
                except:
                    pass
                    
                if data and data.getcode() == 200:
                    json_data = json.loads(data.read().decode(data.headers.get_content_charset()))
                    if json_data['success'] == True:
                        return 0
                    else:
                        return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 0
    else:
        pass

def load_lang(data, num = 2, safe = 0):
    if num == 1:
        curs.execute("select data from other where name = 'language'")
        rep_data = curs.fetchall()

        json_data = open(os.path.join('language', rep_data[0][0] + '.json'), 'rt', encoding='utf-8').read()
        lang = json.loads(json_data)

        if data in lang:
            if safe == 1:
                return lang[data]
            else:
                return html.escape(lang[data])
        else:
            return html.escape(data + ' (M)')
    else:
        curs.execute('select data from user_set where name = "lang" and id = ?', [ip_check()])
        rep_data = curs.fetchall()
        if rep_data:
            try:
                json_data = open(os.path.join('language', rep_data[0][0] + '.json'), 'rt', encoding='utf-8').read()
                lang = json.loads(json_data)
            except:
                return load_lang(data, 1, safe)

            if data in lang:
                if safe == 1:
                    return lang[data]
                else:
                    return html.escape(lang[data])
            else:
                return load_lang(data, 1, safe)
        else:
            return load_lang(data, 1, safe)

def load_oauth(provider):
    oauth = json.loads(open(app_var['path_oauth_setting'], encoding='utf-8').read())

    return oauth[provider]

def update_oauth(provider, target, content):
    oauth = json.loads(open(app_var['path_oauth_setting'], encoding='utf-8').read())
    oauth[provider][target] = content

    with open(app_var['path_oauth_setting'], 'w') as f:
        f.write(json.dumps(oauth, sort_keys=True, indent=4))

    return 'Done'

def ip_or_user(data):
    if re.search('(\.|:)', data):
        return 1
    else:
        return 0

def edit_button():
    insert_list = [
        ['[[name|view]]', load_lang('edit_button_link')], 
        ['[* data]', load_lang('edit_button_footnote')], 
        ['[macro(data)]', load_lang('edit_button_macro')],
        ['{{{#color data}}}', load_lang('edit_button_color')], 
        ["\\'\\'\\'data\\'\\'\\'", load_lang('edit_button_bold')],
        ["~~data~~", load_lang('edit_button_strike')],
        ["{{{+number data}}}", load_lang('edit_button_big')],
        ["== name ==", load_lang('edit_button_paragraph')]
    ]

    data = ''
    for insert_data in insert_list:
        data += '<a href="javascript:insert_data(\'content\', \'' + insert_data[0] + '\')">[' + insert_data[1] + ']</a> '

    return data + '<hr class=\"main_hr\">'

def ip_warring():
    if custom()[2] == 0:    
        curs.execute('select data from other where name = "no_login_warring"')
        data = curs.fetchall()
        if data and data[0][0] != '':
            text_data = '<span>' + data[0][0] + '</span>'
        else:
            text_data = '<span>비로그인 상태로 편집합니다. 편집 역사에 IP(' + str(ip_check()) + ')가 영구히 기록됩니다.</span><br><br>'
    else:
        text_data = ''

    return text_data

def skin_check(set_n = 0):
    skin = 'buma'

    curs.execute('select data from other where name = "skin"')
    skin_exist = curs.fetchall()
    if skin_exist and skin_exist[0][0] != '':
        if os.path.exists(os.path.abspath('./views/' + skin_exist[0][0] + '/index.html')) == 1:
            skin = skin_exist[0][0]
    
    curs.execute('select data from user_set where name = "skin" and id = ?', [ip_check()])
    skin_exist = curs.fetchall()
    if skin_exist and skin_exist[0][0] != '':
        if os.path.exists(os.path.abspath('./views/' + skin_exist[0][0] + '/index.html')) == 1:
            skin = skin_exist[0][0]

    if set_n == 0:
        return './views/' + skin + '/index.html'
    else:
        return skin

def next_fix(link, num, page, end = 50):
    list_data = '<span> </span><div  style="border-width:1px 1px 1px ;border-style:solid;border-color:#cccccc #cccccc #cccccc;padding:0.3rem 0.7rem;display:table;float:left;border-top-left-radius:5px;border-bottom-left-radius:5px;"><span class="icon ion-chevron-left"></span><span style="color:gray"> Past</span></div>' + '<div  style="border-width:1px 1px 1px 0px;border-style:solid;border-color:#cccccc #cccccc #cccccc;padding:0.3rem 0.7rem;display:table;float:left;border-top-right-radius:5px;border-bottom-right-radius:5px;"><span style="color:gray">Next <span class="icon ion-chevron-right"></span></span></div>'

    if num == 1:
        if len(page) == end:
            list_data = '<span> </span><div  style="border-width:1px 1px 1px ;border-style:solid;border-color:#cccccc #cccccc #cccccc;padding:0.3rem 0.7rem;display:table;float:left;border-top-left-radius:5px;border-bottom-left-radius:5px;"><span class="icon ion-chevron-left"></span><span style="color:gray"> Past</span></div>' + '<div  style="border-width:1px 1px 1px 0px;border-style:solid;border-color:#cccccc #cccccc #cccccc;padding:0.3rem 0.7rem;display:table;float:left;border-top-right-radius:5px;border-bottom-right-radius:5px;"><a href="' + link + str(num + 1) + '" style="color:#000">Next </a><span class="icon ion-chevron-right"></span></div>'
    elif len(page) != end:
        list_data = '<span> </span><div  style="border-width:1px 1px 1px ;border-style:solid;border-color:#cccccc #cccccc #cccccc;padding:0.3rem 0.7rem;display:table;float:left;border-top-left-radius:5px;border-bottom-left-radius:5px;"><span class="icon ion-chevron-left"></span><a href="' + link + str(num - 1) + '" style="color:#000"> Past</a></div>' + '<div  style="border-width:1px 1px 1px 0px;border-style:solid;border-color:#cccccc #cccccc #cccccc;padding:0.3rem 0.7rem;display:table;float:left;border-top-right-radius:5px;border-bottom-right-radius:5px;"><span style="color:gray">Next <span class="icon ion-chevron-right"></span></span></div>'
    else:
        list_data = '<span> </span><div  style="border-width:1px 1px 1px ;border-style:solid;border-color:#cccccc #cccccc #cccccc;padding:0.3rem 0.7rem;display:table;float:left;border-top-left-radius:5px;border-bottom-left-radius:5px;"><span class="icon ion-chevron-left"></span><a href="' + link + str(num - 1) + '" style="color:#000"> Past</a></div>' + '<div  style="border-width:1px 1px 1px;border-style:solid;border-color:#cccccc #cccccc #cccccc;padding:0.3rem 0.7rem;display:table;float:left;border-top-right-radius:5px;border-bottom-right-radius:5px;"><a href="' + link + str(num + 1) + '" style="color:#000">Next </a><span class="icon ion-chevron-left"></span></div>'

    return list_data
    
def next_fix_f(link, num, page, end = 50):
    list_data = '<span> </span><div  style="border-width:1px 1px 1px ;border-style:solid;border-color:#cccccc #cccccc #cccccc;padding:0.3rem 0.7rem;display:table;float:left;border-top-left-radius:5px;border-bottom-left-radius:5px;"><span class="icon ion-chevron-left"></span><a href="' + link + str(num - 1) + '" style="color:#000"> Past</a></div>' + '<div  style="border-width:1px 1px 1px;border-style:solid;border-color:#cccccc #cccccc #cccccc;padding:0.3rem 0.7rem;display:table;float:left;border-top-right-radius:5px;border-bottom-right-radius:5px;"><a href="' + link + str(num + 1) + '" style="color:#000">Next </a><span class="icon ion-chevron-left"></span></div>'
    
    return list_data

def other2(data):
    req_list = ''
    for i_data in os.listdir(os.path.join("views", "main_css", "css")):
        req_list += '<link rel="stylesheet" href="/views/main_css/css/' + i_data + '">'
    
    for i_data in os.listdir(os.path.join("views", "main_css", "js")):
        req_list += '<script src="/views/main_css/js/' + i_data + '"></script>'

    data += ['', '''
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/styles/default.min.css">
        <link   rel="stylesheet"
                href="https://cdn.jsdelivr.net/npm/katex@0.10.1/dist/katex.min.css"
                integrity="sha384-dbVIfZGuN1Yq7/1Ocstc1lUEm+AT+/rCkibIcC/OmWo5f0EA48Vf8CytHzGrSwbQ"
                crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/katex@0.10.1/dist/katex.min.js"
                integrity="sha384-2BKqo+exmr9su6dir+qCw08N2ZKRucY4PrGQPPWU1A7FtlCGjmEGFqXCv5nyM5Ij"
                crossorigin="anonymous"></script>
        <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/highlight.min.js"></script>
    ''' + req_list]

    return data

def cut_100(data):
    return re.sub('<(((?!>).)*)>', '', data)[0:100] + '...'

def wiki_set(num = 1):
    if num == 1:
        data_list = []

        curs.execute('select data from other where name = ?', ['name'])
        db_data = curs.fetchall()
        if db_data and db_data[0][0] != '':
            data_list += [db_data[0][0]]
        else:
            data_list += ['무제위키']

        curs.execute('select data from other where name = "license"')
        db_data = curs.fetchall()
        if db_data and db_data[0][0] != '':
            data_list += [db_data[0][0]]
        else:
            data_list += ['모든 문서는 CC 0에 따라 사용할 수 있습니다.']

        data_list += ['', '']

        curs.execute('select data from other where name = "logo"')
        db_data = curs.fetchall()
        if db_data and db_data[0][0] != '':
            data_list += [db_data[0][0]]
        else:
            data_list += [data_list[0]]
            
        curs.execute("select data from other where name = 'head' and coverage = ?", [skin_check(1)])
        db_data = curs.fetchall()
        if db_data and db_data[0][0] != '':
            data_list += [db_data[0][0]]
        else:
            curs.execute("select data from other where name = 'head' and coverage = ''")
            db_data = curs.fetchall()
            if db_data and db_data[0][0] != '':
                data_list += [db_data[0][0]]
            else:
                data_list += ['']

        return data_list

    if num == 2:
        var_data = '무제위키:대문'

        curs.execute('select data from other where name = "frontpage"')
    elif num == 3:
        var_data = '2'

        curs.execute('select data from other where name = "upload"')
    
    db_data = curs.fetchall()
    if db_data and db_data[0][0] != '':
        return db_data[0][0]
    else:
        return var_data

def diff(seqm):
    output = []

    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output += [seqm.a[a0:a1]]
        elif opcode == 'insert':
            output += ["<span style='background:#CFC;'>" + seqm.b[b0:b1] + "</span>"]
        elif opcode == 'delete':
            output += ["<span style='background:#FDD;'>" + seqm.a[a0:a1] + "</span>"]
        elif opcode == 'replace':
            output += ["<span style='background:#FDD;'>" + seqm.a[a0:a1] + "</span>"]
            output += ["<span style='background:#CFC;'>" + seqm.b[b0:b1] + "</span>"]

    end = ''.join(output)
    end = end.replace('\r\n', '\n')
    sub = ''

    if not re.search('\n$', end):
        end += '\n'

    num = 0
    left = 1
    while 1:
        data = re.search('((?:(?!\n).)*)\n', end)
        if data:
            data = data.groups()[0]
            
            left += 1
            if re.search('<span style=\'(?:(?:(?!\').)+)\'>', data):
                num += 1
                if re.search('<\/span>', data):
                    num -= 1

                sub += str(left) + ' : ' + re.sub('(?P<in>(?:(?!\n).)*)\n', '\g<in>', data, 1) + '<br>'
            else:
                if re.search('<\/span>', data):
                    num -= 1
                    sub += str(left) + ' : ' + re.sub('(?P<in>(?:(?!\n).)*)\n', '\g<in>', data, 1) + '<br>'
                else:
                    if num > 0:
                        sub += str(left) + ' : ' + re.sub('(?P<in>.*)\n', '\g<in>', data, 1) + '<br>'

            end = re.sub('((?:(?!\n).)*)\n', '', end, 1)
        else:
            break
            
    return sub
           
def admin_check(num = None, what = None):
    ip = ip_check() 

    curs.execute("select acl from user where id = ?", [ip])
    user = curs.fetchall()
    if user:
        reset = 0

        while 1:
            if num == 1 and reset == 0:
                check = 'ban'
            elif num == 3 and reset == 0:
                check = 'toron'
            elif num == 4 and reset == 0:
                check = 'check'
            elif num == 5 and reset == 0:
                check = 'acl'
            elif num == 6 and reset == 0:
                check = 'hidel'
            elif num == 7 and reset == 0:
                check = 'give'
            else:
                check = 'owner'

            curs.execute('select name from alist where name = ? and acl = ?', [user[0][0], check])
            if curs.fetchall():
                if what:
                    curs.execute("insert into re_admin (who, what, time) values (?, ?, ?)", [ip, what, get_time()])
                    conn.commit()

                return 1
            else:
                if reset == 0:
                    reset = 1
                else:
                    break
                    
    return 0

def ip_pas_t(raw_ip):
    hide = 0

    if re.search("(\.|:)", raw_ip):    
        curs.execute("select data from other where name = 'ip_view'")
        data = curs.fetchall()
        if data and data[0][0] != '':
            ip = re.sub('((?:(?!\.).)+)$', 'xxx', raw_ip)

            if not admin_check(1):
                hide = 1
        else:
            ip = '<a href="/contribution/ip/' + raw_ip + '/document">' + raw_ip + '</a>'
    else:
        curs.execute("select title from data where title = ?", ['사용자:' + raw_ip])
        if curs.fetchall():
            ip = '<a href="/w/' + url_pas('사용자:' + raw_ip) + '">' + raw_ip + '</a>'
        else:
            ip = '<a href="/w/' + url_pas('사용자:' + raw_ip) + '">' + raw_ip + '</a>'
         
    #if hide == 0:
        #ip += ' <a href="/tool/' + url_pas(raw_ip) + '">(' + load_lang('tool') + ')</a>'

    return ip
    
def ip_pas(raw_ip):
    hide = 0

    if re.search("(\.|:)", raw_ip):    
        curs.execute("select data from other where name = 'ip_view'")
        data = curs.fetchall()
        if data and data[0][0] != '':
            ip = re.sub('((?:(?!\.).)+)$', 'xxx', raw_ip)

            if not admin_check(1):
                hide = 1
        else:
            ip = '<a href="/contribution/ip/' + raw_ip + '/document">' + raw_ip + '</a>'
    else:
        curs.execute("select title from data where title = ?", ['사용자:' + raw_ip])
        if curs.fetchall():
            ip = '<a href="/w/' + url_pas('사용자:' + raw_ip) + '"><b>' + raw_ip + '</b></a>'
        else:
            ip = '<a href="/w/' + url_pas('사용자:' + raw_ip) + '"><b>' + raw_ip + '</b></a>'
         
    #if hide == 0:
        #ip += ' <a href="/tool/' + url_pas(raw_ip) + '">(' + load_lang('tool') + ')</a>'

    return ip

def ip_pas_raw(raw_ip):
    hide = 0

    if re.search("(\.|:)", raw_ip):    
        curs.execute("select data from other where name = 'ip_view'")
        data = curs.fetchall()
        if data and data[0][0] != '':
            ip = re.sub('((?:(?!\.).)+)$', 'xxx', raw_ip)

            if not admin_check(1):
                hide = 1
        else:
            ip = '<a href="/record/' + raw_ip + '">' + raw_ip + '</a>'
    else:
        curs.execute("select title from data where title = ?", ['사용자:' + raw_ip])
        if curs.fetchall():
            ip = '<a href="/w/' + url_pas('사용자:' + raw_ip) + '"><b>' + raw_ip + '</b></a>'
        else:
            ip = '<a href="/w/' + url_pas('사용자:' + raw_ip) + '"><b>' + raw_ip + '</b></a>'
         
    #if hide == 0:
        #ip += ' <a href="/tool/' + url_pas(raw_ip) + '">(' + load_lang('tool') + ')</a>'

    return raw_ip
    
def toplst(name):
    curs.execute("select sub from rd where title = ? order by date desc", [name])
    
    ud = 0
    for data in curs.fetchall():
        it_p = 0
        curs.execute("select title from rd where title = ? and sub = ? and stop = 'O' order by sub asc", [name, data[0]])
        if curs.fetchall():
            it_p = 1
        if it_p == 0:
            ud = 1
            break
    
    
    return ud


def custom():
    if 'head' in flask.session:
        user_head = flask.session['head']
    else:
        user_head = ''

    ip = ip_check()
    if ip_or_user(ip) == 0:
        curs.execute('select name from alarm where name = ? limit 1', [ip])
        if curs.fetchall():
            user_icon = 2
        else:
            user_icon = 1
    else:
        user_icon = 0

    if user_icon != 0:
        curs.execute('select data from user_set where name = "email" and id = ?', [ip])
        data = curs.fetchall()
        if data:
            email = data[0][0]
        else:
            email = ''
    else:
        email = ''

    if user_icon != 0:
        user_name = ip
    else:
        user_name = load_lang('user')

    return ['', '', user_icon, user_head, email, user_name, ip_check(), admin_check(1), admin_check(3), admin_check(4), admin_check(5), admin_check(6), admin_check(7), admin_check(), toplst('사용자:' + ip_check())]

def load_skin(data = '', set_n = 0):
    div2 = ''
    div3 = []
    system_file = ['main_css', 'easter_egg.html']

    if data == '':
        ip = ip_check()

        curs.execute('select data from user_set where name = "skin" and id = ?', [ip])
        data = curs.fetchall()

        if not data:
            curs.execute('select data from other where name = "skin"')
            data = curs.fetchall()
            if not data:
                data = [['neo_yousoro']]

        if set_n == 0:
            for skin_data in os.listdir(os.path.abspath('views')):
                if not skin_data in system_file:
                    if data[0][0] == skin_data:
                        div2 = '<option value="' + skin_data + '" selected>' + skin_data + '</option>' + div2
                    else:
                        div2 += '<option value="' + skin_data + '">' + skin_data + '</option>'
        else:
            div2 = []
            for skin_data in os.listdir(os.path.abspath('views')):
                if not skin_data in system_file:
                    if data[0][0] == skin_data:
                        div2 = [skin_data] + div2
                    else:
                        div2 += [skin_data]
    else:
        if set_n == 0:
            for skin_data in os.listdir(os.path.abspath('views')):
                if not skin_data in system_file:
                    if data == skin_data:
                        div2 = '<option value="' + skin_data + '" selected>' + skin_data + '</option>' + div2
                    else:
                        div2 += '<option value="' + skin_data + '">' + skin_data + '</option>'
        else:
            div2 = []
            for skin_data in os.listdir(os.path.abspath('views')):
                if not skin_data in system_file:
                    if data == skin_data:
                        div2 = [skin_data] + div2
                    else:
                        div2 += [skin_data]

    return div2

def acl_check(name, tool = ''):
    ip = ip_check()
    
    if tool == 'render':
        curs.execute("select view from acl where title = ?", [name])
        acl_data = curs.fetchall()
        if acl_data:
            if acl_data[0][0] == 'user':
                if ip_or_user(ip) == 1:
                    return 1

            if acl_data[0][0] == '50_edit':
                if ip_or_user(ip) == 1:
                    return 1
                
                if admin_check(5, 'view (' + name + ')') != 1:
                    curs.execute("select count(title) from history where ip = ?", [ip])
                    count = curs.fetchall()
                    if count:
                        count = count[0][0]
                    else:
                        count = 0

                    if count < 50:
                        return 1

            if acl_data[0][0] == 'admin':
                if ip_or_user(ip) == 1:
                    return 1

                if admin_check(5, 'view (' + name + ')') != 1:
                    return 1

        return 0
    else:
        if ban_check() == 1:
            return 1

        acl_c = re.search("^사용자:((?:(?!\/).)*)", name)
        if acl_c:
            acl_n = acl_c.groups()

            if admin_check(5) == 1:
                return 0

            curs.execute("select dec from acl where title = ?", ['사용자:' + acl_n[0]])
            acl_data = curs.fetchall()
            if acl_data:
                if acl_data[0][0] == 'all':
                    return 0

                if acl_data[0][0] == 'user' and not re.search("(\.|:)", ip):
                    return 0

                if ip != acl_n[0] or re.search("(\.|:)", ip):
                    return 1
            
            if ip == acl_n[0] and not re.search("(\.|:)", ip) and not re.search("(\.|:)", acl_n[0]):
                return 0
            else:
                return 1

        if re.search("^file:", name) and admin_check(None, 'file edit (' + name + ')') != 1:
            return 1

        curs.execute("select dec from acl where title = ?", [name])
        acl_data = curs.fetchall()
        if acl_data:
            if acl_data[0][0] == 'user':
                if ip_or_user(ip) == 1:
                    return 1

            if acl_data[0][0] == 'admin':
                if ip_or_user(ip) == 1:
                    return 1

                if admin_check(5) != 1:
                    return 1

            if acl_data[0][0] == '50_edit':
                if ip_or_user(ip) == 1:
                    return 1
                
                if admin_check(5) != 1:
                    curs.execute("select count(title) from history where ip = ?", [ip])
                    count = curs.fetchall()
                    if count:
                        count = count[0][0]
                    else:
                        count = 0

                    if count < 50:
                        return 1

            if acl_data[0][0] == 'email':
                if ip_or_user(ip) == 1:
                    return 1
                
                if admin_check(5) != 1:
                    curs.execute("select data from user_set where id = ? and name = 'email'", [ip])
                    email = curs.fetchall()
                    if not email:
                        return 1

        curs.execute('select data from other where name = "edit"')
        set_data = curs.fetchall()
        if set_data:
            if set_data[0][0] == 'login':
                if ip_or_user(ip) == 1:
                    return 1

            if set_data[0][0] == 'admin':
                if ip_or_user(ip) == 1:
                    return 1

                if admin_check(5, 'edit (' + name + ')') != 1:
                    return 1

            if set_data[0][0] == '50_edit':
                if ip_or_user(ip) == 1:
                    return 1
                
                if admin_check(5, 'edit (' + name + ')') != 1:
                    curs.execute("select count(title) from history where ip = ?", [ip])
                    count = curs.fetchall()
                    if count:
                        count = count[0][0]
                    else:
                        count = 0

                    if count < 50:
                        return 1

        return 0

def ban_check(ip = None, tool = None):
    if not ip:
        ip = ip_check()

    band = re.search("^([0-9]{1,3}\.[0-9]{1,3})", ip)
    if band:
        band_it = band.groups()[0]
    else:
        band_it = '-'

    curs.execute("delete from ban where (end < ? and end like '2%')", [get_time()])
    conn.commit()

    curs.execute("select login, block from ban where ((end > ? and end like '2%') or end = '') and band = 'regex'", [get_time()])
    regex_d = curs.fetchall()
    for test_r in regex_d:
        g_regex = re.compile(test_r[1])
        if g_regex.search(ip):
            if tool and tool == 'login':
                if test_r[0] != 'O':
                    return 1
            else:
                return 1
    
    curs.execute("select login from ban where ((end > ? and end like '2%') or end = '') and block = ? and band = 'O'", [get_time(), band_it])
    band_d = curs.fetchall()
    if band_d:
        if tool and tool == 'login':
            if band_d[0][0] != 'O':
                return 1
        else:
            return 1

    curs.execute("select login from ban where ((end > ? and end like '2%') or end = '') and block = ? and band = ''", [get_time(), ip])
    ban_d = curs.fetchall()
    if ban_d:
        if tool and tool == 'login':
            if ban_d[0][0] != 'O':
                return 1
        else:
            return 1

    return 0
        
def topic_check(name, sub):
    ip = ip_check()

    if ban_check() == 1:
        return 1

    curs.execute('select data from other where name = "discussion"')
    acl_data = curs.fetchall()
    if acl_data:
        if acl_data[0][0] == 'login':
            if ip_or_user(ip) == 1:
                return 1

        if acl_data[0][0] == 'admin':
            if ip_or_user(ip) == 1:
                return 1

            if admin_check(3, 'topic (' + name + ')') != 1:
                return 1

    curs.execute("select dis from acl where title = ?", [name])
    acl_data = curs.fetchall()
    if acl_data:
        if acl_data[0][0] == 'user':
            if ip_or_user(ip) == 1:
                return 1

        if acl_data[0][0] == '50_edit':
            if ip_or_user(ip) == 1:
                return 1
            
            if admin_check(3, 'topic (' + name + ')') != 1:
                curs.execute("select count(title) from history where ip = ?", [ip])
                count = curs.fetchall()
                if count:
                    count = count[0][0]
                else:
                    count = 0

                if count < 50:
                    return 1

        if acl_data[0][0] == 'admin':
            if ip_or_user(ip) == 1:
                return 1

            if admin_check(3, 'topic (' + name + ')') != 1:
                return 1
        
    curs.execute("select title from rd where title = ? and sub = ? and not stop = ''", [name, sub])
    if curs.fetchall():
        if admin_check(3, 'topic (' + name + ')') != 1:
            return 1

    return 0

def ban_insert(name, end, why, login, blocker, type_d = None):
    now_time = get_time()

    if type_d:
        band = type_d
    else:
        if re.search("^([0-9]{1,3}\.[0-9]{1,3})$", name):
            band = 'O'
        else:
            band = ''

    curs.execute("delete from ban where (end < ? and end like '2%')", [get_time()])

    curs.execute("select block from ban where ((end > ? and end like '2%') or end = '') and block = ? and band = ?", [get_time(), name, band])
    if curs.fetchall():
        curs.execute("insert into rb (block, end, today, blocker, why, band) values (?, ?, ?, ?, ?, ?)", [
            name, 
            'release',
            now_time, 
            blocker, 
            '', 
            band
        ])
        curs.execute("delete from ban where block = ? and band = ?", [name, band])
    else:
        if login != '':
            login = 'O'
        else:
            login = ''

        if end != '0':
            end = int(number_check(end))

            time = datetime.datetime.now()
            plus = datetime.timedelta(seconds = end)
            r_time = (time + plus).strftime("%Y-%m-%d %H:%M:%S")
        else:
            r_time = ''

        curs.execute("insert into rb (block, end, today, blocker, why, band) values (?, ?, ?, ?, ?, ?)", [name, end, now_time, blocker, why, band])
        curs.execute("insert into ban (block, end, why, band, login, start) values (?, ?, ?, ?, ?, ?)", [name, r_time, why, band, login, now_time])
    
    conn.commit()
    
def ban_gr(name, end, why, login, blocker, type_d = None):
    now_time = get_time()


    band = ''

    #curs.execute("delete from ban where (end < ? and end like '2%')", [get_time()])



    login = ''

    

    curs.execute("insert into rb (block, end, today, blocker, why, band) values (?, ?, ?, ?, ?, ?)", [name, end, now_time, blocker, why, band])
    #curs.execute("insert into ban (block, end, why, band, login) values (?, ?, ?, ?, ?)", [name, r_time, why, band, login])
    
    conn.commit()
    
def ban_lh(name, end, why, login, blocker, type_d = None):
    now_time = get_time()


    band = ''

    #curs.execute("delete from ban where (end < ? and end like '2%')", [get_time()])



    login = ''

    

    curs.execute("insert into rb (block, end, today, blocker, why, band) values (?, ?, ?, ?, ?, ?)", [name, end, now_time, blocker, why, band])
    #curs.execute("insert into ban (block, end, why, band, login) values (?, ?, ?, ?, ?)", [name, r_time, why, band, login])
    
    conn.commit()

def rd_plus(title, sub, date):
    curs.execute("select title from rd where title = ? and sub = ?", [title, sub])
    if curs.fetchall():
        curs.execute("update rd set date = ? where title = ? and sub = ?", [date, title, sub])
    else:
        curs.execute("insert into rd (title, sub, date) values (?, ?, ?)", [title, sub, date])

def history_plus(title, data, date, ip, send, leng, t_check = ''):
    curs.execute("select id from history where title = ? order by id + 0 desc limit 1", [title])
    id_data = curs.fetchall()

    send = re.sub('\(|\)|<|>', '', send)
    iii = ''
    if len(send) > 128:
        send = send[:128]

    if t_check != '':
        iii = '<i>(' + t_check + ')</i>'

    curs.execute("insert into history (id, title, data, date, ip, send, leng, hide, i) values (?, ?, ?, ?, ?, ?, ?, '', ?)", [
        str(int(id_data[0][0]) + 1) if id_data else '1',
        title,
        data,
        date,
        ip,
        send,
        leng,
        iii
    ])
    
def block_why(conn, name, tool = ''):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0
    
    div = '''
        <ul>
    '''
    
    su = ''
    
    data_list = ''

    curs.execute("delete from ban where (end < ? and end like '2%')", [get_time()])
    conn.commit()
    
    
    curs.execute("select why, block, '', end, '', band from ban where ((end > ? and end like '2%') or end = '') order by end desc", [get_time()])
    
    if data_list == '':
        data_list = curs.fetchall()

    for data in data_list:
        why = html.escape(data[0])
        if why == '':
            why = '<br>'
        
        if data[5] == 'O':
            ip = data[1] + ' (' + load_lang('range') + ')'
        elif data[5] == 'regex':
            ip = data[1] + ' (' + load_lang('regex') + ')'
        else:
            ip = ip_pas_raw(data[1])

        if data[3] == '':
            end = load_lang('limitless')
        elif data[3] == 'release':
            end = load_lang('release')
        else:
            end = data[3]
            

        if data[2] == '':
            admin = '알 수 없는'
        elif re.search('^tool:', data[2]):
            admin = data[2]
        elif re.search('^도구:', data[2]):
            admin = data[2]
        else:
            admin = ip_pas(data[2])

        if data[4] == '':
            start = ''
        else:
            start = data[4]
        
        if end == '차단 해제':
            #div += '''<div style="display:none"><li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (''' + end + ''' 까지) (''' + why.replace('<br>', '') + ''')</li></div>'''
            div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단 해제)</i> (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''
        elif end == '무기한':
            if ip == name:
                su = why.replace('<br>', '')
                break
            #div += '''<div style="display:none"><li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (영구적으로) (''' + why.replace('<br>', '') + ''')</li></div>'''
            div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (영구적으로) (<span style="color:gray">''' + why.replace('<br>', '') + ''')</span></li>'''
        if not(end == '차단 해제' or end == '무기한'):
            if ip == name:
                su = why.replace('<br>', '')
                break
            div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (''' + end + ''' 까지) (<span style="color:gray">''' + why.replace('<br>', '') + ''')</span></li>'''
            

    div += '</ul>'
                
    return su
    
def block_when(conn, name, tool = ''):
    curs = conn.cursor()

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0
    
    div = '''
        <ul>
    '''
    
    su = ''
    
    data_list = ''

    curs.execute("delete from ban where (end < ? and end like '2%')", [get_time()])
    conn.commit()
    
    
    curs.execute("select why, block, '', end, '', band from ban where ((end > ? and end like '2%') or end = '') order by end desc", [get_time()])
    
    if data_list == '':
        data_list = curs.fetchall()

    for data in data_list:
        why = html.escape(data[0])
        if why == '':
            why = '<br>'
        
        if data[5] == 'O':
            ip = data[1] + ' (' + load_lang('range') + ')'
        elif data[5] == 'regex':
            ip = data[1] + ' (' + load_lang('regex') + ')'
        else:
            ip = ip_pas_raw(data[1])

        if data[3] == '':
            end = load_lang('limitless')
        elif data[3] == 'release':
            end = load_lang('release')
        else:
            end = data[3]
            

        if data[2] == '':
            admin = '알 수 없는'
        elif re.search('^tool:', data[2]):
            admin = data[2]
        elif re.search('^도구:', data[2]):
            admin = data[2]
        else:
            admin = ip_pas(data[2])

        if data[4] == '':
            start = ''
        else:
            start = data[4]
        
        if end == '차단 해제':
            #div += '''<div style="display:none"><li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (''' + end + ''' 까지) (''' + why.replace('<br>', '') + ''')</li></div>'''
            div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단 해제)</i> (<span style="color:gray">''' + why.replace('<br>', '') + '''</span>)</li>'''
        elif end == '무기한':
            if ip == name:
                su = start
                break
            #div += '''<div style="display:none"><li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (영구적으로) (''' + why.replace('<br>', '') + ''')</li></div>'''
            div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (영구적으로) (<span style="color:gray">''' + why.replace('<br>', '') + ''')</span></li>'''
        if not(end == '차단 해제' or end == '무기한'):
            if ip == name:
                su = start
                break
            div += '''<li>''' + start + ''' ''' + admin + ''' 사용자가 ''' + ip + ''' <i>(사용자 차단)</i> (''' + end + ''' 까지) (<span style="color:gray">''' + why.replace('<br>', '') + ''')</span></li>'''
            

    div += '</ul>'
                
    return su

def leng_check(first, second):
    if first < second:
        all_plus = '+' + str(second - first)
    elif second < first:
        all_plus = '-' + str(first - second)
    else:
        all_plus = '0'
        
    return all_plus

def number_check(data):
    if not data:
        return '1'
    else:
        if re.search('[^0-9]', data):
            return '1'
        else:
            return data

def edit_filter_do(data):
    if admin_check(1, 'edit_filter pass') != 1:
        curs.execute("select regex, sub from filter")
        for data_list in curs.fetchall():
            match = re.compile(data_list[0], re.I)
            if match.search(data):
                ban_insert(
                    ip_check(), 
                    '0' if data_list[1] == 'X' else data_list[1], 
                    '편집 필터', 
                    None, 
                    '도구:편집 필터'
                )
                
                return 1
    
    return 0

def redirect(data = '/'):
    return flask.redirect(data)
    
def re_tul(data,un):
    conn.commit()
    
    if data == '/ban':
        ip = un

        end = load_lang('authority_error')

        if ban_check(un) == 1:
            end = ''
            ok_sign = 1

            band = re.search("^([0-9]{1,3}\.[0-9]{1,3})", ip)
            if band:
                band_it = band.groups()[0]
            else:
                band_it = '-'

            curs.execute("delete from ban where (end < ? and end like '2%')", [get_time()])
            conn.commit()

            curs.execute("select login, block, end from ban where ((end > ? and end like '2%') or end = '') and band = 'regex'", [get_time()])
            regex_d = curs.fetchall()
            for test_r in regex_d:
                g_regex = re.compile(test_r[1])
                if g_regex.search(ip):
                    #end += '<li>' + load_lang('type') + ' : regex ban</li>'
                    end += '이 사용자는 ' + test_r[2] + '까지 차단되었습니다.'
                    if test_r[0] != 'O':
                        sadfs = ''
                        #end += '<li>' + load_lang('login_able') + ' (' + load_lang('not_sure') + ')</li>'


            
            curs.execute("select login, end, why, start from ban where ((end > ? and end like '2%') or end = '') and block = ?", [get_time(), band_it])
            band_d = curs.fetchall()
            
            if band_d:
                #end += '<li>' + load_lang('type') + ' : band ban</li>'
                st = band_d[0][3]
                if st == '':
                    st = '알 수 없는 시간'
                if band_d[0][1] == '':
                    end += '이 사용자는 ' + st + '에 영구적으로 차단되었습니다.<br>'
                    end += '차단 사유 : ' + band_d[0][2]
                else:
                    end += '이 사용자는 ' + st + '에 ' + band_d[0][1] + '까지 차단되었습니다.<br>'
                    end += '차단 사유 : ' + band_d[0][2]
                if data[0][0] != 'O':
                    wsdsaf = ''
                    #end += '<li>' + load_lang('login_able') + ' (' + load_lang('not_sure') + ')</li>'



            curs.execute("select login, end, why, start from ban where ((end > ? and end like '2%') or end = '') and block = ?", [get_time(), ip])
            ban_d = curs.fetchall()
            
            if ban_d:
                st1 = ban_d[0][3]
                #end += '<li>' + load_lang('type') + ' : ban</li>'
                if st1 == '':
                    st1 = '알 수 없는 시간'
                if ban_d[0][1] == '':
                    end += '이 사용자는 ' + st1 + '에 영구적으로 차단되었습니다.<br>'
                    end += '차단 사유 : ' + ban_d[0][2]
                else:
                    end += '이 사용자는 ' + st1 + '에 ' + ban_d[0][1] + '까지 차단되었습니다.<br>'
                    end += '차단 사유 : ' + ban_d[0][2]
                if data[0][0] != 'O':
                    sadAD = 'sw'
                    #end += '<li>' + load_lang('login_able') + ' (' + load_lang('not_sure') + ')</li>'

                #end += '<hr class=\"main_hr\">'

        return end
    else:
        error_data = re.search('\/error\/([0-9]+)', data)
        if error_data:
            num = int(error_data.groups()[0])
            if num == 1:
                data = load_lang('no_login_error')
            elif num == 2:
                data = load_lang('no_exist_user_error')
            elif num == 3:
                data = load_lang('authority_error')
            elif num == 4:
                data = load_lang('no_admin_block_error')
            elif num == 6:
                data = load_lang('same_id_exist_error')
            elif num == 7:
                data = load_lang('long_id_error')
            elif num == 8:
                data = load_lang('id_char_error') + ' <a href="/name_filter">(' + load_lang('id') + ' ' + load_lang('filter') + ')</a>'
            elif num == 9:
                data = load_lang('file_exist_error')
            elif num == 10:
                data = load_lang('password_error')
            elif num == 11:
                data = load_lang('topic_long_error')
            elif num == 12:
                data = load_lang('email_error')
            elif num == 13:
                data = load_lang('recaptcha_error')
            elif num == 14:
                data = load_lang('file_extension_error')
            elif num == 15:
                data = load_lang('edit_record_error')
            elif num == 16:
                data = load_lang('same_file_error')
            elif num == 17:
                data = load_lang('file_capacity_error') + ' ' + wiki_set(3)
            elif num == 19:
                data = load_lang('decument_exist_error')
            elif num == 20:
                data = load_lang('password_diffrent_error')
            elif num == 21:
                data = load_lang('edit_filter_error')
            elif num == 22:
                data = load_lang('file_name_error')
            elif num == 23:
                data = load_lang('regex_error')
            else:
                data = '???'

            return '<strong>[오류!] </strong>' + data
        else:
            return redirect('/')
    
def re_balloon(data, edt = 0, tit = ''):
    conn.commit()
    
    if data == '/ban':
        ip = ip_check()
        
        if edt == 1:
            end = '편집 ' + load_lang('authority_error') + ' 대신 <a href="/new_edit_request/' + url_pas(tit) + '"><b>편집 요청</b></a>을 생성하실 수 있습니다.'
        else:
            end = load_lang('authority_error')

        if ban_check() == 1:
            if re.search(".*\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}.*",ip):
                curs.execute("select login from ban where block = ?", [ip])
                lg = curs.fetchall()
                if lg and lg[0][0] == 'O':
                    end = '이용중인 IP는 문서 훼손행위가 자주 발생하는 IP이므로 로그인이 필요합니다.<br>(이 메세지는 같은 인터넷 공급업체를 사용하는 다른 누군가로 인해 발생했을 가능성이 높습니다.)<br>'
                else:
                    end = 'IP가 ' + load_lang('ban') + '되었습니다.<br>'
            else:
                end = load_lang('ban') + '된 계정입니다.<br>'
            ok_sign = 1

            band = re.search("^([0-9]{1,3}\.[0-9]{1,3})", ip)
            if band:
                band_it = band.groups()[0]
            else:
                band_it = '-'

            curs.execute("delete from ban where (end < ? and end like '2%')", [get_time()])
            conn.commit()

            curs.execute("select login, block, end from ban where ((end > ? and end like '2%') or end = '') and band = 'regex'", [get_time()])
            regex_d = curs.fetchall()
            for test_r in regex_d:
                g_regex = re.compile(test_r[1])
                if g_regex.search(ip):
                    #end += '<li>' + load_lang('type') + ' : regex ban</li>'
                    end += '차단 만료일 : ' + test_r[2] + '<br>'
                    if test_r[0] != 'O':
                        sadfs = ''
                        #end += '<li>' + load_lang('login_able') + ' (' + load_lang('not_sure') + ')</li>'


            
            curs.execute("select login, end, why from ban where ((end > ? and end like '2%') or end = '') and block = ?", [get_time(), band_it])
            band_d = curs.fetchall()
            if band_d:
                #end += '<li>' + load_lang('type') + ' : band ban</li>'
                if band_d[0][1] == '':
                    end += '차단 만료일 : 무기한<br>'
                else:
                    end += '차단 만료일 : ' + band_d[0][1] + '<br>'
                end += '차단 사유 : ' + band_d[0][2]
                if data[0][0] != 'O':
                    wsdsaf = ''
                    #end += '<li>' + load_lang('login_able') + ' (' + load_lang('not_sure') + ')</li>'



            curs.execute("select login, end, why from ban where ((end > ? and end like '2%') or end = '') and block = ?", [get_time(), ip])
            ban_d = curs.fetchall()
            if ban_d:
                #end += '<li>' + load_lang('type') + ' : ban</li>'
                if ban_d[0][1] == '':
                    end += '차단 만료일 : 무기한<br>'
                else:
                    end += '차단 만료일 : ' + ban_d[0][1] + '<br>'
                end += '차단 사유 : ' + ban_d[0][2]
                if data[0][0] != 'O':
                    sadAD = 'sw'
                    #end += '<li>' + load_lang('login_able') + ' (' + load_lang('not_sure') + ')</li>'

                #end += '<hr class=\"main_hr\">'

        return '<strong>[오류!] </strong>' + end
    else:
        error_data = re.search('\/error\/([0-9]+)', data)
        if error_data:
            num = int(error_data.groups()[0])
            if num == 1:
                data = load_lang('no_login_error')
            elif num == 2:
                data = load_lang('no_exist_user_error')
            elif num == 3:
                data = load_lang('authority_error')
            elif num == 4:
                data = load_lang('no_admin_block_error')
            elif num == 6:
                data = load_lang('same_id_exist_error')
            elif num == 7:
                data = load_lang('long_id_error')
            elif num == 8:
                data = load_lang('id_char_error') + ' <a href="/name_filter">(' + load_lang('id') + ' ' + load_lang('filter') + ')</a>'
            elif num == 9:
                data = load_lang('file_exist_error')
            elif num == 10:
                data = load_lang('password_error')
            elif num == 11:
                data = load_lang('topic_long_error')
            elif num == 12:
                data = load_lang('email_error')
            elif num == 13:
                data = load_lang('recaptcha_error')
            elif num == 14:
                data = load_lang('file_extension_error')
            elif num == 15:
                data = load_lang('edit_record_error')
            elif num == 16:
                data = load_lang('same_file_error')
            elif num == 17:
                data = load_lang('file_capacity_error') + ' ' + wiki_set(3)
            elif num == 19:
                data = load_lang('decument_exist_error')
            elif num == 20:
                data = load_lang('password_diffrent_error')
            elif num == 21:
                data = load_lang('edit_filter_error')
            elif num == 22:
                data = load_lang('file_name_error')
            elif num == 23:
                data = load_lang('regex_error')
            else:
                data = '???'

            return '<strong>[오류!] </strong>' + data
        else:
            return redirect('/')


def re_error(data):
    conn.commit()
    
    if data == '/ban':
        ip = ip_check()

        end = load_lang('authority_error')

        if ban_check() == 1:
            if re.search(".*\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}.*",ip):
                curs.execute("select login from ban where block = ?", [ip])
                lg = curs.fetchall()
                if lg and lg[0][0] == 'O':
                    end = '이용중인 IP는 문서 훼손행위가 자주 발생하는 IP이므로 로그인이 필요합니다.<br>(이 메세지는 같은 인터넷 공급업체를 사용하는 다른 누군가로 인해 발생했을 가능성이 높습니다.)<br>'
                else:
                    end = 'IP가 ' + load_lang('ban') + '되었습니다.<br>'
            else:
                end = load_lang('ban') + '된 계정입니다.<br>'
            ok_sign = 1

            band = re.search("^([0-9]{1,3}\.[0-9]{1,3})", ip)
            if band:
                band_it = band.groups()[0]
            else:
                band_it = '-'

            curs.execute("delete from ban where (end < ? and end like '2%')", [get_time()])
            conn.commit()

            curs.execute("select login, block, end from ban where ((end > ? and end like '2%') or end = '') and band = 'regex'", [get_time()])
            regex_d = curs.fetchall()
            for test_r in regex_d:
                g_regex = re.compile(test_r[1])
                if g_regex.search(ip):
                    #end += '<li>' + load_lang('type') + ' : regex ban</li>'
                    end += '차단 만료일 : ' + test_r[2] + '<br>'
                    if test_r[0] != 'O':
                        sadfs = ''
                        #end += '<li>' + load_lang('login_able') + ' (' + load_lang('not_sure') + ')</li>'


            
            curs.execute("select login, end, why from ban where ((end > ? and end like '2%') or end = '') and block = ?", [get_time(), band_it])
            band_d = curs.fetchall()
            if band_d:
                #end += '<li>' + load_lang('type') + ' : band ban</li>'
                if band_d[0][1] == '':
                    end += '차단 만료일 : 무기한<br>'
                else:
                    end += '차단 만료일 : ' + band_d[0][1] + '<br>'
                end += '차단 사유 : ' + band_d[0][2]
                if data[0][0] != 'O':
                    wsdsaf = ''
                    #end += '<li>' + load_lang('login_able') + ' (' + load_lang('not_sure') + ')</li>'



            curs.execute("select login, end, why from ban where ((end > ? and end like '2%') or end = '') and block = ?", [get_time(), ip])
            ban_d = curs.fetchall()
            if ban_d:
                #end += '<li>' + load_lang('type') + ' : ban</li>'
                if ban_d[0][1] == '':
                    end += '차단 만료일 : 무기한<br>'
                else:
                    end += '차단 만료일 : ' + ban_d[0][1] + '<br>'
                end += '차단 사유 : ' + ban_d[0][2]
                if data[0][0] != 'O':
                    sadAD = 'sw'
                    #end += '<li>' + load_lang('login_able') + ' (' + load_lang('not_sure') + ')</li>'

                #end += '<hr class=\"main_hr\">'

        return easy_minify(flask.render_template(skin_check(), 
            imp = [load_lang('error'), wiki_set(1), custom(), other2([0, 0])],
            data = '<div style="font-size: 1.75em;margin-bottom: .5714em;font-weight: 600;">' + end + '</div>',
            menu = 0
        ))
    else:
        error_data = re.search('\/error\/([0-9]+)', data)
        if error_data:
            num = int(error_data.groups()[0])
            if num == 1:
                data = load_lang('no_login_error')
            elif num == 2:
                data = load_lang('no_exist_user_error')
            elif num == 3:
                data = load_lang('authority_error')
            elif num == 4:
                data = load_lang('no_admin_block_error')
            elif num == 6:
                data = load_lang('same_id_exist_error')
            elif num == 7:
                data = load_lang('long_id_error')
            elif num == 8:
                data = load_lang('id_char_error') + ' <a href="/name_filter">(' + load_lang('id') + ' ' + load_lang('filter') + ')</a>'
            elif num == 9:
                data = load_lang('file_exist_error')
            elif num == 10:
                data = load_lang('password_error')
            elif num == 11:
                data = load_lang('topic_long_error')
            elif num == 12:
                data = load_lang('email_error')
            elif num == 13:
                data = load_lang('recaptcha_error')
            elif num == 14:
                data = load_lang('file_extension_error')
            elif num == 15:
                data = load_lang('edit_record_error')
            elif num == 16:
                data = load_lang('same_file_error')
            elif num == 17:
                data = load_lang('file_capacity_error') + ' ' + wiki_set(3)
            elif num == 19:
                data = load_lang('decument_exist_error')
            elif num == 20:
                data = load_lang('password_diffrent_error')
            elif num == 21:
                data = load_lang('edit_filter_error')
            elif num == 22:
                data = load_lang('file_name_error')
            elif num == 23:
                data = load_lang('regex_error')
            #elif num == 99:
                #data = '해당 메뉴가 정의되어 있지 않습니다.'
            elif num == 1000:
                data = 'already_starred_document'
            elif num == 1001:
                data = 'already_unstarred_document'
            elif num == 1100:
                data = '5자 이상의 요약을 입력해 주세요.'
            elif num == 1101:
                data = '문서 삭제에 대한 안내를 확인해 주세요.'
            elif num == 1200:
                data = 'disable_user_document'
            elif num == 3000:
                data = '조건이 틀리거나 사용할 수 없거나 존재하지 않습니다.'
            elif num == 3001:
                data = '구현되지 않았습니다.'
            elif num == 4000:
                data = '편집 요청을 찾을 수 없습니다.'
            elif num == 6001:
                data = '올바른 분류를 선택해주세요.'
            elif num == 6002:
                data = '올바른 라이선스를 선택해주세요.'
            else:
                data = '0으로 나누었습니다.'

            return easy_minify(flask.render_template(skin_check(), 
                imp = [load_lang('error'), wiki_set(1), custom(), other2([0, 0])],
                data = '<div style="font-size: 1.75em;margin-bottom: .5714em;font-weight: 600;">' + data + '</div>',
                menu = 0
            )), 401
        else:
            return redirect('/')


def sks(data):
    conn.commit()
    
    if data == '/ban':
        ip = ip_check()

        end = load_lang('authority_error')

        if ban_check() == 1:
            if re.search(".*\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}.*",ip):
                curs.execute("select login from ban where block = ?", [ip])
                lg = curs.fetchall()
                if lg and lg[0][0] == 'O':
                    end = '이용중인 IP는 문서 훼손행위가 자주 발생하는 IP이므로 로그인이 필요합니다.<br>(이 메세지는 같은 인터넷 공급업체를 사용하는 다른 누군가로 인해 발생했을 가능성이 높습니다.)<br>'
                else:
                    end = 'IP가 ' + load_lang('ban') + '되었습니다.<br>'
            else:
                end = load_lang('ban') + '된 계정입니다.<br>'
            ok_sign = 1

            band = re.search("^([0-9]{1,3}\.[0-9]{1,3})", ip)
            if band:
                band_it = band.groups()[0]
            else:
                band_it = '-'

            curs.execute("delete from ban where (end < ? and end like '2%')", [get_time()])
            conn.commit()

            curs.execute("select login, block, end from ban where ((end > ? and end like '2%') or end = '') and band = 'regex'", [get_time()])
            regex_d = curs.fetchall()
            for test_r in regex_d:
                g_regex = re.compile(test_r[1])
                if g_regex.search(ip):
                    #end += '<li>' + load_lang('type') + ' : regex ban</li>'
                    end += '차단 만료일 : ' + test_r[2] + '<br>'
                    if test_r[0] != 'O':
                        sadfs = ''
                        #end += '<li>' + load_lang('login_able') + ' (' + load_lang('not_sure') + ')</li>'


            
            curs.execute("select login, end, why from ban where ((end > ? and end like '2%') or end = '') and block = ?", [get_time(), band_it])
            band_d = curs.fetchall()
            if band_d:
                #end += '<li>' + load_lang('type') + ' : band ban</li>'
                if band_d[0][1] == '':
                    end += '차단 만료일 : 무기한<br>'
                else:
                    end += '차단 만료일 : ' + band_d[0][1] + '<br>'
                end += '차단 사유 : ' + band_d[0][2]
                if data[0][0] != 'O':
                    wsdsaf = ''
                    #end += '<li>' + load_lang('login_able') + ' (' + load_lang('not_sure') + ')</li>'



            curs.execute("select login, end, why from ban where ((end > ? and end like '2%') or end = '') and block = ?", [get_time(), ip])
            ban_d = curs.fetchall()
            if ban_d:
                #end += '<li>' + load_lang('type') + ' : ban</li>'
                if ban_d[0][1] == '':
                    end += '차단 만료일 : 무기한<br>'
                else:
                    end += '차단 만료일 : ' + ban_d[0][1] + '<br>'
                end += '차단 사유 : ' + ban_d[0][2]
                if data[0][0] != 'O':
                    sadAD = 'sw'
                    #end += '<li>' + load_lang('login_able') + ' (' + load_lang('not_sure') + ')</li>'

                #end += '<hr class=\"main_hr\">'

        return easy_minify(flask.render_template(skin_check(), 
            imp = [load_lang('error'), wiki_set(1), custom(), other2([0, 0])],
            data = '<div style="font-size: 1.75em;margin-bottom: .5714em;font-weight: 600;">' + end + '</div>',
            menu = 0
        ))
    else:
        error_data = re.search('\/error\/([0-9]+)', data)
        if error_data:
            num = int(error_data.groups()[0])
            if num == 1:
                data = load_lang('no_login_error')
            elif num == 2:
                data = load_lang('no_exist_user_error')
            elif num == 3:
                data = load_lang('authority_error')
            elif num == 4:
                data = load_lang('no_admin_block_error')
            elif num == 6:
                data = load_lang('same_id_exist_error')
            elif num == 7:
                data = load_lang('long_id_error')
            elif num == 8:
                data = load_lang('id_char_error') + ' <a href="/name_filter">(' + load_lang('id') + ' ' + load_lang('filter') + ')</a>'
            elif num == 9:
                data = load_lang('file_exist_error')
            elif num == 10:
                data = load_lang('password_error')
            elif num == 11:
                data = load_lang('topic_long_error')
            elif num == 12:
                data = load_lang('email_error')
            elif num == 13:
                data = load_lang('recaptcha_error')
            elif num == 14:
                data = load_lang('file_extension_error')
            elif num == 15:
                data = load_lang('edit_record_error')
            elif num == 16:
                data = load_lang('same_file_error')
            elif num == 17:
                data = load_lang('file_capacity_error') + ' ' + wiki_set(3)
            elif num == 19:
                data = load_lang('decument_exist_error')
            elif num == 20:
                data = load_lang('password_diffrent_error')
            elif num == 21:
                data = load_lang('edit_filter_error')
            elif num == 22:
                data = load_lang('file_name_error')
            elif num == 23:
                data = load_lang('regex_error')
            elif num == 99:
                data = '해당 메뉴가 정의되어 있지 않습니다.'
            elif num == 1000:
                data = 'already_starred_document'
            elif num == 1001:
                data = 'already_unstarred_document'
            elif num == 1100:
                data = '5자 이상의 요약을 입력해 주세요.'
            elif num == 1101:
                data = '문서 삭제에 대한 안내를 확인해 주세요.'
            elif num == 1200:
                data = 'disable_user_document'
            elif num == 3000:
                data = '조건이 틀리거나 사용할 수 없거나 존재하지 않습니다.'
            elif num == 3001:
                data = '구현되지 않았습니다.'
            elif num == 5000:
                data = '이 스킨은 설정 기능을 지원하지 않습니다.'
            else:
                data = '???'

            return easy_minify(flask.render_template(skin_check(), 
                imp = ['스킨 설정', wiki_set(1), custom(), other2([0, 0])],
                data = '' + data + '',
                menu = 0
            )), 401
        else:
            return redirect('/')
