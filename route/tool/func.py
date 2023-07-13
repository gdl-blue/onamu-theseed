import os
import sys
from datetime import date
import platform
import datetime
import urllib
import socket
from datetime import datetime, timedelta

advCount = 28

import random



def rndval(choice = '0123456789', count = 6):
    return ''.join(random.choice(choice) for i in range(count))

def generateRandomWords():
    if random.randint(0, 10000)/100 <= 0.1:
        if random.randint(0, 100) <= 30:
            a = ["귀엽고", "외롭고", "말썽꾸러기", "초록", "아기", "공룡"]
            b = ["졸리고", "슬프고", "행복하고", "편안한"]
            c = ["알수없는", "신속한", "초능력"]
            d = ["둘리"]

            return random.choice(a) + random.choice(b) + random.choice(c) + random.choice(d)
        else:
            a = ["Cute", "Lonely", "Troublemaker", "Green", "Baby", "Dinosaur"]
            b = ["Sleepy", "Sad", "Upset", "Happy", "Sleeping", "Relaxed"]
            c = ["Unknown", "Magician", "Fast", "Magical"]
            d = ["Dooly"]

            return random.choice(a) + random.choice(b) + random.choice(c) + random.choice(d)
    else:
        return generateRandomWords2()

def generateRandomWords2():
    a = [
        'A',
        'The'
    ]

    b = [
        "Sleepy",
        "Giddy",
        "Smooth",
        'Beautiful',
        'Foamy',
        'Frightened',
        'Lazy',
        'Wonderful',
        'Happy',
        'Sad',
        'Broken',
        'Angry',
        'Mad',
        'Upset',
        'Red',
        'Blue',
        'Yellow',
        'Impossible',
        'Working',
        'Pretty',
        'Relaxed',
        'Cold',
        'Warm',
        'Hot',
        'Hard',
        'Loud',
        'Quiet',
        'New',
        'Old',
        'Clean',
        'Washable',
        'Open',
        'Closed',
        'Outdated',
        'Fixed',
        'Living',
        'Locked',
        'Unused',
        'Used',
        'Sold',
        'Sharp',
        'Smashed',
        'Crazy',
        'Free',
        'Fancy',
        'Ugly',
        'Big',
        'Small',
        'Fast',
        'Ugly',
        'Slow',
        'Dirty',
        'Unclassifiable',
        'Cloudy',
        'Solid',
        'Different',
        'Hungry',
        'Thirsty',
        'Boorish',
        'Funny',
        'Puffy',
        'Greasy',
        'Efficacious',
        'Functional',
        'Undesirable',
        'Naughty',
        'Gray',
        'Busy',
        'Acceptable',
        'Stormy',
        'Noisy'
    ]

    c = [
        'And'
    ]

    d = [
        "Station",
        "Discount",
        'Deer',
        "Soup",
        "Ice",
        "Recorder",
        "VPN",
        "Installer",
        "Uninstaller",
        "Bot",
        "Robot",
        "Power",
        "Point",
        "Music",
        'Event',
        'Cat',
        'Dog',
        'Phone',
        'Bush',
        'Music',
        'Picture',
        'Lion',
        'Angle',
        'Horse',
        'Mouse',
        'Pencil',
        'Box',
        'Bag',
        'Backpack',
        'Chicken',
        'CD',
        'DVD',
        'Diskette',
        'FloppyDisk',
        'Drive',
        'CPU',
        'Water',
        'Glass',
        'Memory',
        'USB',
        'Drive',
        'Number',
        'Letter',
        'Fan',
        'BIOS',
        'Video',
        'Button',
        'Trash',
        'Bottle',
        'Cylinder',
        'Ball',
        'Key',
        'Door',
        'Plug',
        'Flask',
        'Cable',
        'Radio',
        'File',
        'Disk',
        'Camera',
        'Titan',
        'Ash',
        'Tree',
        'Plank',
        'Script',
        'Day',
        'Car',
        'ATV',
        'Healer',
        'Fox',
        'Wolf',
        'Carrot',
        'Steak',
        'Mushroom',
        'Bandages',
        'Berry',
        'Tea',
        'Charcoal',
        'Limestone',
        'Iron',
        'Bar',
        'Nail',
        'Seed',
        'Fiber',
        'Leather',
        'Fur',
        'Aluminum',
        'Tungsten',
        'Transmission',
        'Wheel',
        'Fork',
        'Engine',
        'Transistor',
        'Plastic',
        'Wrench',
        'Gasoline',
        'Oil',
        'Pickaxe',
        'Hammer',
        'Campfire',
        'Garden',
        'Furnace',
        'Tower',
        'Houseplant',
        'Shirt',
        'Sneakers',
        'Helicopter',
        'Trap',
        'Card',
        'Jar',
        'Toy',
        'Jet',
        'Plane',
        'Statement',
        'Dimension',
        'Toothpaste',
        'Railway',
        'Year',
        'Stew',
        'Farm',
        'Zipper',
        'Horses',
        'Can',
        'Cabbage',
        'Eyes',
        'Motion',
        'Uncle',
        'Teeth',
        'Birthday',
        'Downtown'
    ]

    if rndval(count = 1) == '1' or rndval(count = 1) == '2': #20% 확률
        pa = random.choice(b)
        pb = random.choice(b)
        pc = random.choice(b)
        pd = random.choice(d)

        if pa == pb:
            pb = "Soft"
        if pa == pc:
            pc = "Free"
        return pa + pb + pc + pd
    else:
        #포인타 아님
        pa = random.choice(a)
        pb = random.choice(b)
        pc = random.choice(c)
        pd = random.choice(b)
        pe = random.choice(d)
        if pb[0] in ['A', 'E', 'O', 'U', 'I']:
            if pa == 'A':
                pa = 'An'
        if pd == pb:
            pd = 'Soft'
        return pa + pb + pc + pd + pe

#https://stackoverflow.com/questions/39358869/check-if-an-ip-is-within-a-range-of-cidr-in-python/39358930
from ipaddress import ip_network, ip_address

def ipInCIDR(ip, cidr):
    #net = ip_network("1.1.0.0/16")
    #print(ip_address("1.1.2.2") in net)    # True

    net = ip_network(cidr)
    if ip_address(ip) in net:
        return 1
    else:
        return 0



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
        #import request
        import threading
        import logging
        import random
        import flask
        import json
        import html
        import re
        from PIL import Image, ImageDraw, ImageFont
        from flask import *

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

import base64
from io import BytesIO


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

def getwiki():
    try:
        curs.execute("select db from subwikis where id = ?", [flask.session['wiki']])

        return sqlite3.connect(curs.fetchall()[0][0] + '.db', check_same_thread = False)
    except:
        return conn


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
    if re.search('^사용자:', title):
        ns = '사용자'
    elif re.search('^분류:', title):
        ns = '분류'
    elif re.search('^틀:', title):
        ns = '틀'
    elif re.search('^휴지통:', title):
        ns = '휴지통'
    elif re.search('^파일:', title):
        ns = '파일'
    elif re.search('^' + wiki_set()[0] + ':', title):
        ns = wiki_set()[0]
    else:
        ns = '문서'
    perm = getacl(title, 'read')
    if perm == 0:
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

def sha3(data):
    if sys.version_info < (3, 6):
        return sha3.sha3_256(bytes(data, 'utf-8')).hexdigest()
    else:
        return hashlib.sha3_256(bytes(data, 'utf-8')).hexdigest()

def sha256(data):
    return hashlib.sha256(bytes(data, 'utf-8')).hexdigest()

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

def SQLexec(command, args = None):
    retval = None;

    if args:
        curs.execute(command, args);
    else:
        curs.execute(command);

    try:
        retval = curs.fetchall();
    except:
        pass;

    return retval;

def getNamespaces(typ = 'as list', customOnly = False, builtinOnly = False, unuseableOnly = False, useableOnly = False, fileOnly = False, notFileOnly = False, nologOnly = False):
    if customOnly == True:
        nsList = [''.join((i)) for i in SQLexec('select namespace from namespaces')]
    elif builtinOnly == True:
        nsList = ['문서', '틀', '분류', '파일', '외부파일', '사용자', '특수기능', getConfig('name'), '토론', '휴지통', '투표']
    elif unuseableOnly:
        nsList = ['외부파일', '특수기능', '토론', '투표'] + [''.join((i)) for i in SQLexec("select namespace from namespaces where unuseable = '1'")]
    elif useableOnly:
        nsList = ['문서', '틀', '분류', '파일', '사용자', getConfig('name'), '휴지통'] + [''.join((i)) for i in SQLexec("select namespace from namespaces where not unuseable = '1'")]
    elif fileOnly:
        nsList = ['외부파일', '파일'] + [''.join((i)) for i in SQLexec("select namespace from namespaces where isfile = '1'")]
    elif notFileOnly:
        nsList = ['문서', '틀', '분류', '사용자', '특수기능', getConfig('name'), '토론', '휴지통', '투표'] + [''.join((i)) for i in SQLexec("select namespace from namespaces where not isfile = '1'")]
    elif nologOnly:
        nsList = ['사용자'] + [''.join((i)) for i in SQLexec("select namespace from namespaces where nolog = '1'")]
    else:
        nsList = ['문서', '틀', '분류', '파일', '외부파일', '사용자', '특수기능', getConfig('name'), '토론', '휴지통', '투표'] + [''.join((i)) for i in SQLexec('select namespace from namespaces')]

    if typ == 'as list':
        return nsList
    elif typ == 'as combobox options':
        retval = ''
        for namespace in nsList:
            retval += '<option value="' + html.escape(namespace) + '">' + html.escape(namespace) + '</option>'
        return retval;

def getNamespace(rawNS):
    if rawNS in getNamespaces():
        return rawNS
    else:
        return '문서'

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

def loadLang(k = None, e = None):
    curs.execute("select data from user_set where id = ? and name = 'lang'", [ip_check()])
    try:
        userLang = curs.fetchall()[0][0]
    except:
        userLang = 'ko-KR'
    if k and e:
        if userLang == 'ko-KR':
            return k
        elif userLang == 'en-US':
            return e
        else:
            return k
    elif k:
        return k
    elif e:
        return e

def edit_button():
    return '''
    <span class=btn-group id=editTools>
        <a class="btn btn-secondary btn-sm" href="javascript:insertMarkup('\\'\\'\\'ABC\\'\\'\\'', '\\'\\'\\'', '\\'\\'\\'');">''' + loadLang('굵게', 'Bold') + '''</a>
        <a class="btn btn-secondary btn-sm" href="javascript:insertMarkup('\\'\\'ABC\\'\\'', '\\'\\'', '\\'\\'');">''' + loadLang('기울게', 'Italic') + '''</a>
        <a class="btn btn-secondary btn-sm" href="javascript:insertMarkup('__ABC__', '__', '__');">''' + loadLang('밑줄', 'Underline') + '''</a>
        <a class="btn btn-secondary btn-sm" href="javascript:insertMarkup('--ABC--', '--', '--');">''' + loadLang('취소선', 'Strikethrough') + '''</a>
        <a class="btn btn-secondary btn-sm" href="javascript:insertMarkup('[[URL]]', '[[', ']]');">''' + loadLang('링크', 'Link') + '''</a>
        <a class="btn btn-secondary btn-sm" href="javascript:insertMarkup('\\n\\n== TITLE ==\\n', '== ', ' ==');">''' + loadLang('문단', 'Paragraph') + '''</a>
        <a class="btn btn-secondary btn-sm" href="javascript:insertMarkup('[[파일:FILENAME]]', '[[파일:', ']]');">''' + loadLang('그림', 'Image') + '''</a>
        <a class="btn btn-secondary btn-sm" href="javascript:insertMarkup('[include(틀:NAME)]', '[include(틀:', ')]');">''' + loadLang('틀', 'Template') + '''</a>
        <a class="btn btn-secondary btn-sm" href="javascript:insertMarkup('{{{#색 내용}}}', '{{{#색 ', '}}}');">''' + loadLang('글자색', 'Color') + '''</a>
        <a class="btn btn-secondary btn-sm" href="javascript:insertMarkup('{{{+단계 내용}}}', '{{{+단계 ', '}}}');">''' + loadLang('큰글자', 'SizeUp') + '''</a>
        <a class="btn btn-secondary btn-sm" href="javascript:insertMarkup('{{{-단계 내용}}}', '{{{-단계 ', '}}}');">''' + loadLang('작은글자', 'SizeDown') + '''</a>
    </span>
    '''

editButtons = edit_button

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

def skin_check(set_n = 0, s = None):
    skin = 'buma'

    conn.commit()

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
    oyd = (datetime.datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")

    curs.execute("delete from ua_d where today < ?", [oyd])

    # 도우너=사용자이름 둘리=비밀번호해시

    if not('state' in flask.session):
        if 'dooly' in flask.request.cookies and 'doornot' in flask.request.cookies:
            pwhash = flask.request.cookies.get('dooly')
            username = flask.request.cookies.get('doornot')

            curs.execute("select key from token where username = ? COLLATE NOCASE", [username])
            try:
                usrtkn = curs.fetchall()[0][0]

                curs.execute("select pw from user where id = ? COLLATE NOCASE", [username])
                shusrpw = curs.fetchall()[0][0]

                if pwhash == sha3(sha3(sha3(sha224(sha224(sha3(sha224(sha3(shusrpw + sha3(usrtkn))))))))):
                    curs.execute("select id from user where id = ? COLLATE NOCASE", [username])
                    flask.session['state'] = 1
                    flask.session['id'] = curs.fetchall()[0][0]
            except:
                pass
    else:
        if 'dooly' in flask.request.cookies and 'doornot' in flask.request.cookies:
            pwhash = flask.request.cookies.get('dooly')
            username = flask.request.cookies.get('doornot')

            curs.execute("select key from token where username = ? COLLATE NOCASE", [username])
            try:
                usrtkn = curs.fetchall()[0][0]

                curs.execute("select pw from user where id = ? COLLATE NOCASE", [username])
                shusrpw = curs.fetchall()[0][0]

                if pwhash == sha3(sha3(sha3(sha224(sha224(sha3(sha224(sha3(shusrpw + sha3(usrtkn))))))))):
                    #쿠키가 올바름
                    pass
                else:
                    curs.execute("delete from token where username = ? COLLATE NOCASE", [username])
                    flask.session.pop('state', None)
                    flask.session.pop('id', None)
            except:
                curs.execute("delete from token where username = ? COLLATE NOCASE", [username])
                flask.session.pop('state', None)
                flask.session.pop('id', None)

    if set_n == 0:
        if s:
            return './views/' + skin + '/settings.html'
        return './views/' + skin + '/index.html'
    else:
        return skin

def next_fix(link, num, page, end = 50):
    list_data = '''
        <div class="btn-group" role="group">
        <a class="btn btn-secondary btn-sm disabled"><span class="icon ion-chevron-left"></span>&nbsp;&nbsp;Past</a>
        <a class="btn btn-secondary btn-sm disabled">Next&nbsp;&nbsp;<span class="icon ion-chevron-right"></span></a>
        </div>'''

    if num == 1:
        if len(page) == end:
            list_data = '''
                <div class="btn-group" role="group">
                <a class="btn btn-secondary btn-sm disabled"><span class="icon ion-chevron-left"></span>&nbsp;&nbsp;Past</a>
                <a class="btn btn-secondary btn-sm" href="''' + link + str(num + 1) + '''">Next&nbsp;&nbsp;<span class="icon ion-chevron-right"></span></a>
                </div>'''
    elif len(page) != end:
        list_data = '''
            <div class="btn-group" role="group">
            <a class="btn btn-secondary btn-sm" href="''' + link + str(num - 1) + '''"><span class="icon ion-chevron-left"></span>&nbsp;&nbsp;Past</a>
            <a class="btn btn-secondary btn-sm disabled">Next&nbsp;&nbsp;<span class="icon ion-chevron-right"></span></a>
            </div>'''
    else:
        list_data = '''
            <div class="btn-group" role="group">
            <a class="btn btn-secondary btn-sm" href="''' + link + str(num - 1) + '''"><span class="icon ion-chevron-left"></span>&nbsp;&nbsp;Past</a>
            <a class="btn btn-secondary btn-sm" href="''' + link + str(num + 1) + '''">Next&nbsp;&nbsp;<span class="icon ion-chevron-right"></span></a>
            </div>'''
    return list_data

def next_fix_f(link, num, page, end = 50):
    list_data = '''
        <div class="btn-group" role="group">
        <a class="btn btn-secondary btn-sm" href="''' + link + str(num - 1) + '''"><span class="icon ion-chevron-left"></span>&nbsp;&nbsp;Past</a>
        <a class="btn btn-secondary btn-sm" href="''' + link + str(num + 1) + '''">Next&nbsp;&nbsp;<span class="icon ion-chevron-right"></span></a>
        </div>'''

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

def getConfig(q, d = ''):
    curs.execute('select data from other where name = ?', [q])
    cd = curs.fetchall()
    if cd:
        return cd[0][0]
    else:
        return d

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

def user_isadmin(num = None, name = None):
    ip = name
    what = None

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

def getperm(permname, username = None):
    perm = permname
    if permname == 'update_thread_topic':
        perm = 'utt'
    if permname == 'update_thread_document':
        perm = 'utd'
    if permname == 'update_thread_status':
        perm = 'uts'
    if permname == 'delete_thread':
        perm = 'dt'
    if permname == 'ipacl':
        perm = 'ipa'
    if permname == 'hide_thread_comment':
        perm = 'htc'
    if permname == 'editable_other_user_document':
        perm = 'eou'
    if permname == 'disable_two_factor_login':
        perm = 'dtf'
    if permname == 'no_force_recaptcha':
        perm = 'nfr'

    if permname == 'suspend_account':
        if username:
            return user_isadmin(1, username)
        else:
            return admin_check(1)
    elif permname == 'login_history':
        if username:
            return user_isadmin(4, username)
        else:
            return admin_check(4)
    elif permname == 'admin':
        if username:
            return user_isadmin(5, username)
        else:
            return admin_check(5)
    elif permname == 'hidel':
        if username:
            return user_isadmin(6, username)
        else:
            return admin_check(6)
    elif permname == 'grant':
        if username:
            return user_isadmin(7, username)
        else:
            return admin_check(7)
    elif permname == 'owner' or permname == 'developer':
        if username:
            return user_isadmin(None, username)
        else:
            return admin_check()
    else:
        if username:
            curs.execute("select perm from grant where perm = ? and user = ?", [permname, username])
        else:
            curs.execute("select perm from grant where perm = ? and user = ?", [permname, ip_check()])

        if curs.fetchall():
            return 1
        else:
            return 0

def wiki_set(num = 1):
    if num == 1:
        data_list = []

        curs.execute('select data from other where name = ?', ['name'])
        db_data = curs.fetchall()
        if db_data and db_data[0][0] != '':
            data_list += [db_data[0][0]]
        else:
            data_list += ['Wiki']

        curs.execute('select data from other where name = "license"')
        db_data = curs.fetchall()
        if db_data and db_data[0][0] != '':
            data_list += [db_data[0][0]]
        else:
            data_list += ['CC 0']

        data_list += ['', '']

        curs.execute('select data from other where name = "logo"')
        db_data = curs.fetchall()
        if db_data and db_data[0][0] != '':
            data_list += [db_data[0][0]]
        else:
            data_list += [data_list[0]]

        curs.execute("select data from user_set where id = ? and name = 'wallpaper_code'", [ip_check()])
        mycolor = curs.fetchall()
        if not(mycolor):
            bgclrcss = ''
        else:
            if mycolor[0][0] != '-':
                bgclrcss = '<style>body { background: ' + mycolor[0][0] + ' !important; }</style>'
            else:
                bgclrcss = ''

        advstyle = ''

        for i in range(1, advCount + 1):
            curs.execute("select data from user_set where id = ? and name = 'advstyle" + str(i) + "'", [ip_check()])
            advstylec = curs.fetchall()
            if not(advstylec):
                advstyle += '<style id=CSS-' + str(i) + '></style>'
            else:
                advstyle += '<style id=CSS-' + str(i) + '>' + advstylec[0][0] + '</style>'

        #이것은 코드수정으로 바꿀 수 있지만 엔진 작동에 기초적인 것이니 삭제하지 않기를 바란다.
        defhead = advstyle + bgclrcss + '''
            <!--[if lte IE 10]> <script src="https://code.jquery.com/jquery-1.8.0.min.js"></script> <![endif]-->
            <script type="text/javascript" src="/js/do_preview.js"></script>
            <script type="text/javascript" src="/js/insert_data.js"></script>
            <script src="/js/topic_list_load.js"></script>
            <script src="/js/topic_main_load.js"></script>
            <script src="/js/topic_plus_load.js"></script>
            <script src="/js/topic_reload.js"></script>
            <script src="/js/insert_data.js"></script>
            <!--[if lte IE 10]> <script src="https://code.jquery.com/jquery-1.8.0.min.js"></script> <![endif]-->
            <script src="/js/jquery.min.js"></script>
            <script src="/js/jquery-ui.min.js"></script>
            <!--[if lte IE 10]> <script src="https://code.jquery.com/jquery-1.8.0.min.js"></script> <![endif]-->

            <style>
                a.tab-link {
                    text-decoration: none;
                    color: currentcolor;
                    margin-left: 15px;
                    float: right;
                }
            </style>

            <script>
            /*
                	    https://stackoverflow.com/questions/11076975/insert-text-into-textarea-at-cursor-position-javascript
                	    https://stackoverflow.com/questions/717224/how-to-get-selected-text-in-textarea
                	    https://www.codeproject.com/Questions/897645/Replacing-selected-text-HTML-JavaScript
                	    https://snipplr.com/view/8406/how-to-replace-selected-textarea-value-using-javascript/
                	*/
                	function getSel(eid)
                    {
                        var txtarea = document.getElementById(eid);
                        var start = txtarea.selectionStart;
                        var finish = txtarea.selectionEnd;
                        var sel = txtarea.value.substring(start, finish);
                        return sel;
                    }

                    /*
                    function makeBold(){
                        var span = '<span style="font-weight:bold;">' + highlight + '</span>';

                        var selected, range;
                        if (window.getSelection) {
                            selected= window.getSelection();
                            if (selected.rangeCount) {
                                range = selected.getRangeAt(0);
                                range.deleteContents();
                                range.insertNode(document.createTextNode(span));
                            }
                        } else if (document.selection && document.selection.createRange) {
                            range = document.selection.createRange();
                            range.text = span;
                        }
                    }
                    */

                    /*
                    var textarea = document.getElementById("textarea");

                    if(document.selection)
        			{
        				textarea.focus();
        				var sel = document.selection.createRange();
        				sel.text = '<b>' + sel.text + '</b>';
        			}




                    // code for Mozilla

                      var textarea = document.getElementById("textarea");

                      var len = textarea.value.length;
                       var start = textarea.selectionStart;
                       var end = textarea.selectionEnd;
                       var sel = textarea.value.substring(start, end);

                       // This is the selected text and alert it
                       alert(sel);

                      var replace = '<b>' + sel + '<b>';

                      // Here we are replacing the selected text with this one
                     textarea.value =  textarea.value.substring(0,start) + replace + textarea.value.substring(end,len);
                    */

                    function insertMarkup(myValue, s = '', e = '') {
                        var editorID = 'content';

                        if(getSel(editorID) != "" && s != '' && e != '') {
                            var textarea = document.getElementById(editorID);

                            if(document.selection)
                			{
                				textarea.focus();
                				var sel = document.selection.createRange();
                                sel.text = s + sel.text + e;
                			}

                		;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

                            var textarea = document.getElementById(editorID);

                            var len = textarea.value.length;
                            var start = textarea.selectionStart;
                            var end = textarea.selectionEnd;
                            var sel = textarea.value.substring(start, end);


                            var replace = s + sel + e;

                            textarea.value =  textarea.value.substring(0,start) + replace + textarea.value.substring(end,len);

                            return;
                        }

                        var myField = document.getElementById(editorID);
                        if (document.selection) {
                            myField.focus();
                            sel = document.selection.createRange();
                            sel.text = myValue;
                        }
                        else if (myField.selectionStart || myField.selectionStart == '0') {
                            var startPos = myField.selectionStart;
                            var endPos = myField.selectionEnd;
                            myField.value = myField.value.substring(0, startPos)
                                + myValue
                                + myField.value.substring(endPos, myField.value.length);
                        } else {
                            myField.value += myValue;
                        }
                    }
            </script>

            <script src="/js/diffview.js"></script>
            <script src="/js/difflib.js"></script>
            <script>


            function diffUsingJS(viewType) {
            	"use strict";
            	var byId = function (id) { return document.getElementById(id); },
            		base = difflib.stringAsLines(byId("baseText").value),
            		newtxt = difflib.stringAsLines(byId("newText").value),
            		sm = new difflib.SequenceMatcher(base, newtxt),
            		opcodes = sm.get_opcodes(),
            		diffoutputdiv = byId("diffoutput"),
            		contextSize = byId("contextSize").value;

            	diffoutputdiv.innerHTML = "";
            	contextSize = contextSize || null;

            	diffoutputdiv.appendChild(diffview.buildView({
            		baseTextLines: base,
            		newTextLines: newtxt,
            		opcodes: opcodes,
            		baseTextName: "r" + byId("olderrev").value,
            		newTextName: "r" + byId("rev").value,
            		contextSize: contextSize,
            		viewType: viewType
            	}));
            }


            </script>
            <script src="/js/theseed-onamu.js"></script>
            <script src="/js/intersection-observer.js"></script>
            <script type="text/javascript" src="/js/dateformatter.js"></script>
            <meta name=generator content="onamu-theseed">
            <link rel="shortcut icon" type="image/png" href="/views/main_css/file/favicon.png" />
                        <SCRIPT>
                        jQuery(function() {
                    		$("time").each(function () {
                    			var format = $(this).attr("data-format");
                    			var time = $(this).attr("datetime");

                    			if (!format || !time) {
                    				return;
                    			}
                    			$(this).text(formatDate(new Date(time), format));
                    		});
                    	});
                        </SCRIPT>

            <script>
                function userLinkClicked(event,lnk) {
                    if(event.shiftKey) {
                        window.location.href = "/contribution/author/" + lnk.innerHTML + "/document";
                        return false;
                    }
                }
            </script>

            <STYLE>
            .wiki-category ul {
                margin-top: 0px;
            }
            .tab-pane {
                display: none;
            }
            .tab-pane.active {
                display: block;
            }

            /* HTML5 미만용 태그 호환용 */
            font {
                font-family: attr(face);
                color: attr(color);
                font-size: attr(size);
            }

            strike {
                text-decoration: line-through;
            }

            table[align=right] {
                float: right;
            }

            table[align=center] {
                float: center;
            }

            big {
                font-size: larger;
            }

            menu, dir {
                display: block;
                list-style-type: disc;
                -webkit-margin-before: 1em;
                -webkit-margin-after: 1em;
                -webkit-margin-start: 0px;
                -webkit-margin-end: 0px;
                -webkit-padding-start: 40px;
            }

            center {
                display: block;
                text-align: center;
            }

            tt {
                font-family: monospace;
            }
            </STYLE>

            <STYLE>
            .wiki-category-blur {
                filter: blur(3px);
                -webkit-filter: blur(3px);
            }
            .wiki-category-blur:hover {
                filter: inherit;
                -webkit-filter: inherit;
            }
            input[type=radio] {
                width: 20px !important;
            }
            </STYLE>
            <link rel="stylesheet" href="/css/wiki.css">
            <link rel="stylesheet" href="/css/diffview.css">
            <script>
            /* 포트란 문법강조 */
            /* https://stackoverflow.com/questions/280793/case-insensitive-string-replacement-in-javascript */
            function highlightWords( line, word )
            {
                 var regex = new RegExp( '(' + word + ')', 'gi' );
                 return line.replace( regex, '<span style="color: #00f; font-weight: 700;">$1</span>' );
            }

            function highlightFuncs( line, word )
            {
                 var regex = new RegExp( '(' + word + ')', 'gi' );
                 return line.replace( regex, '<span style="color: #0A0; font-weight: 700;">$1</span>' );
            }

            function highlightOps( line, word )
            {
                 var regex = new RegExp( '(' + word + ')', 'gi' );
                 return line.replace( regex, '<span style="color: #F00; font-weight: 700;">$1</span>' );
            }

            function highlightStrs( line, word )
            {
                 var regex = new RegExp( '(' + word + ')', 'gi' );
                 return line.replace( regex, '<span style="color: #0A0; font-weight: 740;">$1</span>' );
            }

            $(function() {
            	var rawCode = document.querySelector("code.fortran");

            	rawCode.innerHTML = highlightFuncs(rawCode.innerHTML, 'char');
            	rawCode.innerHTML = highlightFuncs(rawCode.innerHTML, 'float');
            	rawCode.innerHTML = highlightFuncs(rawCode.innerHTML, 'int1');
            	rawCode.innerHTML = highlightFuncs(rawCode.innerHTML, 'int2');
            	rawCode.innerHTML = highlightFuncs(rawCode.innerHTML, 'int4');
            	rawCode.innerHTML = highlightFuncs(rawCode.innerHTML, 'int8');
            	rawCode.innerHTML = highlightFuncs(rawCode.innerHTML, 'int16');
            	rawCode.innerHTML = highlightFuncs(rawCode.innerHTML, 'mod');
            	rawCode.innerHTML = highlightFuncs(rawCode.innerHTML, 'sqrt');
            	rawCode.innerHTML = highlightFuncs(rawCode.innerHTML, 'abs');
            	rawCode.innerHTML = highlightFuncs(rawCode.innerHTML, 'break');
            	rawCode.innerHTML = highlightFuncs(rawCode.innerHTML, 'system');

            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'program');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'if');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'block');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'while');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'do');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'forall');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'end');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'select');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'case');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'selectcase');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'value');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'result');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'function');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'integer');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'read');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'double');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'character');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'else');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'elseif');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'read');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'write');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'print');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'format');
            	rawCode.innerHTML = highlightWords(rawCode.innerHTML, 'continue');

            	rawCode.innerHTML = highlightOps(rawCode.innerHTML, '[*]');
                    rawCode.innerHTML = highlightOps(rawCode.innerHTML, '[(]');
                    rawCode.innerHTML = highlightOps(rawCode.innerHTML, '[)]');
                    rawCode.innerHTML = highlightOps(rawCode.innerHTML, '[,]');
                    rawCode.innerHTML = highlightOps(rawCode.innerHTML, '[.]');

            });
            </script>
            <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/highlight.min.js"></script>
            <script>
                $(document).on('click', '.nav-link', function() {
                    $(this).parent().parent().children('.nav-item').children('.nav-link').removeClass('active');
                    $(this).addClass('active');
                    $(this).parent().parent().next().children('.tab-pane').removeClass('active');
                    $(this).parent().parent().next().children('.tab-pane' + $(this).attr('href')).addClass('active');
                });
            </script>
            <script>
                $(document).on('click', '.modal-dialog button[data-dismiss="modal"]', function() {
                    $(this).parent().parent().parent().parent().parent().hide();
                });
                $(document).on('click', 'span[data-toggle="modal"] input[type=button]', function() {
                    $($(this).parent().attr('data-target')).show();
                });
            </script>
            <!--[if lte IE 10]> <script src="https://code.jquery.com/jquery-1.8.0.min.js"></script> <![endif]-->
        '''
        curs.execute("select data from other where name = 'head' and coverage = ?", [skin_check(1)])
        db_data = curs.fetchall()
        if db_data and db_data[0][0] != '':
            data_list += [defhead + db_data[0][0]]
        else:
            curs.execute("select data from other where name = 'head' and coverage = ''")
            db_data = curs.fetchall()
            if db_data and db_data[0][0] != '':
                data_list += [defhead + db_data[0][0]]
            else:
                data_list += [defhead]

        data_list += [getConfig('site_notice', '')]

        data_list += [getperm]

        data_list += [get_time()]

        return data_list

    if num == 2:
        var_data = 'FrontPage'

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

def is_ip(id):
    if re.search(".*\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}.*", id):
        return 1
    else:
        return 0



def ip_pas_t(raw_ip, ismember = None, ia = '0'):
    hide = 0

    if ismember and ismember == 'ip':
        curs.execute("select data from other where name = 'ip_view'")
        data = curs.fetchall()
        if data and data[0][0] != '':
            ip = re.sub('((?:(?!\.).)+)$', '*', raw_ip)

            if not admin_check(1):
                hide = 1
        else:
            ip = '<a href="/contribution/ip/' + raw_ip + '/document">' + raw_ip + '</a>'
    elif ismember and ismember == 'author':
        if ia == '1':
            ip = '<a style="font-weight: bold;" href="/w/' + url_pas('사용자:' + raw_ip) + '">' + raw_ip + '</a>'
        else:
            ip = '<a href="/w/' + url_pas('사용자:' + raw_ip) + '">' + raw_ip + '</a>'
    else:
        if re.search("(\.|:)", raw_ip):
            curs.execute("select data from other where name = 'ip_view'")
            data = curs.fetchall()
            if data and data[0][0] != '':
                ip = re.sub('((?:(?!\.).)+)$', '*', raw_ip)

                if not admin_check(1):
                    hide = 1
            else:
                ip = '<a href="/contribution/ip/' + raw_ip + '/document">' + raw_ip + '</a>'
        else:
            if ia == '1':
                ip = '<a style="font-weight: bold;" href="/w/' + url_pas('사용자:' + raw_ip) + '">' + raw_ip + '</a>'
            else:
                ip = '<a href="/w/' + url_pas('사용자:' + raw_ip) + '">' + raw_ip + '</a>'

    return ip

def ip_pas(raw_ip, ismember = None):
    hide = 0

    if ismember and ismember == 'ip':
        curs.execute("select data from other where name = 'ip_view'")
        data = curs.fetchall()
        if data and data[0][0] != '':
            ip = re.sub('((?:(?!\.).)+)$', 'xxx', raw_ip)

            if not admin_check(1):
                hide = 1
        else:
            ip = '<a href="/contribution/ip/' + raw_ip + '/document">' + raw_ip + '</a>'
    elif ismember and ismember == 'author':
        ip = '<strong><a href="/w/' + url_pas('사용자:' + raw_ip) + '" onclick="userLinkClicked(event, this);" class=user-link>' + raw_ip + '</a></strong>'
    else:
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
            ip = '<strong><a href="/w/' + url_pas('사용자:' + raw_ip) + '" onclick="userLinkClicked(event, this);" class=user-link>' + raw_ip + '</a></strong>'


    return ip

def ip_pas_raw(raw_ip):
    return raw_ip

    #이제보니 내가 왜 이 함수를 만들었지

def toplst(name):
    curs.execute("select sub from rd where title = ? order by date desc", [name])

    ud = 0
    for data in curs.fetchall():
        it_p = 0
        curs.execute("select title from rd where title = ? and sub = ? and (stop = 'O' or agree = 'O') order by sub asc", [name, data[0]])
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

    curs.execute("select data from user_set where id = ? and name = 'color'", [ip_check()])
    mycolor = curs.fetchall()
    if not(mycolor):
        try:
            defaultSkinColor = open('./views/' + skin_check(1) + '/dfltcolr.scl', 'r').read()
        except:
            defaultSkinColor = 'default'
        mycolor = [[defaultSkinColor]]

    curs.execute("select perm from grant where user = ? and perm = 'ipa'", [ip_check()])
    if curs.fetchall():
        ipa = 1
    else:
        ipa = 0

    curs.execute("select perm from grant where user = ? and perm = 'arbiter'", [ip_check()])
    if curs.fetchall():
        ar = 1
    else:
        ar = 0

    curs.execute("select perm from grant where user = ? and perm = 'tribune'", [ip_check()])
    if curs.fetchall():
        tr = 1
    else:
        tr = 0

    curs.execute("select perm from grant where user = ? and perm = 'create_vote'", [ip_check()])
    if curs.fetchall():
        cv = 1
    else:
        cv = 0

    spin = '00000000'
    curs.execute("select pin from spin where username = ?", [ip_check()])
    try:
        spin = curs.fetchall()[0][0]
    except:
        spin = '00000000'

    return ['', '', user_icon, user_head, email, user_name, ip_check(), admin_check(1), admin_check(3), admin_check(4), admin_check(5), admin_check(6), admin_check(7), admin_check(), toplst('사용자:' + ip_check()), ipa, ar, tr, cv, mycolor[0][0], str(spin)]

def load_skin(data = '', set_n = 0):
    div2 = ''
    div3 = []
    system_file = ['main_css', 'easter_egg.html']
    hidden_skins = []

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
                if skin_data in hidden_skins:
                    continue
                if not skin_data in system_file:
                    try:
                        dispSkinName = open('./views/' + skin_data + '/dispname.scl', 'r').read()
                    except:
                        dispSkinName = skin_data
                    if data[0][0] == skin_data:
                        div2 += '<option value="' + skin_data + '" selected>' + dispSkinName + ' ' + load_lang('style') + '</option>'
                    else:
                        div2 += '<option value="' + skin_data + '">' + dispSkinName + ' ' + load_lang('style') + '</option>'
        else:
            div2 = []
            for skin_data in os.listdir(os.path.abspath('views')):
                if skin_data in hidden_skins:
                    continue
                if not skin_data in system_file:
                    if data[0][0] == skin_data:
                        div2 = [skin_data] + div2
                    else:
                        div2 += [skin_data]
    else:
        if set_n == 0:
            for skin_data in os.listdir(os.path.abspath('views')):
                if skin_data in hidden_skins:
                    continue
                if not skin_data in system_file:
                    if data == skin_data:
                        div2 += '<option value="' + skin_data + '" selected>' + skin_data + '</option>'
                    else:
                        div2 += '<option value="' + skin_data + '">' + skin_data + '</option>'
        else:
            div2 = []
            for skin_data in os.listdir(os.path.abspath('views')):
                if skin_data in hidden_skins:
                    continue
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

def ban_check(ip = None, tool = None, ipacl = False):
    curs.execute("delete from ban where (end < ? and not end like '0' and not end like '')", [get_time()])
    conn.commit()

    if not ip:
        ip = ip_check()
        if 'state' in flask.session and flask.session['state'] == 1:
            curs.execute("select block from ban where block = ?", [ip])
            if curs.fetchall():
                return 1
            curs.execute("delete from ipacl where (end < ? and not end like '0' and not end like '')", [get_time()])
            conn.commit()
            curs.execute("select ip, al from ipacl")
            for i in curs.fetchall():
                if ipInCIDR(my_ip(), i[0]) == 1:
                    if i[1] == 'N':
                        return 1
                    else:
                        return 0
            return 0
        else:
            curs.execute("delete from ipacl where (end < ? and not end like '0' and not end like '')", [get_time()])
            conn.commit()
            curs.execute("select ip from ipacl")
            #포문/DO문(포트란) 1부터 1000000까지 1초 미만, 1부터 100000000까지 약 10초
            #다른 빠른알고리즘 생각해도 잘 모르겠음
            for i in curs.fetchall():
                if ipInCIDR(ip, i[0]) == 1:
                    return 1
            return 0

        return 0
    if ipacl == True:
        curs.execute("select ip from ipacl")
        #포문/DO문(포트란) 1부터 1000000까지 1초 미만, 1부터 100000000까지 약 10초
        #다른 빠른알고리즘 생각해도 잘 모르겠음
        for i in curs.fetchall():
            if ipInCIDR(ip, i[0]) == 1:
                return 1
        return 0
    else:
        band = re.search("^([0-9]{1,3}\.[0-9]{1,3})", ip)
        if band:
            band_it = band.groups()[0]
        else:
            band_it = '-'

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
            why,
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

def ban_gr_nh(name, end, why, login, blocker, type_d = None):
    now_time = get_time()


    band = ''

    #curs.execute("delete from ban where (end < ? and end like '2%')", [get_time()])



    login = ''



    #curs.execute("insert into rb (block, end, today, blocker, why, band) values (?, ?, ?, ?, ?, ?)", [name, end, now_time, blocker, why, band])
    #curs.execute("insert into ban (block, end, why, band, login) values (?, ?, ?, ?, ?)", [name, r_time, why, band, login])

    #conn.commit()

def ban_lh(name, end, why, login, blocker, type_d = None):
    now_time = get_time()


    band = ''

    #curs.execute("delete from ban where (end < ? and end like '2%')", [get_time()])



    login = ''



    curs.execute("insert into rb (block, end, today, blocker, why, band) values (?, ?, ?, ?, ?, ?)", [name, end, now_time, blocker, why, band])
    #curs.execute("insert into ban (block, end, why, band, login) values (?, ?, ?, ?, ?)", [name, r_time, why, band, login])

    conn.commit()

def rd_plus(title, sub, date, tnum = None):
    if tnum:
        curs.execute("select title from rd where tnum = ?", [tnum])
        if curs.fetchall():
            curs.execute("update rd set date = ? where tnum = ?", [date, tnum])
        else:
            curs.execute("insert into rd (tnum, date) values (?, ?)", [tnum, date])
    else:
        curs.execute("select title from rd where title = ? and sub = ?", [title, sub])
        if curs.fetchall():
            curs.execute("update rd set date = ? where title = ? and sub = ?", [date, title, sub])
        else:
            curs.execute("insert into rd (title, sub, date) values (?, ?, ?)", [title, sub, date])

updateRD = rd_plus

def history_plus(title, data, date, ip, send, leng, t_check = '', ud = 0):
    curs.execute("select id from history where title = ? order by id + 0 desc limit 1", [title])
    id_data = curs.fetchall()

    iii = ''

    if t_check != '':
        iii = '<i>(' + t_check + ')</i>'
    mi = ''
    curs.execute("select id from user where id = ?", [ip])
    if curs.fetchall():
        mi = 'author'
    else:
        mi = 'ip'

    if ip == ip_check():
        if 'state' in flask.session and flask.session['state'] == 1:
            mi = 'author'
        else:
            mi = 'ip'

    if ud == 1:
        mi = 'author'

    curs.execute("insert into history (id, title, data, date, ip, send, leng, hide, i, ismember) values (?, ?, ?, ?, ?, ?, ?, '', ?, ?)", [
        str(int(id_data[0][0]) + 1) if id_data else '1',
        title,
        data,
        date,
        ip,
        send,
        leng,
        iii,
        mi
    ])

addHistory = history_plus

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

def islogin(dummy1 = 0):
    if 'state' in flask.session and flask.session['state'] == 1:
        return 1
    else:
        return 0

#https://stackoverflow.com/questions/24678308/how-to-find-location-with-ip-address-in-python
def ipInfo(addr=''):
    from urllib.request import urlopen
    from json import load
    if addr == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + addr + '/json'
    res = urlopen(url)
    #response from url(if res==None then check connection)
    data = load(res)
    #will load the json response into data
    return data['country']

def getacl(name, typ):
    curs.execute("select perm from grant where perm = ? and user = ?", ['ignore_acl', ip_check()])
    if curs.fetchall():
        return 1

    curs.execute("delete from seedacl where (exp < ? and not exp like '0' and not exp like '')", [get_time()])
    curs.execute("delete from nsacl where (exp < ? and not exp like '0' and not exp like '')", [get_time()])
    conn.commit()
    try:
        ns = getNamespace(name.split(':')[0])
    except:
        ns = '문서'

    perm = 0
    #                    0    1     2     3    4
    curs.execute("select id, type, perm, how, exp from seedacl where name = ? and what = ? and not type = 'comment' and not how = 'none' order by cast(id as integer) asc", [name, typ])
    doca = curs.fetchall()
    curs.execute("select id, type, perm, how, exp from nsacl where ns = ? and what = ? and not type = 'comment' and not how = 'none' order by cast(id as integer) asc", [ns, typ])
    nspa = curs.fetchall()
    if not(nspa):
        nspa = [['1','perm','any','deny','0']]
    if not(doca):
        alt = nspa
    else:
        alt = doca
    for wtc in alt:
        if wtc[1] == 'perm':
            if wtc[2] == 'all' or wtc[2] == 'any':
                if wtc[3] == 'allow':
                    perm = 1
                    break
                else:
                    perm = 0
                    break
            elif wtc[2] == 'blocked_ipacl':
                banned = 0
                curs.execute("select ip, al from ipacl")
                #포문/DO문(포트란) 1부터 1000000까지 1초 미만, 1부터 100000000까지 약 10초
                #다른 빠른알고리즘 생각해도 잘 모르겠음
                for i in curs.fetchall():
                    if ipInCIDR(my_ip(), i[0]) == 1:
                        if i[1] == 'Y' and('state' in flask.session and flask.session['state'] == 1):
                            banned = 0
                        else:
                            banned = 1
                        break

                if wtc[3] == 'allow':
                    if banned == 1:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if banned == 1:
                        if islogin(conn) == 1:
                            curs.execute("select block from ban where block = ? and login = 'O'", [my_ip()])
                            if curs.fetchall():
                                continue
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'suspend_account':
                if not('state' in flask.session):
                    continue

                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if ban_check() == 1:
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'admin':
                if wtc[3] == 'allow':
                    if admin_check(5) == 1:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if admin_check(5) == 1:
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'email':
                curs.execute("select data from user_set where id = ? and name = 'email'", [ip_check()])
                ismail = curs.fetchall()
                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if ismail:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if ismail:
                        perm = 0
                        break
                    else:
                        continue
            elif re.search("\d{1,}[_][e][d][i][t]", wtc[2]):
                day = int(wtc[2].replace('_edit', ''))
                curs.execute("select count(title) from history where ip = ?", [ip_check()])
                count = curs.fetchall()
                if count:
                    ctc = count[0][0]
                else:
                    ctc = 0
                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if ctc > day - 1:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if ctc > day - 1:
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'match_username_and_document_title':
                doct = name.replace(ns + ':', '')
                m = re.search("^(.*)\/(.*)$", doct)
                if m:
                    doct = m.groups()[0]
                if wtc[3] == 'allow':
                    if doct == ip_check() and islogin(conn) == 1:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if doct == ip_check() and islogin(conn) == 1:
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'match_ip_and_document_title':
                doct = name.replace(ns + ':', '')
                m = re.search("^(.*)\/(.*)$", doct)
                if m:
                    doct = m.groups()[0]
                if wtc[3] == 'allow':
                    if doct == my_ip():
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if doct == my_ip():
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'contributor':
                curs.execute("select ip from history where ip = ?", [ip_check()])
                x = curs.fetchall()
                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if x:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if x:
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'document_contributor':
                curs.execute("select ip from history where title = ? and ip = ?", [name, ip_check()])
                y = curs.fetchall()
                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if y:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if y:
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'document_last_contributed':
                curs.execute("select ip from history where title = ? order by date desc", [name])
                result = curs.fetchall()
                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if result and result[0][0] == ip_check():
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if result and result[0][0] == ip_check():
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'document_creator':
                curs.execute("select ip from history where title = ? and ip = ? and id = '1'", [name, ip_check()])
                y = curs.fetchall()
                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if y:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if y:
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'user' or wtc[2] == 'member':
                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if islogin(conn) == 1:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if islogin(conn) == 1:
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'ip':
                if wtc[3] == 'allow':
                    if islogin(conn) != 1:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if islogin(conn) != 1:
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'login_history':
                if wtc[3] == 'allow':
                    if admin_check(4) == 1:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if admin_check(4) == 1:
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'developer':
                if wtc[3] == 'allow':
                    if admin_check() == 1:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if admin_check() == 1:
                        perm = 0
                        break
                    else:
                        continue
            # <option value="suspended_before">차단된 적이 있는 사용자</option>
            # <option value="document_starred">이 문서를 주시하는 사용자</option>
            # <option value="discussed_document">이 문서에서 토론한 적이 있는 사용자</option>
            # <option value="document_only_contributor">이 문서의 유일한 기여자</option>
            # <option value="discussed">토론한 적이 있는 아이피 혹은 사용자</option>

            elif wtc[2] == 'suspended_before':
                curs.execute("select block from rb where block = ? and not end = 'grant' and not end = 'lh'", [ip_check()])
                x = curs.fetchall()
                if wtc[3] == 'allow':
                    if x:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if x:
                        break
                    else:
                        continue
            elif wtc[2] == 'document_starred':
                curs.execute("select doc from star where doc = ? and user = ?", [name, ip_check()])
                x = curs.fetchall()
                if wtc[3] == 'allow':
                    if x:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if x:
                        break
                    else:
                        continue
            elif wtc[2] == 'discussed_document':
                curs.execute("select ip from topic where title = ? and ip = ?", [name, ip_check()])
                x = curs.fetchall()
                if wtc[3] == 'allow':
                    if x:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if x:
                        break
                    else:
                        continue
            elif wtc[2] == 'document_only_contributor':
                curs.execute("select ip from history where not ip = ? and title = ?", [ip_check(), name])
                x = curs.fetchall()
                curs.execute("select ip from history where ip = ? and title = ?", [ip_check(), name])
                y = curs.fetchall()

                if wtc[3] == 'allow':
                    if y and (not x):
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if y and (not x):
                        break
                    else:
                        continue
            elif wtc[2] == 'discussed':
                curs.execute("select ip from topic where ip = ?", [ip_check()])
                x = curs.fetchall()
                if wtc[3] == 'allow':
                    if x:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if x:
                        break
                    else:
                        continue
            elif wtc[2] == 'nsacl':
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'nsacl'])
                na = curs.fetchall()
                if wtc[3] == 'allow':
                    if na:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if na:
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'editable_other_user_document':
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'eou'])
                eu = curs.fetchall()
                if wtc[3] == 'allow':
                    if eu:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if eu:
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'special':
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'special'])
                sp = curs.fetchall()
                if wtc[3] == 'allow':
                    if sp:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if sp:
                        perm = 0
                        break
                    else:
                        continue
            elif wtc[2] == 'grant':
                if wtc[3] == 'allow':
                    if admin_check(7) == 1:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if admin_check(7) == 1:
                        perm = 0
                        break
                    else:
                        continue
            elif re.search("[m][e][m][b][e][r][_][s][i][g][n][u][p][_]\d{1,}[d][a][y][s][_][a][g][o]", wtc[2]):
                days = int((wtc[2].replace('member_signup_', '')).replace('days_ago', ''))
                aaa = get_time()
                curs.execute("select date from user where id = ?", [ip_check()])
                bbbb = curs.fetchall()
                if bbbb:
                    bbb = bbbb[0][0]
                else:
                    continue
                aa = aaa.split(' ')
                bb = bbb.split(' ')
                a1 = aa[0]
                b1 = bb[0]
                a2 = a1.split('-')
                b2 = b1.split('-')

                p = date(int(a2[0]), int(a2[1]), int(a2[2]))
                q = date(int(b2[0]), int(b2[1]), int(b2[2]))
                ans = (p-q).days

                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if ans >= days:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if ans >= days:
                        perm = 0
                        break
                    else:
                        continue
            elif re.search("[m][e][m][b][e][r][_][n][o][t][_][s][i][g][n][u][p][_]\d{1,}[d][a][y][s][_][a][g][o]", wtc[2]):
                days = int((wtc[2].replace('member_not_signup_', '')).replace('days_ago', ''))
                aaa = get_time()
                curs.execute("select date from user where id = ?", [ip_check()])
                bbbb = curs.fetchall()
                if bbbb:
                    bbb = bbbb[0][0]
                else:
                    continue
                aa = aaa.split(' ')
                bb = bbb.split(' ')
                a1 = aa[0]
                b1 = bb[0]
                a2 = a1.split('-')
                b2 = b1.split('-')

                p = date(int(a2[0]), int(a2[1]), int(a2[2]))
                q = date(int(b2[0]), int(b2[1]), int(b2[2]))
                ans = (p-q).days

                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if ans < days:
                        perm = 1
                        break
                    else:
                        continue
                else:
                    if ans < days:
                        perm = 0
                        break
                    else:
                        continue
        elif wtc[1] == 'member':
            if wtc[3] == 'allow':
                if ip_check() == wtc[2]:
                    perm = 1
                    break
                else:
                    continue
            else:
                if ip_check() == wtc[2]:
                    perm = 0
                    break
                else:
                    continue
        elif wtc[1] == 'ip':
            if wtc[3] == 'allow':
                if my_ip() == wtc[2]:
                    perm = 1
                    break
                else:
                    continue
            else:
                if my_ip() == wtc[2]:
                    perm = 0
                    break
                else:
                    continue
        elif wtc[1] == 'geoip':
            if wtc[3] == 'allow':
                if ipInfo(my_ip()) == wtc[2]:
                    perm = 1
                    break
                else:
                    continue
            else:
                if ipInfo(my_ip()) == wtc[2]:
                    perm = 0
                    break
                else:
                    continue
    return perm

def aclmsg(name, typ):
    try:
        ns = getNamespace(name.split(':')[0])
    except:
        ns = '문서'

    m1 = '' # ~이기 때문에 권한이 부족합니다.
    m2 = '' # ~ 권한이 부족합니다. ~(이)여야 합니다.

    perm = 0
    #                    0    1     2     3    4
    curs.execute("select id, type, perm, how, exp from seedacl where name = ? and what = ? order by cast(id as integer) asc", [name, typ])
    doca = curs.fetchall()
    curs.execute("select id, type, perm, how, exp from nsacl where ns = ? and what = ? order by cast(id as integer) asc", [ns, typ])
    nspa = curs.fetchall()
    if not(nspa):
        nspa = [['1','perm','any','deny','0']]
        return ['', 'ACL에 허용 규칙이 없기 때문에', ''] #인덱스 1로 시작하면 안되나
    if not(doca):
        curs.execute("select id, type, perm, how, exp from nsacl where ns = ? and what = ? and how = 'allow' order by cast(id as integer) asc", [ns, typ])
        if not curs.fetchall():
            return ['', 'ACL에 허용 규칙이 없기 때문에', '']
        alt = nspa
    else:
        curs.execute("select id, type, perm, how, exp from seedacl where name = ? and what = ? and how = 'allow' order by cast(id as integer) asc", [name, typ])
        if not curs.fetchall():
            return ['', 'ACL에 허용 규칙이 없기 때문에', '']
        alt = doca
    for wtc in alt:
        if wtc[1] == 'perm':
            if wtc[2] == 'all' or wtc[2] == 'any':
                if wtc[3] == 'allow':
                    break
                elif wtc[3] == 'deny':
                    m1 = '아무나이기 때문에'
                    break
            elif wtc[2] == 'blocked_ipacl':
                banned = 0
                curs.execute("select ip, al from ipacl")
                #포문/DO문(포트란) 1부터 1000000까지 1초 미만, 1부터 100000000까지 약 10초
                #다른 빠른알고리즘 생각해도 잘 모르겠음
                for i in curs.fetchall():
                    if ipInCIDR(my_ip(), i[0]) == 1:
                        if i[1] == 'Y' and('state' in flask.session and flask.session['state'] == 1):
                            banned = 0
                        else:
                            banned = 1
                        break

                if wtc[3] == 'allow':
                    if banned == 1:
                        break
                    else:
                        m2 += ' OR 차단된 아이피'
                        continue
                else:
                    if banned == 1:
                        m1 = '차단된 아이피이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'suspend_account':
                if islogin(conn) == 0:
                    continue

                if my_ip() == ip_check():
                    continue

                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 차단된 사용자'
                        continue
                else:
                    if ban_check() == 1:
                        m1 = '차단된 사용자이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'admin':
                if wtc[3] == 'allow':
                    if admin_check(5) == 1:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 관리자'
                        continue
                else:
                    if admin_check(5) == 1:
                        m1 = '관리자이기 때문에' # (...)
                        break
                    else:
                        continue
            elif wtc[2] == 'email':
                curs.execute("select data from user_set where id = ? and name = 'email'", [ip_check()])
                ismail = curs.fetchall()
                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        m2 += ' OR 이메일 인증된 사용자'
                        continue
                    if ismail:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 이메일 인증된 사용자'
                        continue
                else:
                    if ismail:
                        m1 = '이메일 인증된 사용자이기 때문에'
                        break
                    else:
                        continue
            elif re.search("\d{1,}[_][e][d][i][t]", wtc[2]):
                day = int(wtc[2].replace('_edit', ''))
                curs.execute("select count(title) from history where ip = ?", [ip_check()])
                count = curs.fetchall()
                if count:
                    ctc = count[0][0]
                else:
                    ctc = 0
                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        m2 += ' OR 기여 횟수가 ' + str(day) + '회 이상인 사용자'
                        continue
                    if ctc > day - 1:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 기여 횟수가 ' + str(day) + '회 이상인 사용자'
                        continue
                else:
                    if ctc > day - 1:
                        m1 = '기여 횟수가 ' + str(day) + '회 이상인 사용자이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'match_username_and_document_title':
                doct = name.replace(ns + ':', '')
                m = re.search("^(.*)\/(.*)$", doct)
                if m:
                    doct = m.groups()[0]
                if wtc[3] == 'allow':
                    if doct == ip_check() and islogin(conn) == 1:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 문서 제목과 사용자 이름이 일치'
                        continue
                else:
                    if doct == ip_check() and islogin(conn) == 1:
                        m1 = '문서 제목과 사용자 이름이 일치이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'match_ip_and_document_title':
                doct = name.replace(ns + ':', '')
                m = re.search("^(.*)\/(.*)$", doct)
                if m:
                    doct = m.groups()[0]
                if wtc[3] == 'allow':
                    if doct == my_ip():
                        perm = 1
                        break
                    else:
                        m2 += ' OR 문서 제목과 아이피 주소가 일치'
                        continue
                else:
                    if doct == my_ip():
                        m1 = '문서 제목과 아이피 주소가 일치이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'contributor':
                curs.execute("select ip from history where ip = ?", [ip_check()])
                x = curs.fetchall()
                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if x:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 위키 기여자'
                        continue
                else:
                    if x:
                        m1 = '위키 기여자이기 때문에'
                        break
                    else:
                        continue

            #<option value="member_suspended_before">차단된 적이 있는 사용자</option>
            #<option value="member_document_starred">이 문서를 주시하는 사용자</option>
            #<option value="member_discussed_document">이 문서에서 토론한 적이 있는 아이피 혹은 사용자</option>
            elif wtc[2] == 'suspended_before':
                curs.execute("select block from rb where block = ? and not end = 'grant' and not end = 'lh'", [ip_check()])
                x = curs.fetchall()
                if wtc[3] == 'allow':
                    if x:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 차단된 적이 있는 사용자'
                        continue
                else:
                    if x:
                        m1 = '차단된 적이 있는 사용자'
                        break
                    else:
                        continue
            elif wtc[2] == 'document_starred':
                curs.execute("select doc from star where doc = ? and user = ?", [name, ip_check()])
                x = curs.fetchall()
                if wtc[3] == 'allow':
                    if x:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 이 문서를 주시하는 사용자'
                        continue
                else:
                    if x:
                        m1 = '이 문서를 주시하는 사용자'
                        break
                    else:
                        continue
            elif wtc[2] == 'discussed_document':
                curs.execute("select ip from topic where title = ? and ip = ?", [name, ip_check()])
                x = curs.fetchall()
                if wtc[3] == 'allow':
                    if x:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 이 문서에서 토론한 적이 있는 아이피 혹은 사용자'
                        continue
                else:
                    if x:
                        m1 = '이 문서에서 토론한 적이 있는 아이피 혹은 사용자'
                        break
                    else:
                        continue
            elif wtc[2] == 'document_contributor':
                curs.execute("select ip from history where title = ? and ip = ?", [name, ip_check()])
                y = curs.fetchall()
                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if y:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 해당 문서 기여자'
                        continue
                else:
                    if y:
                        m1 = '해당 문서 기여자이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'document_last_contributed':
                curs.execute("select ip from history where title = ? order by date desc", [name])
                result = curs.fetchall()
                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if result and result[0][0] == ip_check():
                        perm = 1
                        break
                    else:
                        m2 += ' OR 해당 문서의 마지막 기여자'
                        continue
                else:
                    if result and result[0][0] == ip_check():
                        m1 = '해당 문서의 마지막 기여자이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'document_creator':
                curs.execute("select ip from history where title = ? and ip = ? and id = '1'", [name, ip_check()])
                y = curs.fetchall()
                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if y:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 해당 문서를 만든 사용자'
                        continue
                else:
                    if y:
                        m1 = '해당 문서를 만든 사용자이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'user' or wtc[2] == 'member':
                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if islogin(conn) == 1:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 로그인된 사용자'
                        continue
                else:
                    if islogin(conn) == 1:
                        m1 = '로그인된 사용자이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'ip':
                if wtc[3] == 'allow':
                    if islogin(conn) != 1:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 아이피 사용자'
                        continue
                else:
                    if islogin(conn) != 1:
                        m1 = '아이피 사용자이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'login_history':
                if wtc[3] == 'allow':
                    if admin_check(4) == 1:
                        perm = 1
                        break
                    else:
                        m2 += ' OR perm:login_history'
                        continue
                else:
                    if admin_check(4) == 1:
                        m1 = 'perm:login_history이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'developer':
                if wtc[3] == 'allow':
                    if admin_check() == 1:
                        perm = 1
                        break
                    else:
                        m2 += ' OR perm:developer'
                        continue
                else:
                    if admin_check() == 1:
                        m1 = 'perm:developer이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'nsacl':
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'nsacl'])
                na = curs.fetchall()
                if wtc[3] == 'allow':
                    if na:
                        perm = 1
                        break
                    else:
                        m2 += ' OR perm:nsacl'
                        continue
                else:
                    if na:
                        m1 = 'perm:nsacl이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'editable_other_user_document':
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'eou'])
                eu = curs.fetchall()
                if wtc[3] == 'allow':
                    if eu:
                        perm = 1
                        break
                    else:
                        m2 += ' OR perm:editable_other_user_document'
                        continue
                else:
                    if eu:
                        m1 = 'perm:editable_other_user_document이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'special':
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'special'])
                sp = curs.fetchall()
                if wtc[3] == 'allow':
                    if sp:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 특수 사용자'
                        continue
                else:
                    if sp:
                        m1 = '특수 사용자이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'grant':
                if wtc[3] == 'allow':
                    if admin_check(7) == 1:
                        perm = 1
                        break
                    else:
                        m2 += ' OR perm:grant'
                        continue
                else:
                    if admin_check(7) == 1:
                        m1 = 'perm:grant이기 때문에'
                        break
                    else:
                        continue
            elif re.search("[m][e][m][b][e][r][_][s][i][g][n][u][p][_]\d{1,}[d][a][y][s][_][a][g][o]", wtc[2]):
                days = int((wtc[2].replace('member_signup_', '')).replace('days_ago', ''))
                aaa = get_time()
                curs.execute("select date from user where id = ?", [ip_check()])
                bbbb = curs.fetchall()
                if bbbb:
                    bbb = bbbb[0][0]
                else:
                    m2 += ' OR 가입한지 ' + str(days) + '일 지난 사용자'
                    continue

                aa = aaa.split(' ')
                bb = bbb.split(' ')
                a1 = aa[0]
                b1 = bb[0]
                a2 = a1.split('-')
                b2 = b1.split('-')

                p = date(int(a2[0]), int(a2[1]), int(a2[2]))
                q = date(int(b2[0]), int(b2[1]), int(b2[2]))
                ans = (p-q).days

                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if ans >= days:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 가입한지 ' + str(days) + '일 지난 사용자'
                        continue
                else:
                    if ans >= days:
                        m1 = '가입한지 ' + str(days) + '일 지난 사용자이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'discussed':
                curs.execute("select ip from topic where title = ? and ip = ?", [name, ip_check()])
                x = curs.fetchall()
                if wtc[3] == 'allow':
                    if x:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 토론한 적이 있는 사용자'
                        continue
                else:
                    if x:
                        m1 = '토론한 적이 있는 사용자이기 때문에'
                        break
                    else:
                        continue
            elif wtc[2] == 'document_only_contributor':
                curs.execute("select ip from history where not ip = ? and title = ?", [ip_check(), name])
                x = curs.fetchall()
                curs.execute("select ip from history where ip = ? and title = ?", [ip_check(), name])
                y = curs.fetchall()

                if wtc[3] == 'allow':
                    if y and (not x):
                        perm = 1
                        break
                    else:
                        m2 += ' OR 이 문서의 유일한 기여자'
                        continue
                else:
                    if y and (not x):
                        m1 = '이 문서의 유일한 기여자이기 때문에'
                        break
                    else:
                        continue
            elif re.search("[m][e][m][b][e][r][_][n][o][t][_][s][i][g][n][u][p][_]\d{1,}[d][a][y][s][_][a][g][o]", wtc[2]):
                days = int((wtc[2].replace('member_not_signup_', '')).replace('days_ago', ''))
                aaa = get_time()
                curs.execute("select date from user where id = ?", [ip_check()])
                bbbb = curs.fetchall()
                if bbbb:
                    bbb = bbbb[0][0]
                else:
                    continue
                aa = aaa.split(' ')
                bb = bbb.split(' ')
                a1 = aa[0]
                b1 = bb[0]
                a2 = a1.split('-')
                b2 = b1.split('-')

                p = date(int(a2[0]), int(a2[1]), int(a2[2]))
                q = date(int(b2[0]), int(b2[1]), int(b2[2]))
                ans = (p-q).days

                if wtc[3] == 'allow':
                    if ban_check() == 1:
                        continue
                    if ans < days:
                        perm = 1
                        break
                    else:
                        m2 += ' OR 가입한지 ' + str(days) + '일이 지나지 않은 사용자'
                        continue
                else:
                    if ans < days:
                        m1 = '가입한지 ' + str(days) + '일이 지나지 않은 사용자이기 때문에'
                        break
                    else:
                        continue
        elif wtc[1] == 'member':
            if islogin(conn) == 0:
                m2 += ' OR member:' + wtc[2]
                continue

            if wtc[3] == 'allow':
                if ip_check() == wtc[2] and islogin(conn) == 1:
                    perm = 1
                    break
                else:
                    m2 += ' OR member:' + wtc[2]
                    continue
            else:
                if ip_check() == wtc[2] and islogin(conn) == 1:
                    m1 = 'member:' + wtc[2] + '이기 때문에'
                    break
                else:
                    continue
        elif wtc[1] == 'ip':
            if wtc[3] == 'allow':
                if my_ip() == wtc[2]:
                    perm = 1
                    break
                else:
                    m2 += ' OR ip:' + wtc[2]
                    continue
            else:
                if my_ip() == wtc[2]:
                    m1 = 'ip:' + wtc[2] + '이기 때문에'
                    break
                else:
                    continue
        elif wtc[1] == 'geoip':
            if wtc[3] == 'allow':
                if ipInfo(my_ip()) == wtc[2]:
                    perm = 1
                    break
                else:
                    m2 += ' OR geoip:' + wtc[2]
                    continue
            else:
                if ipInfo(my_ip()) == wtc[2]:
                    m1 = 'geoip:' + wtc[2] + '이기 때문에'
                    break
                else:
                    continue
    if m2 == '':
        return ['', m1, '']
    else:
        return ['', m1, re.sub('^ OR ', '', m2) + '(이)여야 합니다.'] #인덱스 1로 시작하면 안되나

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

def checkEditFilter(content, baserev = 0, title = '', h = True):
    if admin_check(1, 'edit_filter pass') != 1:
        curs.execute("select name, regex, banner, end, note, revertnote from edit_filters")
        for data_list in curs.fetchall():
            match = re.compile(data_list[1], re.I)
            if match.search(content):
                try:
                    matchingKeyword = match.findall(content)[0]
                except:
                    matchingKeyword = ''

                curs.execute("select data from history where title = ? and id = ?", [title, str(baserev)])
                hd = curs.fetchall()
                if not hd:
                    hd = [['']]
                if h == True:
                    history_plus(
                        title,
                        hd[0][0],
                        get_time(),
                        data_list[2],
                        data_list[5],
                        leng_check(len(content), len(hd[0][0])),
                        'r' + str(baserev) + '으로 되돌림'
                    )
                    curs.execute("update data set data = ?, date = ? where title = ?", [hd[0][0], get_time(), title])
                else:
                    history_plus(
                        title,
                        '',
                        get_time(),
                        data_list[2],
                        data_list[5],
                        '-' + str(len(content)),
                        '삭제'
                    )
                    curs.execute("delete from data where title = ?", [title])

                if data_list[3] != '-1':
                    if 'state' in flask.session and flask.session['state'] == 1:
                        ban_insert(
                            ip_check(),
                            data_list[3],
                            data_list[4],
                            None,
                            data_list[2]
                        )
                    else:
                        #def ban_insert(name, end, why, login, blocker, type_d = None):
                        #ban_insert 참고함.
                        end = int(number_check(data_list[3]))

                        time = datetime.datetime.now()
                        plus = datetime.timedelta(seconds = end)
                        r_time = (time + plus).strftime("%Y-%m-%d %H:%M:%S")
                        if data_list[3] == '0':
                            r_time = '0'

                        al = 'N'
                        try:
                            socket.inet_aton(ip_check())
                            actionIP = ip_check() + '/32'
                        except socket.error:
                            actionIP = ip_check() + '/128'


                        curs.execute("select ip from ipacl where ip = ?", [actionIP])
                        if curs.fetchall():
                            return [1, matchingKeyword]

                        curs.execute("insert into ipacl (ip, al, start, end, log) values (?, ?, ?, ?, ?)", [actionIP, al, get_time(), r_time, data_list[4]])
                        curs.execute("insert into rb (block, end, today, blocker, why, band, ipacl) values (?, ?, ?, ?, ?, '', '1')", [actionIP, data_list[3], get_time(), data_list[2], data_list[4]])
                        conn.commit()

                return [1, matchingKeyword]

    return [0, '']

def redirect(data = '/'):
    conn.commit()
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


            curs.execute("select login, end, why, start from ban where ((end > ? and end like '2%') or end = '') and block = ?", [get_time(), ip])
            ban_d = curs.fetchall()

            if ban_d:
                st1 = ban_d[0][3]
                #end += '<li>' + load_lang('type') + ' : ban</li>'
                if st1 == '':
                    st1 = '알 수 없는 시간'
                if ban_d[0][1] == '' or ban_d[0][1] == '0':
                    end += '이 사용자는 ' + generateTime(st1) + '에 영구적으로 차단되었습니다.<br>'
                    end += '차단 사유 : ' + ban_d[0][2]
                else:
                    end += '이 사용자는 ' + generateTime(st1) + '에 ' + generateTime(ban_d[0][1]) + '까지 차단되었습니다.<br>'
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

def noread(conn, name):
    curs = conn.cursor()
    return easy_minify(flask.render_template(skin_check(),
        imp = [load_lang('error'), wiki_set(1), custom(), other2([0, 0])],
        data = '<h2 style="border:none;font-weight:600">' + aclmsg(name, 'read')[1] + ' 읽기 권한이 부족합니다. ' + aclmsg(name, 'read')[2] + ' 해당 문서의 <a href="/acl/' + url_pas(name) + '">ACL 탭</a>을 확인하시기 바랍니다.</h2>',
        menu = 0
    )), 401

def noreadview(conn, name):
    curs = conn.cursor()
    return '<h2 style="border:none;font-weight:600">읽기 권한이 부족합니다. 해당 문서의 <a href="/acl/' + url_pas(name) + '">ACL 탭</a>을 확인하시기 바랍니다.</h2>'

def re_balloon(data, edt = 0, tit = ''):
    conn.commit()

    if data == '/ban':
        ip = ip_check()

        if edt == 1:
            end = aclmsg(tit, 'edit')[1] + ' 편집 ' + load_lang('authority_error') + ' ' + aclmsg(tit, 'edit')[2] + ' 해당 문서의 <a href="/acl/' + url_pas(tit) + '">ACL 탭</a>을 확인하시기 바랍니다. 대신 <a href="/new_edit_request/' + url_pas(tit) + '"><b>편집 요청</b></a>을 생성하실 수 있습니다.'
        else:
            end = load_lang('authority_error')
        curs.execute("select block from ban where block = ?", [ip_check()])
        if curs.fetchall() and ban_check() == 1 and ('state' in flask.session and flask.session['state'] == 1):
            end = '차단된 계정입니다.<br>'
            curs.execute("select start, end, why from ban where block = ?", [ip])
            ban_d = curs.fetchall()
            if ban_d:
                if ban_d[0][1] == '' or ban_d[0][1] == '0':
                    end += '차단 만료일 : 무기한<br>'
                else:
                    end += '차단 만료일 : ' + generateTime(ban_d[0][1], 'Y-m-d H:i:sO') + '<br>'
                end += '차단 사유 : ' + ban_d[0][2]
        elif ban_check() == 1:
            curs.execute("select ip, al, end, log from ipacl")
            for i in curs.fetchall():
                if ipInCIDR(my_ip(), i[0]) == 1:
                    if i[1] == 'Y':
                        end = '이용중인 IP는 문서 훼손행위가 자주 발생하는 IP이므로 로그인이 필요합니다.<br>(이 메세지는 본인이 반달을 했다기 보다는 같은 인터넷 공급업체를 사용하는 다른 누군가로 인해 발생했을 가능성이 높습니다.)<br>'
                    else:
                        end = 'IP가 차단되었습니다.<br>'
                    if i[2] == '0' or i[2] == '':
                        end += '차단 만료일 : 무기한'
                    else:
                        end += '차단 만료일 : ' + generateTime(i[2], 'Y-m-d H:i:sO')
                    end += '<br>차단 사유 : ' + i[3]
                    break

        return end
    else:
        return ''


def re_error(data):
    conn.commit()

    if data == '/ban':
        ip = ip_check()

        end = load_lang('authority_error')
        curs.execute("select block from ban where block = ?", [ip_check()])
        if curs.fetchall() and ban_check() == 1 and ('state' in flask.session and flask.session['state'] == 1):
            end = '차단된 계정입니다.<br>'
            curs.execute("select start, end, why from ban where block = ?", [ip])
            ban_d = curs.fetchall()
            if ban_d:
                if ban_d[0][1] == '' or ban_d[0][1] == '0':
                    end += '차단 만료일 : 무기한<br>'
                else:
                    end += '차단 만료일 : ' + generateTime(ban_d[0][1], 'Y-m-d H:i:sO') + '<br>'
                end += '차단 사유 : ' + ban_d[0][2]
        elif ban_check() == 1:
            curs.execute("select ip, al, end, log from ipacl")
            for i in curs.fetchall():
                if ipInCIDR(my_ip(), i[0]) == 1:
                    if i[1] == 'Y':
                        end = '이용중인 IP는 문서 훼손행위가 자주 발생하는 IP이므로 로그인이 필요합니다.<br>(이 메세지는 본인이 반달을 했다기 보다는 같은 인터넷 공급업체를 사용하는 다른 누군가로 인해 발생했을 가능성이 높습니다.)<br>'
                    else:
                        end = 'IP가 차단되었습니다.<br>'
                    if i[2] == '0' or i[2] == '':
                        end += '차단 만료일 : 무기한'
                    else:
                        end += '차단 만료일 : ' + generateTime(i[2], 'Y-m-d H:i:sO')
                    end += '<br>차단 사유 : ' + i[3]
                    break
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
                data = 'reCAPTCHA 인증에 실패했습니다.'
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
                data = 'already_starred_document (1000)'
            elif num == 1001:
                data = 'already_unstarred_document (1001)'
            elif num == 1100:
                data = '5자 이상의 요약을 입력해 주세요.'
            elif num == 1101:
                data = '문서 삭제에 대한 안내를 확인해 주세요.'
            elif num == 1200:
                data = 'disable_user_document (1200)'
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
            elif num == 7000:
                data = '토론이 존재하지 않습니다.'
            elif num == 7001:
                data = '토론이 이미 존재합니다.'
            elif num == 8000:
                data = '문서를 찾을 수 없습니다.'
            elif num == 9001:
                data = '문서 이름이 올바르지 않습니다.'
            elif num == 8001:
                data = '섹션이 올바르지 않습니다.'
            else:
                data = '지정되지 않은 오류입니다. (' + str(num) + ')'

            return easy_minify(flask.render_template(skin_check(),
                imp = [load_lang('error'), wiki_set(1), custom(), other2([0, 0])],
                data = '<h2>' + data + '</h2>',
                menu = 0,
                errdata = data
            )), 401
        else:
            return redirect('/')




def showError(data):
    return easy_minify(flask.render_template(skin_check(),
        imp = ['문제가 발생했습니다!', wiki_set(1), custom(), other2([0, 0])],
        data = '<h2>' + data + '</h2>',
        menu = 0,
        errdata = data
    )), 401


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
                try:
                    open('./views/' + skin_check(1) + '/js/settings.js', 'r').read()
                    data = '설정 페이지를 불러오는 중...'
                except:
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

def generateTime(time, form = 'Y-m-d H:i:s', f = False):
    if f != False:
        if time == '0' or time == 0:
            return '영구'
    try:
        ddd = time.split(' ')[0]
        ttt = time.split(' ')[1]

        return '<time datetime="' + ddd + 'T' + ttt + '.000Z" data-format="' + form + '">' + time + '</time>'
    except:
        return time

def stringInFormat(pattern, string):
    if len(string) < 1:
        return 0
    try:
        if re.sub(pattern, '', string) == '':
            return 1
        else:
            return 0
    except:
        return 0



def getForm(name, default = ''):
    return flask.request.form.get(name, default)

def alertBalloon(data, alertType = 'danger', alertTitle = '오류', dismissable = True):
    if dismissable == True:
        return '''<div class="alert alert-''' + alertType + ''' alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
        <span class="sr-only">Close</span>
        </button>
           <strong>[''' + alertTitle + '''!]</strong> ''' + data + '''
       </div>'''
    else:
        return '''<div class="alert alert-''' + alertType + '''" role="alert">
           <strong>[''' + alertTitle + '''!]</strong> ''' + data + '''
       </div>'''

def enableCompat():
    ua = flask.request.headers.get('User-Agent')
    if re.search('[;] MSIE \d{1,1}[.]\d{1,5};', ua): # MS IE 1.0부터 9.0까지 인식
        return True
    else:
        return None

def discussFetch(tnum, nojs = '0', snum = None):
    curs = conn.cursor()

    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')

    if getacl(name, 'read') != 1:
        return re_error('/error/3')

    curs.execute("select id, data, date, ip, block, top, adm, ismember from topic where tnum = ? order by date asc", [tnum])

    data = curs.fetchall()
    all_data = ''
    admin = admin_check(3)

    number = 1
    if snum:
        snum = int(snum)
    for i in data:
        if snum:
            if not(number == 1) and number < snum:
                number += 1
                continue
            if number > snum + 29:
                break

        t_data_f = render_set(data = i[1])
        if t_data_f == '스레드 상태를 <b>open</b>로 변경':
            t_data_f = '스레드 상태를 <b>normal</b>로 변경'
        if i[4] != 'O':
            b_color = ''
        else:
            b_color = 'toron_color_grey'
            curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'htc'])
            if not(curs.fetchall()):
                curs.execute("select who from re_admin where what = ? order by time desc limit 1", ['blind (' + name + ' - ' + sub + '#' + str(i[0]) + ')'])
                who_blind = curs.fetchall()
                if who_blind:
                    t_data_f = '[' + who_blind[0][0] + '에 의해 숨겨진 글입니다.]'
                    blablabla = 1
                else:
                    t_data_f = '[알 수 없는 사용자에 의해 숨겨진 글입니다.]'
                    blablabla = 1
            curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'htc'])
            if curs.fetchall():
                curs.execute("select who from re_admin where what = ? order by time desc limit 1", ['blind (' + name + ' - ' + sub + '#' + str(i[0]) + ')'])
                who_blind = curs.fetchall()
                if who_blind:
                    #t_data_f = '<span class="hidden-info">[' + who_blind[0][0] + '에 의해 숨겨진 글입니다.]</span><ctl class="new-show-hidden-content-button"> <a class="btn btn-danger btn-sm" onclick="$(this).parent().children(\'.hidden-content\').show(); $(this).hide(); $(this).parent().parent().children(\'.hidden-info\').hide(); $(this).parent().parent().attr(\'class\', \'r-body\'); return false;" style="color: rgb(255, 255, 255); width: auto;">[ADMIN] SHOW</a><div class="hidden-content" style="display:none">' + t_data_f + '</div></ctl><ctl class="old-show-hidden-content-button" style="display: none;"><div class="text-line-break" style="margin: 25px 0px 0px -10px; display:block"><a class="text" onclick="$(this).parent().parent().children(\'.hidden-content\').show(); $(this).parent().css(\'margin\', \'15px 0 15px -10px\'); $(this).hide(); return false;" style="display: block; color: #fff;">[ADMIN] Show hidden content</a><div class="line"></div></div><div class="hidden-content" style="display:none">' + t_data_f + '</div></ctl>'
                    t_data_f = '[' + who_blind[0][0] + '에 의해 숨겨진 글입니다.]<div class="text-line-break" style="margin: 25px 0px 0px -10px; display:block"><a class="text" onclick="$(this).parent().parent().children(\'.hidden-content\').show(); $(this).parent().css(\'margin\', \'15px 0 15px -10px\'); $(this).hide(); return false;" style="display: block; color: #fff;">[ADMIN] Show hidden content</a><div class="line"></div></div><div class="hidden-content" style="display:none">' + t_data_f + '</div>'
                    blablabla = 1
                else:
                    t_data_f = '[숨겨진 글입니다.]<br><br>' + t_data_f
                    blablabla = 1

        if i[0] == '1':
            s_user = i[3]
        else:
            if flask.request.args.get('num', None):
                curs.execute("select ip from topic where tnum = ? order by id + 0 asc limit 1", [tnum])
                g_data = curs.fetchall()
                if g_data:
                    s_user = g_data[0][0]
                else:
                    s_user = ''
        oraoraorgaanna = 0
        if flask.request.args.get('top', None):
            t_color = 'toron_color_red'
        elif i[3] == s_user:
            t_color = 'toron_color_green'
        elif i[5] == '1':
            if i[3] == s_user:
                t_color = 'toron_color_green'
            else:
                t_color = 'toron_color'
            oraoraorgaanna = 1
        else:
            t_color = 'toron_color'

        ip = ''

        if nojs == '1' and admin_check(1) == 1:
            if i[7] == 'ip':
                if ban_check(i[3], ipacl = True) == 1:
                    ip += ' <a href="/admin/ipacl?cidr=' + url_pas(i[3]) + '/32&note=쓰레드 ' + tnum + ' %23' + i[0] + '">[차단 해제]</a>'
                else:
                    ip += ' <a href="/admin/ipacl?cidr=' + url_pas(i[3]) + '/32&note=쓰레드 ' + tnum + ' %23' + i[0] + '">[차단]</a>'
            else:
                if ban_check(i[3]) == 1:
                    ip += ' <a href="/admin/suspend_account/' + url_pas(i[3]) + '?note=쓰레드 ' + tnum + ' %23' + i[0] + '">[차단 해제]</a>'
                else:
                    ip += ' <a href="/admin/suspend_account/' + url_pas(i[3]) + '?note=쓰레드 ' + tnum + ' %23' + i[0] + '">[차단]</a>'



        if 3 == 4:#if i[6] == '1':
            if i[7] != 'ip':
                ip += '<a style="font-weight: bold;" href="/w/사용자:' + url_pas(i[3]) + '">' + html.escape(i[3]) + '</a>'
            else:
                ip += '<a style="font-weight: bold;" href="/contribution/ip/' + url_pas(i[3]) + '/document">' + html.escape(i[3]) + '</a>'
        if 3 == 5:#else:
            if i[7] != 'ip':
                ip += '<a href="/w/사용자:' + url_pas(i[3]) + '">' + html.escape(i[3]) + '</a>'
            else:
                ip += '<a href="/contribution/ip/' + url_pas(i[3]) + '/document">' + html.escape(i[3]) + '</a>'
        ip += ip_pas_t(i[3], i[7], i[6])

        #if admin == 1 or b_color != 'toron_color_grey':
            #ip += ' <a href="/topic/' + url_pas(name) + '/sub/' + url_pas(sub) + '/admin/' + i[0] + '">(' + load_lang('discussion_tool') + ')</a>'
        if i[7] == 'ip':
            if ban_check(i[3], ipacl = True) == 1:
                ip += ' <sub>(차단된 아이피)</sub>'
        else:
            if ban_check(i[3]) == 1:
                ip += ' <sub>(차단된 사용자)</sub>'
        pinbtn = ''
        curs.execute("select perm from grant where perm = 'htc' and user = ?", [ip_check()])
        if curs.fetchall():
            if i[5] == 'O':
                pinbtn = '<a class="btn btn-warning btn-sm" href="/admin/thread/' + tnum + '/' + i[0] + '/unpin">[ADMIN] 고정 해제</a>'
            else:
                pinbtn = '<a class="btn btn-warning btn-sm" href="/admin/thread/' + tnum + '/' + i[0] + '/pin">[ADMIN] 고정</a>'
        if i[5] == '1':
            pinbtn = ''

        all_data += '''
            <div class="res-wrapper" data-id="''' + i[0] + '''">'''
        if i[5] == '1':
            all_data +=  '<div class="res res-type-status">'
        else:
            all_data +=  '<div class="res res-type-normal">'
        all_data += '''
                <div class="r-head'''
        if i[3] == s_user:
            all_data += ' first-author'
        ddd = i[2].split(' ')[0]
        ttt = i[2].split(' ')[1]
        all_data += '''
                        "><span class="num"><a id="''' + i[0] + '">#' + i[0] + '</a>&nbsp;</span> ' + ip + ' <span style="margin-left: 25px;float:right"><time datetime="''' + ddd + 'T' + ttt + '''.000Z" data-format="Y-m-d H:i:s">''' + i[2] + '''</time></span><div class="clearfix"></div>
                        </div>
                <div class="r-body'''
        if i[4] == 'O':
            all_data += ' r-hidden-body'
        all_data += '''">'''
        all_data += t_data_f + '''
                    </div>
        '''
        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'htc'])
        if curs.fetchall():
            if i[4] == 'O':
                urlToHideOrShow = 'show'
            else:
                urlToHideOrShow = 'hide'
            all_data += '''
            <div class="combo admin-menu">

		    <a class="btn btn-danger btn-sm" href="/admin/thread/''' + url_pas(tnum) + '''/''' + i[0] + '''/''' + urlToHideOrShow + '''" style="color:#fff">'''
            if i[4] == 'O':
                all_data += '''[ADMIN] 숨기기 해제'''
            else:
                all_data += '''[ADMIN] 숨기기'''
            all_data += '''</a>''' + pinbtn + '''</div>'''
        all_data += '</div></div>'

        #all_data += '<br /><br />'

        number += 1

    return all_data
asasdsda = '''
def setCAPTCHA():
    img = Image.new('RGB', (70, 30), color = (73, 109, 137))

    crndval = ''.join(random.choice("2346789") for i in range(8))

    # fnt = ImageFont.truetype('Arial.ttf', 15)
    d = ImageDraw.Draw(img)
    d.text((10,10), crndval, fill=(255, 255, 0))
    d.line((0,0, 69,29), fill=(255, 255, 225), width=2)
    d.line((0,13, 69,13), fill=(255, 255, 225), width=1)
    d.line((0,17, 69,17), fill=(255, 255, 225), width=1)

    buffered = BytesIO()

    img.save(buffered, format="PNG")

    #flask.session['rndval'] = crndval

    return re.sub("[']$", '', re.sub("^[b][']", '', str(base64.b64encode(buffered.getvalue()))))

'''