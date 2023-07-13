import os
import re

for i_data in os.listdir("route"):
    f_src = re.search("(.+)\.py$", i_data)
    if f_src:
        f_src = f_src.groups()[0]

        exec("from route." + f_src + " import *")

version_list = json.loads(open('version.json', encoding='utf-8').read())

r_ver = version_list['master']['r_ver']
c_ver = version_list['master']['c_ver']
s_ver = version_list['master']['s_ver']

print('버전: ' + r_ver)

app_var = json.loads(open('data/app_variables.json', encoding='utf-8').read())

# DB
all_src = []
for i_data in os.listdir("."):
    f_src = re.search("(.+)\.db$", i_data)
    if f_src:
        all_src += [f_src.groups()[0]]

if len(all_src) == 0:
    print('데이터베이스 이름 (기본값 data): ', end = '')

    db_name = input()
    if db_name == '':
        db_name = 'data'
elif len(all_src) > 1:
    db_num = 1

    for i_data in all_src:
        print(str(db_num) + ': ' + i_data)

        db_num += 1

    print('숫자: ', end = '')
    db_name = all_src[int(number_check(input())) - 1]
else:
    db_name = all_src[0]

if len(all_src) == 1:
    print('데이터베이스 이름: ' + db_name)

if os.path.exists(db_name + '.db'):
    setup_tool = 0
else:
    setup_tool = 1

conn = sqlite3.connect('WIKIDATA.db', check_same_thread = False)
curs = conn.cursor()

load_conn(conn)

#logging.basicConfig(level = logging.ERROR)

app = flask.Flask(__name__, template_folder = './')
app.config['JSON_AS_ASCII'] = False

flask_reggie.Reggie(app)

compress = flask_compress.Compress()
compress.init_app(app)

class EverythingConverter(werkzeug.routing.PathConverter):
    regex = '.*?'

app.jinja_env.filters['md5_replace'] = md5_replace
app.jinja_env.filters['load_lang'] = load_lang
app.jinja_env.filters['cut_100'] = cut_100
app.jinja_env.filters['url_pas'] = url_pas
app.jinja_env.filters['url_encode'] = url_pas
app.jinja_env.filters['to_date'] = generateTime
app.jinja_env.filters['CEng'] = loadLang

app.url_map.converters['everything'] = EverythingConverter

curs.execute('create table if not exists data(test text)')
curs.execute('create table if not exists cache_data(test text)')
curs.execute('create table if not exists history(test text)')
curs.execute('create table if not exists rd(test text)')
curs.execute('create table if not exists user(test text)')
curs.execute('create table if not exists user_set(test text)')
curs.execute('create table if not exists ban(test text)')
curs.execute('create table if not exists topic(test text)')
curs.execute('create table if not exists rb(test text)')
curs.execute('create table if not exists back(test text)')
curs.execute('create table if not exists custom(test text)')
curs.execute('create table if not exists other(test text)')
curs.execute('create table if not exists alist(test text)')
curs.execute('create table if not exists re_admin(test text)')
curs.execute('create table if not exists alarm(test text)')
curs.execute('create table if not exists ua_d(test text)')
curs.execute('create table if not exists filter(test text)')
curs.execute('create table if not exists scan(test text)')
curs.execute('create table if not exists acl(test text)')
curs.execute('create table if not exists inter(test text)')
curs.execute('create table if not exists html_filter(test text)')
curs.execute('create table if not exists oauth_conn(test text)')
curs.execute('create table if not exists star(test text)')
curs.execute('create table if not exists erq(test text)')
curs.execute('create table if not exists leq(test text)')
curs.execute('create table if not exists grant(test text)')
curs.execute('create table if not exists ipacl(test text)')
curs.execute('create table if not exists ipc(test text)')
curs.execute('create table if not exists seedacl(test text)')
curs.execute('create table if not exists nsacl(test text)')

if setup_tool == 0:
    try:
        curs.execute('select data from other where name = "ver"')
        ver_set_data = curs.fetchall()
        if not ver_set_data:
            setup_tool = 1
        else:
            if c_ver > ver_set_data[0][0]:
                setup_tool = 1
    except:
        setup_tool = 1

if setup_tool != 0:
    create_data = {}

    create_data['all_data'] = [
        'data',
        'cache_data',
        'history',
        'rd',
        'user',
        'user_set',
        'ban',
        'topic',
        'rb',
        'back',
        'custom',
        'other',
        'alist',
        're_admin',
        'alarm',
        'ua_d',
        'filter',
        'scan',
        'acl',
        'inter',
        'html_filter',
        'oauth_conn',
        'star',
        'erq',
        'leq',
        'grant',
        'ipacl',
        'ipc',
        'seedacl',
        'nsacl'
    ]

    create_data['data'] = ['title', 'data', 'date']
    create_data['cache_data'] = ['title', 'data']
    create_data['history'] = ['id', 'title', 'data', 'date', 'ip', 'send', 'leng', 'hide', 'type', 'i', 'q', 'qn']
    create_data['rd'] = ['title', 'sub', 'date', 'band', 'stop', 'agree' 'pause']
    create_data['user'] = ['id', 'pw', 'acl', 'date', 'encode']
    create_data['user_set'] = ['name', 'id', 'data']
    create_data['ban'] = ['block', 'end', 'why', 'band', 'login', 'start']
    create_data['topic'] = ['id', 'title', 'sub', 'data', 'date', 'ip', 'block', 'top', 'adm']
    create_data['rb'] = ['block', 'end', 'today', 'blocker', 'why', 'band']
    create_data['back'] = ['title', 'link', 'type']
    create_data['custom'] = ['user', 'css']
    create_data['other'] = ['name', 'data', 'coverage']
    create_data['alist'] = ['name', 'acl']
    create_data['re_admin'] = ['who', 'what', 'time']
    create_data['alarm'] = ['name', 'data', 'date']
    create_data['ua_d'] = ['name', 'ip', 'ua', 'today', 'sub']
    create_data['filter'] = ['name', 'regex', 'sub']
    create_data['scan'] = ['user', 'title']
    create_data['acl'] = ['title', 'dec', 'dis', 'view', 'why']
    create_data['inter'] = ['title', 'link']
    create_data['html_filter'] = ['html', 'kind']
    create_data['oauth_conn'] = ['provider', 'wiki_id', 'sns_id', 'name', 'picture']
    create_data['star'] = ['user', 'doc']
    create_data['erq'] = ['name', 'num', 'send', 'leng', 'data', 'user', 'state', 'time', 'closer', 'y', 'ap', 'pan', 'why']
    create_data['leq'] = ['l', 'm']
    create_data['grant'] = ['perm', 'user']
    create_data['ipc'] = ['c', 'm']
    create_data['seedacl'] = ['id', 'type', 'perm', 'how', 'exp', 'name', 'what']
    create_data['nsacl'] = ['id', 'type', 'perm', 'how', 'exp', 'ns', 'what']

    for create_table in create_data['all_data']:
        for create in create_data[create_table]:
            try:
                curs.execute('select ' + create + ' from ' + create_table + ' limit 1')
            except:
                curs.execute("alter table " + create_table + " add " + create + " text default ''")

    update()

    curs.execute('insert into leq (l, m) values (?, ?)', ['0', '1'])
    curs.execute('insert into ipc (c, m) values (?, ?)', ['0', '1'])

# Init
curs.execute('select name from alist where acl = "owner"')
if not curs.fetchall():
    curs.execute('delete from alist where name = "owner"')
    curs.execute('insert into alist (name, acl) values ("owner", "owner")')

if not os.path.exists(app_var['path_data_image']):
    os.makedirs(app_var['path_data_image'])

if not os.path.exists('views'):
    os.makedirs('views')

import route.tool.init as server_init

dislay_set_key = ['호스트 주소', '포트', '언어', '문법', '암호화 방식']
server_set_key = ['host', 'port', 'language', 'markup', 'encode']
server_set = {}

for i in range(len(server_set_key)):
    curs.execute('select data from other where name = ?', [server_set_key[i]])
    server_set_val = curs.fetchall()
    if not server_set_val:
        server_set_val = server_init.init(server_set_key[i])

        curs.execute('insert into other (name, data) values (?, ?)', [server_set_key[i], server_set_val])
        conn.commit()
    else:
        server_set_val = server_set_val[0][0]

    print(dislay_set_key[i] + ': ' + server_set_val)

    server_set[server_set_key[i]] = server_set_val

try:
    if not os.path.exists('robots.txt'):
        curs.execute('select data from other where name = "robot"')
        robot_test = curs.fetchall()
        if robot_test:
            fw_test = open('./robots.txt', 'w')
            fw_test.write(re.sub('\r\n', '\n', robot_test[0][0]))
            fw_test.close()
        else:
            fw_test = open('./robots.txt', 'w')
            fw_test.write('User-agent: *\nDisallow: /\nAllow: /$\nAllow: /w/')
            fw_test.close()

            curs.execute('insert into other (name, data) values ("robot", "User-agent: *\nDisallow: /\nAllow: /$\nAllow: /w/")')

        print('----')
        print('robots.txt 생성 완료.')
except:
    pass

curs.execute('select data from other where name = "key"')
rep_data = curs.fetchall()
if not rep_data:
    rep_key = ''.join(random.choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(16))
    if rep_key:
        curs.execute('insert into other (name, data) values ("key", ?)', [rep_key])
else:
    rep_key = rep_data[0][0]

curs.execute('select data from other where name = "adsense"')
adsense_result = curs.fetchall()
if not adsense_result:
    curs.execute('insert into other (name, data) values ("adsense", "False")')
    curs.execute('insert into other (name, data) values ("adsense_code", "")')

curs.execute('delete from other where name = "ver"')
curs.execute('insert into other (name, data) values ("ver", ?)', [c_ver])


def back_up():
    print('----')
    try:
        shutil.copyfile(db_name + '.db', 'back_' + db_name + '.db')

        print('백업: 좋음')
    except:
        print('백업: 오류')

    threading.Timer(60 * 60 * back_time, back_up).start()

try:
    curs.execute('select data from other where name = "back_up"')
    back_up_time = curs.fetchall()

    back_time = int(back_up_time[0][0])
except:
    back_time = 0

print('----')
if back_time != 0:
    print('백업 상태: ' + str(back_time) + '시간')

    if __name__ == '__main__':
        back_up()
else:
    print('백업 상태: 사용 안함')

curs.execute('select data from other where name = "s_ver"')
ver_set_data = curs.fetchall()
if not ver_set_data:
    curs.execute('insert into other (name, data) values ("s_ver", ?)', [s_ver])

    if setup_tool == 0:
        print('----')
        print('Skin update required')
else:
    if int(ver_set_data[0][0]) < int(s_ver):
        curs.execute('delete from other where name = "s_ver"')
        curs.execute('insert into other (name, data) values ("s_ver", ?)', [s_ver])

        print('----')
        print('Skin update required')

def mysql_dont_off():
    try:
        urllib.request.urlopen('http://localhost:' + server_set['port'] + '/')
    except:
        pass

    threading.Timer(60 * 60 * 6, mysql_dont_off).start()

mysql_dont_off()

conn.commit()

print('----')

## Func
@app.route('/js/<everything:filename>')
def jfehurhf4ueii(filename):
    return flask.send_from_directory('./views/main_css/js', filename)

@app.route('/css/<everything:filename>')
def dgvdfsgdfgrf4r4e3(filename):
    return flask.send_from_directory('./views/main_css/css', filename)

@app.route('/admin/botting', methods=['POST', 'GET'])
def botting_r():
    return botting(conn)

@app.route('/member/advanced_style', methods=['POST', 'GET'])
def uhf873hf4r3u():
    return advancedStyle(conn)

@app.route('/admin/username_filters', methods=['POST', 'GET'])
def aunf():
    return usernameFilter(conn)

@app.route('/admin/edit_filters', methods=['POST', 'GET'])
def aedf():
    return editFilter(conn)

@app.route('/sidebar.json')
def sj():
    return sidebarRecent(conn)

@app.route('/admin/boardipacl')
@app.route('/admin/boardsuspendaccount')
def bia():
    return biaf(conn)

@app.route('/admin/blowup_documents', methods=['POST', 'GET'])
@app.route('/admin/exploder', methods=['POST', 'GET'])
def routeBlowupDocuments():
    return blowupDocuments(conn)

@app.route('/htmldata/recentchanges')
def routeSenkawaRecentApi():
    return senkawaRecentApi(conn)

@app.route('/complete/<everything:name>')
def complete(name = ''):
    return searchAutoComplete(conn, name)

@app.route('/member/clear_notifications')
def alarm_del():
    return alarm_del_2(conn)

@app.route('/member/notifications')
def alarm():
    return alarm_2(conn)

@app.route('/baduk')
def baduk():
    return baduk_2(conn)

@app.route('/janggi')
def janggi():
    return janggi_2(conn)

@app.route('/web')
def web():
    return web_2(conn)

@app.route('/redirect/<everything:name>')
def libertyRedirect(name = ''):
    return libertyRedirect2(conn, name)

@app.route('/RandomPage')
def randompage():
    return randompage_2(conn)

@app.route('/<regex("inter_wiki|(?:edit|email|file|name)_filter"):tools>')
@app.route('/admin/<regex("inter_wiki|(?:edit|email|file|name)_filter"):tools>')
def inter_wiki(tools = None):
    return inter_wiki_2(conn, tools)

@app.route('/<regex("del_(?:inter_wiki|(?:edit|email|file|name)_filter)"):tools>/<name>')
def inter_wiki_del(tools = None, name = None):
    return inter_wiki_del_2(conn, tools, name)

@app.route('/<regex("plus_(?:inter_wiki|(?:edit|email|file|name)_filter)"):tools>', methods=['POST', 'GET'])
@app.route('/<regex("plus_edit_filter"):tools>/<name>', methods=['POST', 'GET'])
def inter_wiki_plus(tools = None, name = None):
    return inter_wiki_plus_2(conn, tools, name)

@app.route('/admin/global_head', methods=['POST', 'GET'])
def agh():
    return setting_2(conn, 3)

@app.route('/admin/google', methods=['POST', 'GET'])
def agg():
    return setting_2(conn, 6)

@app.route('/admin/robots', methods=['POST', 'GET'])
def arb():
    return setting_2(conn, 5)

@app.route('/setting')
@app.route('/setting/<int:num>', methods=['POST', 'GET'])
def setting(num = 0):
    return setting_2(conn, num)

@app.route('/admin/config', methods=['POST', 'GET'])
def wikiconfig():
    return setting_2(conn, 1)

@app.route('/not_close_topic')
def dedir32734():
    return flask.redirect('/OngoingDiscussions')

@app.route('/OngoingDiscussions')
def list_not_close_topic():
    return list_not_close_topic_2(conn)

@app.route('/acl_list')
def list_acl():
    return list_acl_2(conn)

@app.route('/admin_plus/<name>', methods=['POST', 'GET'])
def give_admin_groups(name = None):
    return give_admin_groups_2(conn, name)

@app.route('/admin_list')
def redir8():
    return flask.redirect('/AdminList')

@app.route('/AdminList')
def list_admin():
    return list_admin_2(conn)

@app.route('/hidden/<everything:name>')
def give_history_hidden(name = None):
    return give_history_hidden_2(conn, name)

@app.route('/user_log')
def redir9():
    return flask.redirect('/UserList')

@app.route('/UserList')
def list_user():
    return list_user_2(conn)

@app.route('/')
def rtrt():
    return rtrt_2(conn)

@app.route('/new_edit_request/<everything:name>', methods=['POST', 'GET'])
def nerq(name):
    return nerq_2(conn, name)

@app.route('/edit_request/<num>', methods=['POST', 'GET'])
def eq(num):
    return eq_2(conn, num)

@app.route('/edit_request_close/<num>')
def eqc(num, methods=['POST', 'GET']):
    return eqc_2(conn, num)

@app.route('/edit_request_accept/<num>')
def eqa(num, methods=['POST', 'GET']):
    return eqa_2(conn, num)

@app.route('/admin_log', methods=['POST', 'GET'])
def list_admin_use():
    return list_admin_use_2(conn)

@app.route('/give_log')
def list_give():
    return list_give_2(conn)

@app.route('/admin/ipacl', methods=['POST', 'GET'])
def routeIPACL():
    return ipacl(conn)

@app.route('/admin/ipacl/remove', methods=['POST'])
def routeIPACLdelete():
    return ipaclDelete(conn)

@app.route('/indexing', methods=['POST', 'GET'])
def redir10():
    return redirect('/admin/db_indexing')

@app.route('/admin/db_indexing', methods=['POST', 'GET'])
def server_indexing():
    return server_indexing_2(conn)

@app.route('/restart', methods=['POST', 'GET'])
def redir11():
    return flask.redirect('/admin/engine_restart')

@app.route('/admin/engine_restart', methods=['POST', 'GET'])
def server_restart():
    return server_restart_2(conn)

@app.route('/update', methods=['GET', 'POST'])
def server_now_update():
    return server_now_update_2(conn)

@app.route('/oauth_setting', methods=['GET', 'POST'])
def setting_oauth():
    return setting_oauth_2(conn)

@app.route('/adsense_setting', methods=['GET', 'POST'])
def setting_adsense():
    return setting_adsense_2(conn)

@app.route('/xref/<everything:name>')
def view_xref(name = None):
    return view_xref_2(conn, name)

@app.route('/please')
def redir12():
    return flask.redirect('/NeededPages')

@app.route('/NeededPages')
def list_please():
    return list_please_2(conn)

@app.route('/OrphanedPages')
def list_orf():
    return list_orf_2(conn)

@app.route('/UncategorizedPages')
def list_unc():
    return list_unc_2(conn)

@app.route('/OldPages')
def list_old():
    return list_old_2(conn)

@app.route('/ShortestPages')
def list_short():
    return list_short_2(conn)

@app.route('/LongestPages')
def list_long():
    return list_long_2(conn)

@app.route('/member/star/<everything:name>')
def star(name = None):
    return star_2(conn, name)

@app.route('/member/unstar/<everything:name>')
def unstar(name = None):
    return unstar_2(conn, name)

@app.route('/member/starred_documents')
def stardoc():
    return stardoc_2(conn)

@app.route('/recent_discuss')
def redir13():
    return flask.redirect('/RecentDiscuss?logtype=' + flask.request.args.get('what', ''))

@app.route('/RecentDiscuss')
def recent_discuss():
    return recent_discuss_2(conn)

@app.route('/httpstat/<int:code>')
def httpstat(code = 200):
    return 'HTTP ' + str(code), code

@app.route('/block_log')
def redir14():
    return flask.redirect('/BlockHistory')

@app.route('/BlockHistory')
@app.route('/<regex("block_user|block_admin"):tool>/<name>')
def list_block(name = None, tool = None):
    return list_block_2(conn, name, tool)

@app.route('/search', methods=['POST'])
def search():
    return search_2(conn)

@app.route('/goto', methods=['POST'])
@app.route('/go', methods=['POST'])
@app.route('/goto/<everything:name>', methods=['POST'])
def search_goto(name = 'test'):
    return search_goto_2(conn, name)

@app.route('/go/<everything:name>', methods=['POST', 'GET'])
def gotodocument(name = ''):
    curs.execute("select title from data where title = ? COLLATE NOCASE", [name])
    td = curs.fetchall()
    if td:
        return redirect('/w/' + td[0][0])
    else:
        curs.execute("select title from history where title = ?", [name])
        if curs.fetchall():
            return redirect('/w/' + name)
        else:
            return redirect('/search/' + name)

@app.route('/search/<everything:name>')
def search_deep(name = 'test'):
    return search_deep_2(conn, name)

@app.route('/raw/<everything:name>')
def view_raw(name = None, sub_title = None, num = None):
    return view_raw_2(conn, name, sub_title, num)

@app.route('/revert/<everything:name>', methods=['POST', 'GET'])
def edit_revert(name = None):
    return edit_revert_2(conn, name)

@app.route('/edit/<everything:name>', methods=['POST', 'GET'])
def edit(name = None):
    return edit_2(conn, name)

@app.route('/preview/<everything:title>', methods = ['POST'])
def routePreview(title = ''):
    return Preview(title)

@app.route('/delete/<everything:name>', methods=['POST', 'GET'])
def edit_delete(name = None):
    return edit_delete_2(conn, name, app_var)

@app.route('/move/<everything:name>', methods=['POST', 'GET'])
def edit_move(name = None):
    return edit_move_2(conn, name)

@app.route('/other')
def redir15():
    return flask.redirect('/Special')

@app.route('/Special')
def main_other():
    return main_other_2(conn)

@app.route('/manager', methods=['POST', 'GET'])
@app.route('/admin', methods=['POST', 'GET'])
@app.route('/manager/<int:num>', methods=['POST', 'GET'])
def main_manager(num = 1):
    return main_manager_2(conn, num, r_ver)

@app.route('/title_index')
def dsf343fr4r4f3():
    return flask.redirect('/TitleIndex')

@app.route('/ErrorPage')
def dsf343fr4rdsdsdsds4f3():
    typ = int(flask.request.args.get('type', '1'))
    if typ == 1:
        n = 3 + 'string' + SyntaxError
    elif typ == 2:
        s = int('test string')
    elif typ == 3:
        testvar2 = testvar
    else:
        return re_error('/error/7777')

    return 'Error!'



@app.route('/TitleIndex')
def list_title_index():
    return list_title_index_2(conn)

@app.route('/admin/thread/<tnum>/hide/<int:num>')
@app.route('/admin/thread/<tnum>/<int:num>/<regex("hide|show"):typ>')
def topic_block(tnum, num = 1, typ = 'x'):
    return topic_block_2(conn, tnum, num, typ)

@app.route('/thread/<tnum>/<int:num>')
def topic_seed(tnum = None, num = 1):
    return topic_seed_2_3(conn, tnum, num)

@app.route('/thread/<tnum>/info')
def trfgjiertgioerjio(tnum = ''):
    return threadInfo(conn, tnum)

@app.route('/admin/thread/<tnum>/move/<everything:title>')
def topic_move(tnum = None, title = None):
    return topic_move_2(conn, tnum, title)

@app.route('/admin/thread/<tnum>/ren/<new>')
def topic_ren(tnum = None, new = None):
    return topic_ren_2(conn, tnum, new)

@app.route('/admin/thread/<tnum>/delete')
def topic_del(tnum = None):
    return topic_del_2(conn, tnum)

@app.route('/admin/thread/<tnum>/permanent_delete')
def gretgergersthg(tnum = None):
    return topic_pdel_2(conn, tnum)

@app.route('/admin/thread/<tnum>/restore')
def fdgvbfgert4w3(tnum = None):
    return topic_rdel_2(conn, tnum)

@app.route('/admin/thread/<tnum>/<int:num>/pin')
@app.route('/admin/thread/<tnum>/<int:num>/unpin')
def topic_top(tnum = None, num = 1):
    return topic_top_2(conn, tnum, num)

@app.route('/admin/thread/<tnum>/tool/<regex("close|stop|agree|pause"):tool>', methods=['POST', 'GET'])
def topic_stop(tnum = None, tool = None):
    return topic_stop_2(conn, tnum, tool)

@app.route('/thread/<tnum>/tool')
def topic_tool(tnum = None):
    return topic_tool_2(conn, tnum)

@app.route('/topic/<int:num>')
def topic_tnum(num = 1):
    curs = conn.cursor()
    curs.execute("select tnum from rd where tnumber = ?", [str(num)])
    try:
        return redirect('/thread/' + curs.fetchall()[0][0])
    except:
        return showError('토론이 존재하지 않습니다.')

@app.route('/thread/<tnum>/admin/<int:num>')
def topic_admin(tnum = None, num = 1):
    return topic_admin_2(conn, tnum, num)

@app.route('/thread/<tnum>', methods=['POST', 'GET'])
def topic(tnum = None):
    return topic_2(conn, tnum)

@app.route('/admin/thread/<tnum>/<regex("document|status|topic"):toolname>', methods=['POST'])
def routeThreadAdminTools(tnum = '', toolname = ''):
    return threadTools(conn, tnum, toolname)

@app.route('/discuss/<everything:name>', methods=['POST', 'GET'])
@app.route('/discuss/<everything:name>/<regex("close|agree|eqclose"):tool>', methods=['GET'])
def topic_close_list(name = None, tool = None):
    return topic_close_list_2(conn, name, tool)

@app.route('/tool/<name>')
def user_tool(name = None):
    return user_tool_2(conn, name)

@app.route('/login', methods=['POST', 'GET'])
def redir2():
    return flask.redirect('/member/login')

@app.route('/member/login', methods=['POST', 'GET'])
def login():
    return login_2(conn)

@app.route('/oauth/<regex("discord|naver|facebook|kakao"):platform>/<regex("init|callback"):func>', methods=['GET', 'POST'])
def login_oauth(platform = None, func = None):
    return login_oauth_2(conn, platform, func)

@app.route('/change', methods=['POST', 'GET'])
def redir1():
    return flask.redirect('/member/mypage')

@app.route('/member/mypage', methods=['POST', 'GET'])
def user_setting():
    return user_setting_2(conn, server_init)

@app.route('/pw_change')
def df4etyw4r5trtgy5gstaw4t5():
    return redirect('/member/mypage/change_password')

@app.route('/member/mypage/change_password', methods=['POST', 'GET'])
def login_pw_change():
    return login_pw_change_2(conn)

@app.route('/check/<name>')
@app.route('/login_history/<name>')
@app.route('/admin/login_history/<name>')
def give_user_check(name = None):
    return give_user_check_2(conn, name)

@app.route('/check')
@app.route('/login_history')
@app.route('/admin/login_history', methods=['POST', 'GET'])
def give_user_check_un():
    return lh_un_2(conn)

@app.route('/register', methods=['POST', 'GET'])
def dgr44rr():
    return flask.redirect('/member/signup')

@app.route('/member/signup', methods=['POST', 'GET'])
def login_register():
    return login_register_2(conn)

@app.route('/<regex("need_email|pass_find|email_change"):tool>', methods=['POST', 'GET'])
def login_need_email(tool = 'pass_find'):
    return login_need_email_2(conn, tool)

@app.route('/<regex("check_key|check_pass_key|email_replace"):tool>', methods=['POST', 'GET'])
def login_check_key(tool = 'check_pass_key'):
    return login_check_key_2(conn, tool)

@app.route('/logout')
@app.route('/member/logout')
def login_logout():
    return login_logout_2(conn)

@app.route('/admin/suspend_account', methods=['POST', 'GET'])
@app.route('/ban', methods=['POST', 'GET'])
@app.route('/admin/suspend_account/<name>', methods=['POST', 'GET'])
@app.route('/suspend_account', methods=['POST', 'GET'])
@app.route('/suspend_account/<name>', methods=['POST', 'GET'])
@app.route('/ban/<name>', methods=['POST', 'GET'])
def give_user_ban(name = None):
    return give_user_ban_2(conn, name)

@app.route('/acl/<everything:name>', methods=['POST', 'GET'])
def give_acl(name = None):
    return give_acl_2(conn, name)

@app.route('/admin/grant', methods=['POST', 'GET'])
@app.route('/grant', methods=['POST', 'GET'])
def give_admin():
    return give_admin_2(conn)

@app.route('/admin/adgrp/<name>', methods=['POST', 'GET'])
@app.route('/adgrp/<name>', methods=['POST', 'GET'])
def give_adgrp(name = None):
    return give_adgrp_2(conn, name)

@app.route('/diff/<everything:name>')
def view_diff_data(name = None):
    return view_diff_data_2(conn, name)

@app.route('/down/<everything:name>')
def view_down(name = None):
    return view_down_2(conn, name)

@app.route('/w/<everything:name>')
def view_read(name = None):
    return view_read_2(conn, name)

@app.route('/topic_record/<name>')
@app.route('/contribution/<regex("author|ip"):ismember>/<name>/discuss')
def list_user_topic(name = None, ismember = 'author'):
    return list_user_topic_2(conn, name, ismember)

@app.route('/recent_changes')
def j8grg8j94g8j4():
    return flask.redirect('/RecentChanges?logtype=' + flask.request.form.get("set", ""))

@app.route('/RecentChanges')
@app.route('/<regex("record"):tool>/<name>')
@app.route('/<regex("contribution"):tool>/<regex("author|ip"):ismember>/<name>/document')
@app.route('/<regex("history"):tool>/<everything:name>', methods=['POST', 'GET'])
def recent_changes(name = None, tool = 'record', ismember = ''):
    return recent_changes_2(conn, name, tool, ismember)

@app.route('/contribution/<regex("document|discuss"):typ>', methods=['POST', 'GET'])
def routeContributionPostForm(typ = 'document'):
    return contribution(typ)

@app.route('/upload', methods=['GET', 'POST'])
def gj4489jj89g4r():
    return flask.redirect('/Upload')

@app.route('/Upload', methods=['GET', 'POST'])
def func_upload():
    return func_seed_upload_2(conn)

@app.route('/user')
def g4rh5h55tewafr4w():
    return flask.redirect('/member')

@app.route('/member')
def user_info():
    return user_info_2(conn)

@app.route('/watch_list')
def watch_list():
    return watch_list_2(conn)

@app.route('/watch_list/<everything:name>')
def watch_list_name(name = None):
    return watch_list_name_2(conn, name)

@app.route('/custom_head', methods=['GET', 'POST'])
def redir325678():
    return flask.redirect('/member/custom_head')

@app.route('/member/custom_head', methods=['GET', 'POST'])
def user_custom_head_view():
    return user_custom_head_view_2(conn)

@app.route('/count')
@app.route('/count/<name>')
def user_count_edit(name = None):
    return user_count_edit_2(conn, name)

@app.route('/random')
def func_title_random():
    return func_title_random_2(conn)

@app.route('/notify/thread/<tnum>', methods=['POST'])
def dsfuy98rjioewakJreio(tnum):
    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')

    if getacl(name, 'read') != 1:
        return re_error('/error/3')

    curs.execute("select sub from rd where tnum = ? and removed = '1'", [tnum])
    if curs.fetchall() and admin_check() != 1:
        return re_error('/error/7000')

    if getacl(name, 'read') != 1:
        return re_error('/error/3')

    status = 'event'

    curs.execute("select id from topic where tnum = ? order by date desc limit 1", [tnum])
    comment_id = int(curs.fetchall()[0][0])

    return flask.jsonify(
        {
            "status": status,
            "comment_id": comment_id
        }
    )

@app.route('/image/<name>')
def main_image_view(name = None):
    return main_image_view_2(conn, name, app_var)

@app.route('/skin_set')
def redir3():
    return flask.redirect('/settings')

@app.route('/settings')
def main_skin_set_dot():
    return main_skin_set_2(conn)

@app.route('/admin/subwikis', methods=['POST', 'GET'])
def subWikiConfig():
    if admin_check() != 1:
        return re_error('/error/3')

    content = '''
        <form method=post>
            <input type=hidden name=submittype value=add>

            <div class=form-group>
                <label>위키 ID:</label><br>
                <input type=text class=form-control name=wikiid>
            </div>

            <div class=form-group>
                <label>언어:</label><br>
                <select class=form-control name=language>
                    <option value=ko-KR>한국어</option>
                    <option value=en-US>English</option>
                </select>
            </div>

            <div class=btns>
                <button type=submit class="btn btn-primary" style="width: 100px;">추가</button>
            </div>
        </form>

        <table class=table>
            <colgroup>
                <col>
                <col style="width: 100px;">
                <col style="width: 140px;">
                <col style="width:  60px;">
            </colgroup>

            <thead>
                <tr>
                    <th>ID</th>
                    <th>언어</th>
                    <th>DB</th>
                    <th>작업</th>
                </tr>
            </thead>

            <tbody id>
                '''

    curs.execute("select id, lang, db from subwikis")

    for swiki in curs.fetchall():
        content += '''
            <tr>
                <td>''' + swiki[0] + '''</td>
                <td>''' + swiki[1] + '''</td>
                <td>''' + swiki[2] + '''</td>
                <td>
                    <form method=post onsubmit="return confirm('삭제하시겠습니까? 데이타베이스는 삭제되지 않습니다.');">
                        <input type=hidden name=wikiid value="''' + swiki[0] + '''">
                        <input type=hidden name=submittype value=add>

                        <button type=submit class="btn btn-danger btn-sm">삭제</button>
                    </form>
                </td>
            </tr>
        '''

    content += '''
            </tbody>
        </table>
    '''

    pagetitle = '하위 위키 관리자'

    if flask.request.method == 'POST':
        wikiid = getForm('wikiid', '')

        if getForm('submittype', '') == 'add':
            if SQLexec("select wikiid from subwikis where wikiid = ?", [wikiid]):
                print(3)
        else:
            print(3)

        conn.commit()

        return redirect('/admin/subwikis')

# API
@app.route('/api/w/<everything:name>', methods=['POST', 'GET'])
def api_w(name = ''):
    return api_w_2(conn, name)

@app.route('/api/raw/<everything:name>')
def api_raw(name = ''):
    return api_raw_2(conn, name)

@app.route('/api/version')
def api_version():
    return api_version_2(conn, r_ver, c_ver)

@app.route('/regc/<name>')
def regc(name = None):
    return regc_2(conn, name)

@app.route('/api/skin_info')
def api_skin_info():
    return api_skin_info_2(conn)

@app.route('/api/thread/<tnum>')
def api_topic_sub(tnum = '', time = ''):
    return api_topic_sub_2(conn, tnum, time)

@app.route('/SQLexec', methods=['POST', 'GET'])
def sql():
    return sql_2(conn)

@app.route('/SQLexec/<key>', methods=['POST', 'GET'])
def sqlexec(key = ''):
    return sqlexec_2(conn, key)

@app.route('/admin/namespaces', methods=['POST', 'GET'])
def dhg87rghug4rhirue():
    return namespaceSettingsPage(conn)

## File
@app.route('/views/easter_egg.html')
def main_easter_egg():
    return main_easter_egg_2(conn)

@app.route('/views/main_css/ccs.html')
def ccs():
    return ccs_2(conn)

@app.route('/views/<everything:name>')
@app.route('/skins/<everything:name>')
def main_views(name = None):
    return main_views_2(conn, name, 'views')

@app.route('/<data>')
def main_file(data = None):
    return main_file_2(conn, data)

@app.route('/cat/<ci>')
def cap_img(ci = None):
    return cap_img_2(conn, ci)

@app.route('/License')
def lice():
    return lice_2(conn)

@app.route('/aclman/del/<id>/<what>/<everything:name>')
def acldel(id = None, name = None, what = None):
    return acldel_2(conn, id, name, what)

@app.route('/aclup/<id>/<what>/<everything:name>')
def aclup(id = None, name = None, what = None):
    return aclup_2(conn, id, name, what)

@app.route('/acldn/<id>/<what>/<everything:name>')
def acldn(id = None, name = None, what = None):
    return acldn_2(conn, id, name, what)

@app.route('/nsup/<id>/<what>/<everything:name>')
def nsup(id = None, name = None, what = None):
    return nsup_2(conn, id, name, what)

@app.route('/nsdn/<id>/<what>/<everything:name>')
def nsdn(id = None, name = None, what = None):
    return nsdn_2(conn, id, name, what)

@app.route('/aclman/add/<what>/<typ>/<perm>/<act>/<everything:name>')
def acladd(what = None, typ = None, perm = None, name = None, act = None):
    return acladd_2(conn, what, typ, perm, name, act)

@app.route('/nsacl/del/<id>/<what>/<everything:name>')
def nsdel(id = None, name = None, what = None):
    return nsdel_2(conn, id, name, what)

@app.route('/nsacl/add/<what>/<typ>/<perm>/<act>/<everything:name>')
def nsadd(what = None, typ = None, perm = None, name = None, act = None):
    return nsadd_2(conn, what, typ, perm, name, act)

@app.route('/vote/<num>', methods=['POST', 'GET'])
def routeVoteScreen(num = '0'):
    return voteScreen(conn, num)

@app.route('/admin/create_vote', methods=['POST', 'GET'])
def routeCreateVote():
    return createVote(conn)

@app.route('/admin/vote/<num>/edit', methods=['POST', 'GET'])
def routeEditVote(num = '0'):
    return editVote(conn, num)

@app.route('/admin/vote/<num>/delete', methods=['POST', 'GET'])
def routeDeleteVote(num = '0'):
    return deleteVote(conn, num)

@app.route('/member/ip_whitelist', methods=['POST', 'GET'])
def mipwlst():
    return ip_whitelist(conn)

## End
@app.errorhandler(404)
def main_error_404(e):
    return main_error_404_2(conn)

@app.errorhandler(405)
def main_error_4034(e):
    return '''
        <title>주의!</title>
        <meta charset=utf-8>
        <meta name=viewport content="width=device-width, initial-scale=1">

        <style>
        	body {
        		overflow: hidden;
        	}

        	body.bluescreen {
        		margin: 0 0 0 0;
        		background-color: #008000;
        		text-align: center;
        		padding-top: 30vh;
        	}

        	div.content {
        		max-width: calc(100% - 300px);
        		text-align: center;
        		display: inline-block;
        	}

        	body.bluescreen .korean {
        		font-family: "IHIYAGI_SYS",iyg,IYAGI,DOSIyagi,"명조","DOSMyungjo","바탕","둥근모꼴","둥근모꼴 일반체";
        		margin: 0 0 0 0;
        	}
        	body.bluescreen .english {
        		font-family: IHIYAGI_SYS,iyg,IYAGI,DOSIyagi,Fixedsys,System,"둥근모꼴","둥근모꼴 일반체";
        		margin: 0 0 0 0;
        	}
        	body.bluescreen p {
        		font-size: 30px;
        		color: #fff;
        	}
        	body.bluescreen .title {
        		display: inline-block;
        		color: #008000;
        		background-color: #fff;
        		margin-bottom: 40px;
        	}
        	.nodisplay {
        		display: none;
        	}
        </style>

        <body class=bluescreen>
        	<div class=content>
        		<p class="korean title">요청이 올바르지 않습니다.
        		<p class=korean>지금요청중인방식 [''' + flask.request.method + ''']이 해당페이지에서 허용되지않은 방식입니다. 주소를 직접입력하였다면 사용할 수 없는기능이니 뒤로 이동하십시오.

        		<div style="text-align: left; padding-left: 50px; display: inline-block; margin-top: 20px;">
        			<p class=korean> * 자동으로 이 메시지가 보였다면 개발자에게 문의하십시오.
        			<p class=korean> * 올바른 링크를 눌렀는지 확인하십시오.
        		</div>

        		<p class=korean>&nbsp;
        		<p class=korean style="padding-left: 80px;">계속하려면 <span class=english>&lt;Alt+Shift+B&gt;</span>글쇠를 누르십시오

        		<a class=nodisplay onclick="history.back();" accesskey=b>뒤로단추</a>
        	</div>
    ''', 405

@app.errorhandler(500)
def Error500(e):
    return '''
        <title>주의!</title>
        <meta charset=utf-8>
        <meta name=viewport content="width=device-width, initial-scale=1">

        <style>
        	body {
        		overflow: hidden;
        	}

        	body.bluescreen {
        		margin: 0 0 0 0;
        		background-color: #008000;
        		text-align: center;
        		padding-top: 30vh;
        	}

        	div.content {
        		max-width: calc(100% - 300px);
        		text-align: center;
        		display: inline-block;
        	}

        	body.bluescreen .korean {
        		font-family: "IHIYAGI_SYS",iyg,IYAGI,DOSIyagi,"명조","DOSMyungjo","바탕","둥근모꼴","둥근모꼴 일반체";
        		margin: 0 0 0 0;
        	}
        	body.bluescreen .english {
        		font-family: IHIYAGI_SYS,iyg,IYAGI,DOSIyagi,Fixedsys,System,"둥근모꼴","둥근모꼴 일반체";
        		margin: 0 0 0 0;
        	}
        	body.bluescreen p {
        		font-size: 30px;
        		color: #fff;
        	}
        	body.bluescreen .title {
        		display: inline-block;
        		color: #008000;
        		background-color: #fff;
        		margin-bottom: 40px;
        	}
        	.nodisplay {
        		display: none;
        	}
        </style>

        <body class=bluescreen>
        	<div class=content>
        		<p class="korean title">주의!
        		<p class=korean>요청을 서버에서 처리하는데 오류 [INTERNAL SERVER ERROR : ''' + str(e).upper() + ''']가 발생했습니다. 이 오류를 해결하는 업데이트가 진행될때까지 기다리거나 새로고침할 수 있습니다.

        		<div style="text-align: left; padding-left: 50px; display: inline-block; margin-top: 20px;">
        			<p class=korean> * 새로고침하거나 <span class=english>&lt;Alt+Shift+B&gt;</span>글쇠를 눌러 뒤로 이동합니다.
        			<p class=korean> * 엔진 개발자에게 해결을 요청합니다. 위의 오류내용을 첨부하십시오.
        			<p class=korean> * 제출값이 올바른지 확인하십시오.
        		</div>

        		<p class=korean>&nbsp;
        		<p class=korean style="padding-left: 80px;">계속하려면 <span class=english>&lt;F5&gt;</span>글쇠를 누르십시오

        		<a class=nodisplay onclick="history.back();" accesskey=b>뒤로단추</a>
        	</div>
    ''', 500

    return '''
        <head>
    			<meta charset="utf-8">
    			<meta name="viewport" content="width=device-width, initial-scale=1">
    			<style type="text/css">.container{border:3px solid #000;max-width: 600px;}.container .content{font-family:NanumGothic;min-height:200px;padding:10px}.container .content h1{font-size:25px;font-weight:400;margin:10px 0 25px}.container p{font-size:15px}.construct-stripe{background-image:repeating-linear-gradient(45deg,#000,#000 30px,#e2bd00 0,#e2bd00 60px);height:20px}</style>
    	</head><body>
    		<div class="container">
    			<div class="construct-stripe"></div>
    			<div class="content">
    				<h1>오류</h1>

    				<p>내부 응용 프로그램 오류가 발생했습니다.<br><br>
    				<a href="?">[새로고침]</a><br>
    				</p>
    			</div>
    			<div class="construct-stripe"></div>

    	</div></body>
    ''', 500

@app.route('/exp/posttest', methods=['POST', "GET"])
def weufhtw348htru3():
    if flask.request.method == 'POST':
        return flask.request.form.get('a', '0') + " " + flask.request.form.get('b', '0')
    return '''
        ===
        <FORM METHOD=POST ID=1>
            <FORM METHOD=POST ID=2>
                <INPUT NAME=a>
                <INPUT NAME=b>

                <BUTTON TYPE=SUBMIT>S</BUTTON>
            </FORM>

            <INPUT NAME=a>
            <BUTTON TYPE=SUBMIT>S</BUTTON>
        </FORM>
        ---
    '''

@app.route('/admin/email_whitelist', methods=['POST', 'GET'])
def dgrj9iuj349i3awiy9i():
    return emailWhtLst(conn)

app.secret_key = rep_key
app.wsgi_app = werkzeug.debug.DebuggedApplication(app.wsgi_app, False)
app.debug = False

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(tornado.wsgi.WSGIContainer(app))
    http_server.listen(server_set['port'], address = server_set['host'])

    tornado.ioloop.IOLoop.instance().start()
