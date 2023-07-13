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

    sub = ''
    acl = ''
    div = ''

    num = flask.request.args.get('num', None)
    if num:
        num = int(number_check(num))
    else:
        if not flask.request.args.get('from', None):
            curs.execute("select title from back where link = ? and type = 'redirect'", [name])
            redirect_data = curs.fetchall()
            if redirect_data and not(flask.request.args.get('noredirect', None)):
                return redirect('/w/' + redirect_data[0][0] + '?from=' + name)

    curs.execute("select sub from rd where title = ? and not stop = 'O' order by date desc", [name])
    if curs.fetchall():
        sub += '' #' (' + load_lang('discussion') + ' 진행 중)'

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
            div = '<br><h2 id="cate_normal">' + load_lang('category') + '</h2><ul>'
            u_div = ''

            for data in back:    
                if re.search('^분류:', data[0]):
                    u_div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a></li>'
                else:
                    curs.execute("select title from back where title = ? and type = 'include'", [data[0]])
                    db_data = curs.fetchall()
                    if db_data:
                        div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a> <a id="inside" href="/xref/' + url_pas(data[0]) + '">(' + load_lang('backlink') + ')</a></li>'
                    else: 
                        div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a></li>'

            div += '</ul>'
            
            if div == '<br><h2 id="cate_normal">' + load_lang('category') + '</h2><ul></ul>':
                div = ''
            
            if u_div != '':
                div += '<br><h2 id="cate_under">' + load_lang('under_category') + '</h2><ul>' + u_div + '</ul>'


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
        end_data = '<h2 style="border:none;font-weight:600">' + load_lang('authority_error') + '</h2>'
        err = 1
    elif end_data == 'HTTP Request 404':
        response_data = 404
        end_data = '<p style="margin-bottom: 1em;">' + load_lang('decument_404_error') + '</p><p><a rel="nofollow" href="/edit/' + url_pas(name) + '">[새 문서 만들기]</a></p>'
        err = 1
        nd = 1
        st = 0
        curs.execute('select ip, date, leng, send, id, i from history where title = ? order by date desc', [name])
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
        menu = [['xref/' + url_pas(name), load_lang('backlink')], ['topic/' + url_pas(name), load_lang('discussion')], ['edit/' + url_pas(name), load_lang('edit')], ['history/' + url_pas(name), load_lang('history')], ['acl/' + url_pas(name), load_lang('acl')]]

        

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
    
    
    if adm == 1:
        ab += '<div style="border-width: 5px 1px 1px; border-style: solid; border-color: orange gray gray; padding: 10px; margin-bottom: 10px;" onmouseover="this.style.borderTopColor=\'red\';" onmouseout="this.style.borderTopColor=\'orange\';"><span style="font-size:14pt">이 사용자는 특수 권한을 가지고 있습니다.</span></div>'
    if blk == 1:
        ab += '<div style="border-width: 5px 1px 1px; border-style: solid; border-color: red gray gray; padding: 10px; margin-bottom: 10px;" onmouseover="this.style.borderTopColor=\'blue\';" onmouseout="this.style.borderTopColor=\'red\';"> <span style="font-size: 14pt">이 사용자는 차단된 사용자입니다.</span><br><br>' + re_tul('/ban',name.replace('사용자:','')) + '</div>'
    div = ab + adsense_code + '<div>' + div + '</div>'
    
    if flask.request.args.get('from', None):
        div = '''
            <div id="redirect" style="padding:0.5rem 0.8rem;color:#31708f;background-color:#d9edf7;border-color:#bcdff1;padding-right: 30px;padding:10px;margin-bottom:1rem;border:1px solid #bcdff1;border-radius:.25rem;">
                <a href="/w/''' + url_pas(flask.request.args.get('from', None)) + '?noredirect=1">' + flask.request.args.get('from', None) + '</a>에서 넘어옴' + '''
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
        
    if re.search("^파일:([^/]*)", dn):
        dn = dn.replace('파일:', '')
        ns = '파일:'
    if re.search("^틀:([^/]*)", dn):
        dn = dn.replace('틀:', '')
        ns = '틀:'
    if re.search("^사용자:([^/]*)", dn):
        dn = dn.replace('사용자:', '')
        ns = '사용자:'
    if re.search("^" + str(wiki_set()[0]) + ":([^/]*)", dn):
        dn = dn.replace(str(wiki_set()[0]) + ':', '')
        ns = str(wiki_set()[0]) + ':'
    if re.search("^특수기능:([^/]*)", dn):
        dn = dn.replace('특수기능:', '')
        ns = '특수기능:'
    if re.search("^토론:([^/]*)", dn):
        dn = dn.replace('토론:', '')
        ns = '토론:'
    if re.search("^투표:([^/]*)", dn):
        dn = dn.replace('투표:', '')
        ns = '투표:'
    if re.search("^휴지통:([^/]*)", dn):
        dn = dn.replace('휴지통:', '')
        ns = '휴지통:'
    if re.search("^분류:([^/]*)", dn):
        dn = dn.replace('분류:', '')
        ns = '분류:'
    
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
        nsdn = dn.replace(ns + ':', '')
    )), response_data