from .tool.func import *

def main_manager_2(conn, num, r_ver):
    curs = conn.cursor()

    title_list = {
        0 : [load_lang('document_name'), 'acl', '문서 ACL 변경'],
        1 : [0, 'check', ''],
        2 : [load_lang('file_name'), 'plus_file_filter', '파일명 필터 추가'],
        3 : [0, 'admin', ''],
        4 : [0, 'record', ''],
        5 : [0, 'topic_record', ''],
        6 : [load_lang('name'), 'admin_plus', '관리자 그룹 추가'],
        7 : [load_lang('name'), 'plus_edit_filter', ''],
        8 : [load_lang('document_name'), 'search', '검색'],
        9 : [0, 'block_user', ''],
        10 : [0, 'block_admin', ''],
        11 : [load_lang('document_name'), 'watch_list', ''],
        12 : [load_lang('compare_target'), 'check', ''],
        13 : [load_lang('document_name'), 'edit', '문서 편집']
    }
    a=''
    b=''
    c=''
    d=''
    e=''
    f=''
    g=''

    unav = ' (사용불가능)'
    if getperm('admin')==0:
        a=unav
    if getperm('login_history')==0:
        b=unav
    if getperm('ipacl')==0:
        c=unav
    if getperm('suspend_account')==0:
        d=unav
    if getperm('grant')==0:
        e=unav
    if getperm('developer')==0:
        g=unav

    if num == 1:
        return easy_minify(flask.render_template(skin_check(),
            imp = [load_lang('admin_tool'), wiki_set(), custom(), other2([0, 0])],
            data =  '''
                    <h2>관리 기능</h2>
                    <ul class=wiki-list>
                        <li><a href="/manager/2">''' + load_lang('acl_change') + '''</a>''' + a + '''</li>
                        <li><a href="/admin/login_history">''' + load_lang('check_user') + '''</a>''' + b + '''</li>
                        <li><a href="/admin/ipacl">IPACL</a>''' + c + '''</li>
                        <li><a href="/admin/suspend_account">사용자 ''' + load_lang('ban') + '''</a>''' + d + '''</li>
                        <li><a href="/admin/grant">''' + load_lang('authorize') + '''</a>''' + e + '''</li>
                        <li><a href="/give_log">''' + load_lang('admin_group_list') + '''</a>''' + f + '''</li>
                    </ul>
                    <br>
                    <h2>위키 구성</h2>
                    <ul class=wiki-list>
                        <li><a href="/manager/8">''' + load_lang('admin_group_add') + '''</a>''' + g + '''</li>
                        <li><a href="/admin/config">위키 ''' + load_lang('setting') + '''</a>''' + g + '''</li>
                    </ul>
                    <h2>''' + load_lang('filter') + '''</h2>
                    <ul class=wiki-list>
                        <li><a href="/admin/inter_wiki">''' + load_lang('interwiki_list') + '''</a></li>
                        <li><a href="/admin/email_filter">''' + load_lang('email_filter_list') + '''</a></li>
                        <li><a href="/admin/username_filters">''' + load_lang('id_filter_list') + '''</a>''' + g + '''</li>
                        <li><a href="/admin/file_filter">''' + load_lang('file_filter_list') + '''</a></li>
                        <li><a href="/admin/edit_filters">''' + load_lang('edit_filter_list') + '''</a></li>
                    </ul>
                    <br>
                    <h2>''' + load_lang('server') + '''</h2>
                    <ul class=wiki-list>
                        <li><a href="/admin/db_indexing">''' + load_lang('indexing') + '''</a>''' + g + '''</li>
                        <li><a href="/admin/engine_restart">''' + load_lang('wiki_restart') + '''</a>''' + g + '''</li>
                    </ul>
                    ''',
            menu = [['other', load_lang('return')]]
        ))
    elif not num - 1 > len(title_list):
        if flask.request.method == 'POST':
            if flask.request.args.get('plus', None):
                return redirect('/' + title_list[(num - 2)][1] + '/' + url_pas(flask.request.args.get('plus', None)) + '?plus=' + flask.request.form.get('name', None))
            else:
                return redirect('/' + title_list[(num - 2)][1] + '/' + url_pas(flask.request.form.get('name', None)))
        else:
            if title_list[(num - 2)][0] == 0:
                placeholder = load_lang('user_name')
            else:
                placeholder = title_list[(num - 2)][0]

            return easy_minify(flask.render_template(skin_check(),
                imp = [title_list[(num - 2)][2], wiki_set(), custom(), other2([0, 0])],
                data =  '''
                        <form method="post">
                            <div><label>''' + placeholder + ''' : </label><br>
                            <input name="name" type="text" style="width: 250px;" class=form-control></div><div class=btns>
                            <button type="submit" class="btn btn-info pull-right" id="moveBtn" style="width:100px;">확인</button></div>
                        </form>
                        ''',
                menu = [['manager', load_lang('return')]]
            ))
    else:
        return redirect()

def contribution(typ):
    if flask.request.method == 'POST':
        return redirect('/contribution/' + getForm('usertype') + '/' + getForm('username') + '/' + typ)

    if typ == 'document':
        title = '문서'
    else:
        title = '토론'

    return easy_minify(flask.render_template(skin_check(),
        imp = [title + ' 기여 목록 조회', wiki_set(), custom(), other2([0, 0])],
        data =  '''
                <form method="post">
                    <div><label>사용자 이름 : </label><br>
                    <input name=username id=usernameInput type="text" style="width: 250px;" class=form-control></div>
                    <div>
                    <label style="display: inline-block;"><input type=radio name=usertype value=ip> 아이피</label>
                    <label style="display: inline-block;"><input type=radio name=usertype value=author checked selected> 사용자</label>
                    </div>

                    <div class=btns>
                    <button type="submit" class="btn btn-info pull-right" id="moveBtn" style="width: 100px;">확인</button></div>
                </form>
                ''',
        menu = [['manager', load_lang('return')]]
    ))