from .tool.func import *

def ifstar(conn, unm):
    curs = conn.cursor()

    curs.execute("select doc, user from star")
    lst = curs.fetchall()
    div = '<ul>'
    sub = 0
    ret = 0
    if lst:
        for dc in lst:
            if dc[1] == ip_check():
                curs.execute("select date from data where title = ?", [dc[0]])
                edt = '알 수 없음'
                edtf = curs.fetchall()
                if edtf:
                    if edtf[0][0] == '':
                        edt = '알 수 없음'
                    else:
                        edt = edtf[0][0]
                else:
                    edt = '알 수 없음'

                if dc[0] == unm:
                    ret = 1
                div += '<li><a href="/w/' + url_pas(dc[0]) + '">' + dc[0] + '</a> (수정 시각:' + edt + ')</li>'

    div += '</ul>'

    return ret

def starc(conn, unm):
    curs = conn.cursor()

    curs.execute("select doc, user from star")
    lst = curs.fetchall()
    div = '<ul>'
    sub = 0
    ret = 0
    if lst:
        for dc in lst:
            curs.execute("select date from data where title = ?", [dc[0]])
            edt = '알 수 없음'
            edtf = curs.fetchall()
            if edtf:
                if edtf[0][0] == '':
                    edt = '알 수 없음'
                else:
                    edt = edtf[0][0]
            else:
                edt = '알 수 없음'

            if dc[0] == unm:
                ret = ret + 1
            div += '<li><a href="/w/' + url_pas(dc[0]) + '">' + dc[0] + '</a> (수정 시각:' + edt + ')</li>'

    div += '</ul>'

    return ret

def view_read_2(conn, name):
    curs = conn.cursor()

    if name == '' or name == ' ':
        return redirect('/');

    sub = ''
    acl = ''
    div = ''

    num = flask.request.args.get('rev', None)
    curs.execute("select title from history where title = ? and id = ?", [name, str(num)])
    if not(curs.fetchall()) and num:
        return showError('해당 리비전이 존재하지 않습니다.')

    if num:
        num = int(number_check(num))
    else:
        if not flask.request.args.get('from', None):
            curs.execute("select title from back where link = ? and type = 'redirect'", [name])
            redirect_data = curs.fetchall()
            if redirect_data and not(flask.request.args.get('noredirect', None)):
                return redirect('/w/' + redirect_data[0][0] + '?from=' + name)
    discuss_ongoing = 0
    curs.execute("select sub from rd where title = ? and not stop = 'O' and not agree = 'O' order by date desc", [name])
    if curs.fetchall():
            discuss_ongoing = 1

    curs.execute("select link from back where title = ? and type = 'cat' order by link asc", [name])

    curs.execute("select title from data where title like ?", ['%' + name + '/%'])
    if curs.fetchall():
        down = 1
    else:
        down = 0

    m = re.search("^(.*)\/(.*)$", name)
    if m:
        uppage = m.groups()[0]
    else:
        uppage = 0

    if re.search('^분류:', name):
        curs.execute("select link from back where title = ? and type = 'cat' order by link asc", [name])
        back = curs.fetchall()
        if back:
            div = '<br><h2 id="cate_normal">"' + name.replace('분류:', '') + '" ' + load_lang('category') + '에 속하는 모든 문서</h2>'

            if name == '분류:파일':
                div += '''
                    <style>
                        .xp-icon-link {
                            display: inline-block;
                            vertical-align: top;
                        }

                        .xp-icon {
                            display: inline-block;
                            margin: 5px;
                        }

                        .xp-icon td {
                            border: none;
                            background: transparent;
                        }

                        .xp-icon-container {
                            width: 96px;
                            height: 96px;
                            background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAABD0lEQVR4nO3SPUoDURiG0dn/EiyzArfgBlKkt7Oz0C5l0kQU8wOCc3PJc154qmFg+M4si5nZlDsMyi7ssH3ZDGmBcLZhx4dwvuHHh/C9ux3/F8KjNy9AoVsIxb9xSH8C+Hpp/7nTP/UT4iaAw4+BuApw7w8sBABAOwAA2gEA0A4AgHYAALQDAKAdAADtAABoBwBAOwAA2gEA0A4AgHYAZgb4eHvWygEA0A4AgHYAALQDAKAdAADtAABoBwBAOwAA2gEA0A4AgHYAALQDAKAdAADtAMwM8P76pJUDAKAdAADtAABoBwBAOwAA2gEA0A4AgHYAALQDAKAdAADtAABoBwBAOwATAyynh1o/M7MZdgREziYFLq9OHgAAAABJRU5ErkJggg==) !important;
                        }

                        .xp-icon-container img {
                            width: 44px;
                            height: 38px;
                        }

                        .xp-icon-label {
                            text-align: center;
                        }
                    </style>
                '''
            cdiv = ''
            if re.search('^분류[:]파일[/]', name):
                cdiv += '''
                    <style>
                        .xp-icon {
                            display: inline-block;
                            margin: 5px;
                        }

                        .xp-icon-container {
                            width: 96px;
                            height: 96px;
                            background-size: cover !important;
                        }

                        .xp-icon-label {
                            text-align: center;
                        }
                    </style>

                    <script>
                        $(function() {
                            $(".xp-icon-container").click(function() {
                                var thisObj = $(this);
                                $("#imgPreviewFrame").attr("src", thisObj.attr("data-image-src"));
                            });
                        });
                    </script>

                    <div style="overflow: scroll; white-space: nowrap;">
                '''

            u_div = ''
            xmrtnrlsmd = '' #특수기능
            tkdydwk = '' #사용자
            xmf = '' #틀
            vkdlf = '' #파일
            xhfhs = '' #토론
            xnvy = '' #투표
            dustmqwkd = '' #연습장
            gbwlxhd = '' #휴지통
            wikins = '' #위키이름공간
            ucnt = 0
            ccnt = 0

            for data in back:
                if re.search('^분류:', data[0]):
                    if name == '분류:파일':
                        curs.execute("select link from back where title = ? and type = 'cat'", [data[0]])
                        imglst = curs.fetchall()

                        try:
                            piece = os.path.splitext(imglst[0][0].replace(imglst[0][0].split(':')[0] + ':', ''))
                            i1s = sha224(piece[0]) + piece[1]
                        except:
                            i1s = ''
                        try:
                            piece = os.path.splitext(imglst[1][0].replace(imglst[1][0].split(':')[0] + ':', ''))
                            i2s = sha224(piece[0]) + piece[1]
                        except:
                            i2s = ''
                        try:
                            piece = os.path.splitext(imglst[2][0].replace(imglst[2][0].split(':')[0] + ':', ''))
                            i3s = sha224(piece[0]) + piece[1]
                        except:
                            i3s = ''
                        try:
                            piece = os.path.splitext(imglst[3][0].replace(imglst[3][0].split(':')[0] + ':', ''))
                            i4s = sha224(piece[0]) + piece[1]
                        except:
                            i4s = ''

                        u_div += '''
                            <a href="/w/''' + url_pas(data[0]) + '''" class=xp-icon-link>
                                <table class=xp-icon>
                                    <tbody>
                                        <tr>
                                            <td class=xp-icon-container>
                                                <table style="margin: 0 auto auto 3px;">
                                                    <tbody>
                                                        <tr>
                                                            <td style="width: 44px; height: 33px; background: url('/image/''' + i1s + '''\') center top; background-size: cover;"></td>
                                                            <td style="width: 44px; height: 33px; background: url('/image/''' + i2s + '''\') center top; background-size: cover;"></td>
                                                        </tr>

                                                        <tr>
                                                            <td style="width: 44px; height: 33px; background: url('/image/''' + i3s + '''\') center top; background-size: cover;"></td>
                                                            <td style="width: 44px; height: 33px; background: url('/image/''' + i4s + '''\') center top; background-size: cover;"></td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>

                                        <tr>
                                            <td class=xp-icon-label>
                                                ''' + html.escape(data[0]) + '''
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </a>
                        '''
                    else:
                        u_div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a></li>'

                    ucnt += 1
                else:
                    if re.search("^분류[:]파일[/]", name):
                        piece = os.path.splitext(data[0].replace(data[0].split(':')[0] + ':', ''))
                        imgsrc = sha224(piece[0]) + piece[1]

                        cdiv += '''
                            <a class=xp-icon>
                                <table>
                                    <tbody>
                                        <tr>
                                            <td class=xp-icon-container data-image-src="/image/''' + imgsrc + '''" style="background: url(\'/image/''' + imgsrc + '''\') center top;">
                                            </td>
                                        </tr>

                                        <tr>
                                            <td class=xp-icon-label>
                                                <a href="/w/''' + url_pas(data[0]) + '''">
                                                    ''' + html.escape(data[0]) + '''
                                                </a>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </a>
                        '''
                    else:
                        cdiv += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a></li>'

                    ccnt += 1

            if re.search('^분류[:]파일[/]', name):
                cdiv += '</div><img id=imgPreviewFrame></img>'

            div += '전체 ' + str(ccnt) + '개 문서<br><ul>' + cdiv + '</ul>'

            if div == '<br><h2 id="cate_normal">' + load_lang('category') + '</h2><ul></ul>':
                div = ''

            if u_div != '':
                div += '<br><h2 id="cate_under">' + load_lang('under_category') + '</h2>전체 ' + str(ucnt) + '개 문서<br><ul>' + u_div + '</ul>'


    if num:
        curs.execute("select title from history where title = ? and id = ? and hide = 'O'", [name, str(num)])
        if curs.fetchall() and admin_check(6) != 1:
            return redirect('/history/' + url_pas(name))

        curs.execute("select title, data from history where title = ? and id = ?", [name, str(num)])
    else:
        curs.execute("select title, data from data where title = ?", [name])

    data = curs.fetchall()
    if data:
        else_data = data[0][1]
    else:
        else_data = None
    adm = 0
    blk = 0
    m = re.search("^사용자:([^/]*)", name)
    if m:
        g = m.groups()

        curs.execute("select acl from user where id = ?", [g[0]])
        test = curs.fetchall()
        if test and test[0][0] != 'user':
            acl = ''
            #acl = ' (' + load_lang('admin') + ')'
            adm = 1
        if ban_check(g[0]) == 1:
            sub += ''
            #sub += ' (' + load_lang('blocked') + ')'
            blk = 1
        else:
            acl = ''

    curs.execute("select dec from acl where title = ?", [name])
    data = curs.fetchall()
    if data:
        acl += ''

    if flask.request.args.get('from', None) and else_data:
        else_data = re.sub('^\r\n', '', else_data)
        else_data = re.sub('\r\n$', '', else_data)

    end_data = render_set(
        title = name,
        data = else_data
    )
    err = 0
    nd = 0
    st = 1
    if end_data == 'HTTP Request 401.3':
        response_data = 401
        end_data = '<h2 style="border:none;font-weight:600">' + aclmsg(name, 'read')[1] + ' 읽기 권한이 부족합니다. ' + aclmsg(name, 'read')[2] + ' 해당 문서의 <a href="/acl/' + url_pas(name) + '">ACL 탭</a>을 확인하시기 바랍니다.</h2>'
        err = 1
    elif end_data == 'HTTP Request 404':
        response_data = 404
        end_data = '<p style="margin-bottom: 1em;">' + load_lang('decument_404_error') + '</p><p><a rel="nofollow" href="/edit/' + url_pas(name) + '">[새 문서 만들기]</a></p>'
        err = 1
        nd = 1
        st = 0
        curs.execute('select ip, date, leng, send, id, i, hide from history where title = ? order by date desc', [name])
        sql_d = curs.fetchall()
        if sql_d:
            ic = 0
            end_data += '<br><br><h3 style="border:none">이 문서의 ' + load_lang('history') + '</h3><ul>'
            for i in sql_d:
                if ic >= 3:
                    break
                if re.search("\+", i[2]):
                    leng = '(<span style="color:green;">' + i[2] + '</span>)'
                elif re.search("\-", i[2]):
                    leng = '(<span style="color:red;">' + i[2] + '</span>)'
                else:
                    leng = '(<span style="color:gray;">' + i[2] + '</span>)'
                if admin_check(6) != 1 and i[6] == 'O':
                    continue
                end_data += '<li>' + i[1] + ' <b>r' + str(i[4]) + '</b> <i>' + str(i[5]) + '</i> ' + leng + ' ' + ip_pas(i[0]) + ' (<span style="color:gray">' + i[3] + '</span>)</li>'
                ic += 1
            end_data += '</ul><a href="/history/' + url_pas(name) + '">[더보기]</a>'
    else:
        response_data = 200

    if num:
        menu = [['history/' + url_pas(name), load_lang('history')]]
        sub = ' (r' + str(num) + ' 판)'
        acl = ''
        r_date = 0
    else:
        menu = [['xref/' + url_pas(name), load_lang('backlink')], ['discuss/' + url_pas(name), load_lang('discussion')], ['edit/' + url_pas(name), load_lang('edit')], ['history/' + url_pas(name), load_lang('history')], ['acl/' + url_pas(name), load_lang('acl')]]



        if uppage != 0:
            menu += [['w/' + url_pas(uppage), load_lang('upper')]]

        if down:
            menu += [['down/' + url_pas(name), load_lang('sub')]]

        curs.execute("select date from history where title = ? order by date desc limit 1", [name])
        date = curs.fetchall()
        if date:
            r_date = date[0][0]
        else:
            r_date = 0
    us = 0
    un = ''
    if re.search("^사용자:([^/]*)", name):
        menu += [['contribution/author/' + name.replace('사용자:','') + '/document', '기여내역']]
        us = 1
        un = name.replace('사용자:','')

    div = end_data + div

    adsense_code = '<div align="center" style="display: block; margin-bottom: 10px;">{}</div>'

    curs.execute("select data from other where name = 'adsense'")
    adsense_enabled = curs.fetchall()[0][0]
    if adsense_enabled == 'True':
        curs.execute("select data from other where name = 'adsense_code'")
        adsense_code = adsense_code.format(curs.fetchall()[0][0])
    else:
        adsense_code = adsense_code.format('')

    curs.execute("select data from other where name = 'body'")
    body = curs.fetchall()
    if body:
        div = body[0][0] + '' + div

    ab = ''
    if render_set(title = name, data = else_data) != 'HTTP Request 401.3' and render_set(title = name, data = else_data) != 'HTTP Request 404':
        curs.execute("select link from back where link = ? and type = 'cat'", [name])
        if not(curs.fetchall()) and not(re.search('^사용자:', name)) and not(re.search('^연습장:', name)) and not(name == '분류:분류'):
            ab += '''<div class="alert alert-info alert-dismissible" id="wikiNoCategoryAlert" role="alert" style="opacity: 0.9490137878803078;">
<button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
        <span class="sr-only">Close</span>
        </button>
이 문서는 분류가 되어 있지 않습니다. <a href="/w/%EB%B6%84%EB%A5%98:%EB%B6%84%EB%A5%98">분류:분류</a>에서 적절한 분류를 찾아 문서를 분류해주세요!
</div>'''

    if render_set(title = name, data = else_data) != 'HTTP Request 401.3' and render_set(title = name, data = else_data) != 'HTTP Request 404':
        if re.search("^사용자:([^/]*)", name):
            if user_isadmin(5, name.replace('사용자:','')) == 1 or getperm('arbiter', name.replace('사용자:','')) == 1 or getperm('tribune', name.replace('사용자:','')) == 1 or getperm('noban', name.replace('사용자:','')) == 1:
                ab += '<div style="display:block;border-width: 5px 1px 1px; border-style: solid; border-color: orange gray gray; padding: 10px; margin-bottom: 10px;" onmouseover="this.style.borderTopColor=\'red\';" onmouseout="this.style.borderTopColor=\'orange\';"><span style="font-size:14pt">이 사용자는 특수 권한을 가지고 있습니다.</span></div>'

            if blk == 1:
                ab += '<div style="border-width: 5px 1px 1px; border-style: solid; border-color: red gray gray; padding: 10px; margin-bottom: 10px;" onmouseover="this.style.borderTopColor=\'blue\';" onmouseout="this.style.borderTopColor=\'red\';"> <span style="font-size: 14pt">이 사용자는 차단된 사용자입니다.</span><br><br>' + re_tul('/ban',name.replace('사용자:','')) + '</div>'
        if name.split(':')[0] in getNamespaces(fileOnly = True):
            piece = os.path.splitext(name.replace(name.split(':')[0] + ':', ''))
            ab += '<img src="/image/' + sha224(piece[0]) + piece[1] + '">'
    div = ab + adsense_code + '<div class=wiki-content>' + div + '</div>'

    if flask.request.args.get('from', None):
        div = '''
            <div id=wikiFromAlert class="alert alert-info" role="alert">
                <a class=document rel=nofollow href="/w/''' + url_pas(flask.request.args.get('from', None)) + '?noredirect=1">' + flask.request.args.get('from', None) + '</a>에서 넘어옴' + '''
            </div>
        ''' + div

    dno = flask.request.args.get('show', name)
    dn = dno

    curs.execute("select date from data where title = ?", [name])
    edt = '알 수 없는 시간'
    edtf = curs.fetchall()
    if edtf:
        if edtf[0][0] == '':
            edt = '알 수 없는 시간'
        else:
            edt = edtf[0][0]
    else:
        edt = '알 수 없는 시간'

    rdg = 1

    ddd = edt.split(' ')[0]
    ttt = edt.split(' ')[1]
    #edt = '<time datetime="' + ddd + 'T' + ttt + '.000Z" data-format="Y-m-d H:i:sO">' + edt + '</time>'

    if end_data == 'HTTP Request 404':
        strd = 0
        strc = ''
    else:
        strd = ifstar(conn, name)
        strc = starc(conn, name)

    if isinstance(strc, int):
        dgdfgsd = 23
    else:
        strc = '?'

    ns = ''

    dcn = dn

    if name.split(':')[0] in getNamespaces():
        ns = name.split(':')[0]
        dn = name.replace(name.split(':')[0] + ':', '')

    return easy_minify(flask.render_template(skin_check(),
        imp = [dcn, wiki_set(), custom(), other2([sub + acl, r_date]), edt],
        data = div,
        menu = menu,
        edt = edt,
        rdg = 1,
        st = st,
        us = us,
        un = un,
        strd = strd,
        strc = strc,
        nd = nd,
        err = err,
        ns = ns,
        nsdn = dn.replace(ns + ':', ''),
        dn = dn,
        discuss_ongoing = discuss_ongoing,
        rev = flask.request.args.get('rev', None)
    )), response_data

def namespaceSettingsPage(conn):
    curs = conn.cursor();

    if admin_check() != 1:
        return showError('이름공간 관리자를 액세스할 수 없습니다. (2301)<br><br>액세스가 거부되었습니다.');

    content = '''
        <form method=post class=settings-section>
            <div class=form-group>
                <label>추가할 이름공간 명칭:</label><br>
                <input type=text class=form-control style="width: 250px;" name=namespace id=namespaceInput>
            </div>

            <div class=form-group>
                <label>파일 이름공간:</label><br>
                <div class=checkbox>
                    <input type=checkbox class=form-control style="width: 20px;" name=isfile>
                </div>
            </div>
            <div class=form-group>
                <label>사용불가능:</label><br>
                <div class=checkbox>
                    <input type=checkbox class=form-control style="width: 20px;" name=unuseable>
                </div>
            </div>
            <div class=form-group>
                <label>최근 변경내역에 기록하지 않음:</label><br>
                <div class=checkbox>
                    <input type=checkbox class=form-control style="width: 20px;" name=nolog>
                </div>
            </div>

            <div class=btns>
                <button class="btn btn-info" style="width: 100px;" id=submitBtn type=submit>추가</button>
            </div>
            <input type=hidden name=submittype value=add>
        </form>

        <br>

        <table class=table>
            <colgroup>
                <col>
                <col style="width: 100px;">
                <col style="width: 100px;">
                <col style="width: 100px;">
                <col style="width: 80px;">
            </colgroup>

            <thead>
                <tr>
                    <th>이름공간</th>
                    <th>파일</th>
                    <th>비활성</th>
                    <th>기록</th>
                    <th>작업</th>
                </tr>
            </thead>

            <tbody id=namespaceList>
    ''';

    for namespace in getNamespaces(builtinOnly = True):
        if namespace in getNamespaces(unuseableOnly = True):
            unuseable = '<td>예</td>'
        else:
            unuseable = '<td>아니오</td>'
        if namespace in getNamespaces(fileOnly = True):
            isfile = '<td>예</td>'
        else:
            isfile = '<td>아니오</td>'

        if namespace in getNamespaces(nologOnly = True):
            nolog = '<td>아니오</td>'
        else:
            nolog = '<td>예</td>'

        content += '''
            <tr>
                <td>''' + html.escape(namespace) + '''</td>
                ''' + isfile + '''
                ''' + unuseable + '''
                ''' + nolog + '''
                <td>
                    <button type=button disabled title="기본 이름공간으로 삭제할 수 없습니다." class="btn btn-danger btn-sm">삭제</button>
                </td>
            </tr>
        ''';

    for namespace in getNamespaces(customOnly = True):
        if namespace in getNamespaces(unuseableOnly = True):
            unuseable = '<td>예</td>'
        else:
            unuseable = '<td>아니오</td>'
        if namespace in getNamespaces(fileOnly = True):
            isfile = '<td>예</td>'
        else:
            isfile = '<td>아니오</td>'

        if namespace in getNamespaces(nologOnly = True):
            nolog = '<td>아니오</td>'
        else:
            nolog = '<td>예</td>'

        content += '''
            <tr>
                <td>''' + html.escape(namespace) + '''</td>
                ''' + isfile + '''
                ''' + unuseable + '''
                ''' + nolog + '''
                <td>
                    <form method=post onsubmit="return confirm('이 이름공간을 삭제하시겠습니까? 정의한 이름공간 ACL은 삭제되지 않습니다.');">
                        <input type=hidden name=submittype value=delete>
                        <input type=hidden name=namespace value="''' + html.escape(namespace) + '''">
                        <button type=submit class="btn btn-danger btn-sm">삭제</button>
                    </form>
                </td>
            </tr>
        ''';

    content += '''
            </tbody>
        </table>
    ''';

    #create table namespaces (namespace text default '', unuseable text default '0', isfile text default '0', nolog text default '0')
    if flask.request.method == 'POST':
        if getForm('submittype') == 'delete':
            if not getForm('namespace') in getNamespaces(customOnly = True):
                return easy_minify(flask.render_template(skin_check(),
                    imp = ['이름공간 관리자', wiki_set(), custom(), other2([0, 0])],
                    data = alertBalloon('해당 이름공간을 삭제할 수 없습니다. 해당 이름공간이 존재하는지, 그리고 사용가능한지 확인하십시오.') + content,
                    menu = 0,
                    err = 1
                ))
            curs.execute("delete from namespaces where namespace = ?", [getForm('namespace')])
        else:
            if getForm('namespace') in getNamespaces():
                return easy_minify(flask.render_template(skin_check(),
                    imp = ['이름공간 관리자', wiki_set(), custom(), other2([0, 0])],
                    data = alertBalloon('해당 이름공간이 이미 존재합니다.') + content,
                    menu = 0,
                    err = 1
                ))
            if getForm('namespace') == '' or re.search('^\s', getForm('namespace')) or re.search('\s$', getForm('namespace')) or re.search('(?:[^A-Za-z0-9_ㄱ-힣 -])', getForm('namespace')):
                return easy_minify(flask.render_template(skin_check(),
                    imp = ['이름공간 관리자', wiki_set(), custom(), other2([0, 0])],
                    data = alertBalloon('이름공간 \'' + html.escape(getForm('namespace')) + '\'이 올바르지 않습니다.') + content,
                    menu = 0,
                    err = 1
                ))
            if getForm('unuseable', 0) != 0:
                unuseable = '1'
            else:
                unuseable = '0'

            if getForm('isfile', 0) != 0:
                isfile = '1'
            else:
                isfile = '0'

            if getForm('nolog', 0) != 0:
                nolog = '1'
            else:
                nolog = '0'
            curs.execute("insert into namespaces (namespace, unuseable, isfile, nolog) values (?, ?, ?, ?)", [getForm('namespace'), unuseable, isfile, nolog])

        conn.commit()

        return redirect('/admin/namespaces')

    return easy_minify(flask.render_template(skin_check(),
        imp = ['이름공간 관리자', wiki_set(), custom(), other2([0, 0])],
        data = content,
        menu = 0
    ))

def libertyRedirect2(conn, name):
    curs = conn.cursor()

    curs.execute("select start from redirect where end = ? order by start asc", [name])
    dbData = curs.fetchall()
    data = '''<form method="POST">
        출발지 이름 : <br><input type="text" name="start"><div class="btns pull-right"><button type="submit" class="btn btn-info" style="width:120px">추가</button></div><br><hr><br>
    '''
    data += '''<table class="table"><colgroup> <col> <col style="width: 90%;"> <col style="width: 10%;"> </colgroup><style>.nohov:hover { background-color: transparent !important; }</style> <tbody><tr class="nohov" style="border-bottom: 2px solid #eceeef;"> <td><b>출발지</b> </td><td><b>삭제</b> </td></tr>'''

    for lst in dbData:
        data += '<tr><td>' + lst[0] + '</td><td><a href="/redirdel/' + url_pas(lst[0]) + '/' + url_pas(name) + '" class="btn btn-danger btn-sm">삭제</a></td></tr>'

    data += '''</tbody></table></form>'''

    if flask.request.method == 'POST':
        if getacl(name, 'edit'):
            return re_error('/error/3')
        curs.execute("select start from redirect where end = ?", [name])
        if curs.fetchall():
            return easy_minify(flask.render_template(skin_check(),
                imp = [name, wiki_set(), custom(), other2([' (넘겨주기 문서)', 0])],
                data = '''<div class="alert alert-danger alert-dismissible" role="alert">
                        <strong>[오류!]</strong> 해당 출발지가 이미 있읍니다.
                        </div>''' + data,
                menu = [['/w/' + name, '취소']]
            ))

        curs.execute("insert into redirect (start, end) values (?, ?)", [flask.request.form.get('start', '-'), name])

        return redirect('/redirect/' + url_pas(name))
    else:
        return easy_minify(flask.render_template(skin_check(),
            imp = [name, wiki_set(), custom(), other2([' (넘겨주기 문서)', 0])],
            data = data,
            menu = [['/w/' + name, '취소']]
        ))

