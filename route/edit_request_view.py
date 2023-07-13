from .tool.func import *

def eq_2(conn, num):
    curs = conn.cursor()
    
    name = ''
    curs.execute("select name from erq where num = ?", [num])
    naamam = curs.fetchall()
    if naamam:
        name = naamam[0][0]
    r = ''
    curs.execute("select user from erq where num = ?", [num])
    ifdfpipp = curs.fetchall()
    if ifdfpipp:
        r = ifdfpipp[0][0]
    state = ''
    curs.execute("select state from erq where num = ?", [num])
    statestate = curs.fetchall()
    if statestate:
        state = statestate[0][0]
    else:
        return re_error('/error/4000')
    t = ''
    curs.execute("select time from erq where num = ?", [num])
    tt = curs.fetchall()
    if tt:
        t = tt[0][0]
    s = ''
    curs.execute("select send from erq where num = ?", [num])
    ss = curs.fetchall()
    if ss:
        s = ss[0][0]
    d = ''
    curs.execute("select data from erq where num = ?", [num])
    dd = curs.fetchall()
    if dd:
        d = dd[0][0]
    ap = ''
    curs.execute("select ap from erq where num = ?", [num])
    app = curs.fetchall()
    if app:
        ap = app[0][0]
    p = ''
    curs.execute("select pan from erq where num = ?", [num])
    pp = curs.fetchall()
    if pp:
        p = pp[0][0]
    w = ''
    curs.execute("select why from erq where num = ?", [num])
    ww = curs.fetchall()
    if ww:
        w = ww[0][0]
        
    if flask.request.method == 'POST':
        rea = flask.request.form.get('close_reason', '')
        if not(r == ip_check()) and not(admin_check(1) == 1):
            return re_error('/error/3')
    
        curs.execute("update erq set state = ? where num = ?", ['close', str(num)])
        curs.execute("update erq set closer = ? where num = ?", [ip_check(), str(num)])
        curs.execute("update erq set y = ? where num = ?", [get_time(), str(num)])
        curs.execute("update erq set why = ? where num = ?", [rea, str(num)])
        #flask.request.form.get('otent', '')
        
        return redirect('/edit_request/' + str(num))
    else:   
        result = ''
        curs.execute("select data from history where id = ? and title = ?", [str(int(str(p)) - 1), name])
        first_raw_data = curs.fetchall()
        if first_raw_data:
            second_raw_data = [[d]]
            first_data = html.escape(first_raw_data[0][0])            
            second_data = html.escape(second_raw_data[0][0])

            if first_raw_data == second_raw_data:
                result = '-'
            else:            
                diff_data = difflib.SequenceMatcher(None, first_data, second_data)
                result = re.sub('\r', '', diff(diff_data))
        
        dis = ''
        act = '이 편집 요청을 문서에 적용합니다.'
        if acl_check(name) == 1:
            dis = ' disabled'
            act = '이 문서를 편집할 수 있는 권한이 없습니다.'
        cds = ''
        cdt = '이 편집 요청을 닫습니다.'
        spo = '<span data-toggle="modal" data-target="#edit-request-close-modal">'
        spc = '</span>'
        if not(r == ip_check()) and not(admin_check(1) == 1):
            cds = ' disabled'
            cdt = '편집 요청을 닫기 위해서는 요청자 본인이거나 권한이 있어야 합니다.'
            spo = ''
            spc = ''
        crd = '''<div class="card">
                        <div class="card-block">
                        <h4 class="card-title" style="border:none">이 편집 요청을...</h4>
                        <p class="card-text">''' + t + '''에 마지막으로 수정됨</p>
                        <form id="edit-request-accept-form" style="display: inline;">

                        <input type="button" class="btn btn-lg btn-success''' + dis + '''" value="Accept" data-toggle="tooltip" data-placement="top" title="''' + act + '''" style="width:auto" onclick="location.href = \'/edit_request_accept/''' + str(num) + '''\';"''' + dis + '''>
                        </form>
                        ''' + spo + '''<input type="button" class="btn btn-lg''' + cds + '''" data-toggle="tooltip" data-placement="top" title="''' + cdt + '''" value="Close" style="width:auto;background:#efefef"''' + cds + '''>''' + spc + '''
                        <input type="button" class="btn btn-info btn-lg disabled" data-toggle="tooltip" data-placement="top" title="지원되지 않습니다." style="cursor: not-allowed;width:auto" value="Edit">
                        </div>
                        </div>'''
                        
        dtdt = '''<br><pre style="word-wrap: break-word">''' + result + '''</pre>'''
            
        if state == 'close':
            ct = ''
            cr = ''
            curs.execute("select y from erq where num = ?", [num])
            ctct = curs.fetchall()
            curs.execute("select closer from erq where num = ?", [num])
            crcr = curs.fetchall()
            if ctct and crcr:
                ct = ctct[0][0]
                cr = crcr[0][0]
                crd = '''<div class="card">
                            <div class="card-block">
                            <h4 class="card-title" style="border:none">편집 요청이 닫혔습니다.</h4>
                            
                            <p class="card-text">''' + ct + '''에 ''' + ip_pas(cr) + '''가 편집 요청을 닫았습니다.</p>'''
                if not(w == ''):
                    crd += '''<p class="card-text">사유 : ''' + w + '''</p>'''
                    
                crd += '''</div>
                            </div>'''
        elif state == 'accept':
            dtdt = ''
            ct = ''
            cr = ''
            curs.execute("select y from erq where num = ?", [num])
            ctct = curs.fetchall()
            curs.execute("select closer from erq where num = ?", [num])
            crcr = curs.fetchall()
            if ctct and crcr:
                ct = ctct[0][0]
                cr = crcr[0][0]
                crd = '''<div class="card">
                            <div class="card-block">
                            <h4 class="card-title" style="border:none">편집 요청이 승인되었습니다.</h4>
                            
                            <p class="card-text">''' + ct + '''에 ''' + ip_pas(cr) + '''가 r''' + str(ap) + '''으로 승인함.</p>
                            </div>
                            </div>'''

        ip = ip_check()
        
       
        
        
        #if acl_check(name) == 1:
         #   return re_error('/ban')
         
        
                
        if 3 == 4:
            return re_error('/error/666')
        else:            
            return easy_minify(flask.render_template(skin_check(), 
                imp = [name, wiki_set(), custom(), other2([' (' + load_lang('edit') + ' 요청 ' + str(num) + ')', 0])],
                data = '''
                        <div class="wiki-article content" style="overflow-x:auto">
                        <h3 style="border:0">
                        ''' + ip_pas(r) + '''가 ''' + t + '''에 요청
                        </h3>
                        <hr>
                        <div class="form-group">
                        <label class="control-label">기준 판</label>
                        r''' + str(int(str(p)) - 1) + '''
                        </div>
                        <div class="form-group">
                        <label class="control-label">편집 요약</label>
                        ''' + s + '''
                        </div>
                        <div id="edit-request-close-modal" class="modal fade" role="dialog" style="display: none;" aria-hidden="true">
                        <div class="modal-dialog">
                        <form id="edit-request-close-form" method="post">
                        <div class="modal-content">
                        <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal">×</button>
                        <h4 class="modal-title" style="border:none">편집 요청 닫기</h4>
                        </div>
                        <div class="modal-body">
                        <p>사유:</p>
                        <input type="text" name="close_reason">
                        </div>
                        <div class="modal-footer">
                        <input type="submit" class="btn btn-primary" value="닫기" style="width:auto">
                        <button type="button" class="btn btn-default" data-dismiss="modal" style="background:#efefef">취소</button>
                        </div>
                        </div>
                        </form>
                        </div>
                        </div>
                        ''' + crd + dtdt + '''
                        </div>
                ''',
                menu = [['w/' + url_pas(name), load_lang('return')], ['delete/' + url_pas(name), load_lang('delete')], ['move/' + url_pas(name), load_lang('move')]],
                st = 0,
                err = 0
            ))
        
def eqc_2(conn, num):
#if acl_check(name) == 1:
    curs = conn.cursor()
    ip = ip_check()
    admin = admin_check(1)
    name = ''
    curs.execute("select name from erq where num = ?", [num])
    naamam = curs.fetchall()
    if naamam:
        name = naamam[0][0]
    r = ''
    curs.execute("select user from erq where num = ?", [num])
    ifdfpipp = curs.fetchall()
    if ifdfpipp:
        r = ifdfpipp[0][0]
    state = ''
    curs.execute("select state from erq where num = ?", [num])
    statestate = curs.fetchall()
    if statestate:
        state = statestate[0][0]
    t = ''
    curs.execute("select time from erq where num = ?", [num])
    tt = curs.fetchall()
    if tt:
        t = tt[0][0]
    s = ''
    curs.execute("select send from erq where num = ?", [num])
    ss = curs.fetchall()
    if ss:
        s = ss[0][0]
    d = ''
    curs.execute("select data from erq where num = ?", [num])
    dd = curs.fetchall()
    if dd:
        d = dd[0][0]
    
    if not(r == ip_check()) and not(admin == 1):
        return re_error('/error/3')
    
    curs.execute("update erq set state = ? where num = ?", ['close', str(num)])
    curs.execute("update erq set closer = ? where num = ?", [ip, str(num)])
    curs.execute("update erq set y = ? where num = ?", [get_time(), str(num)])
    #flask.request.form.get('otent', '')
    
    return redirect('/edit_request/' + str(num))
    
def eqa_2(conn, num):
#if acl_check(name) == 1:
    curs = conn.cursor()
    ip = ip_check()
    admin = admin_check(1)
    name = ''
    curs.execute("select name from erq where num = ?", [num])
    naamam = curs.fetchall()
    if naamam:
        name = naamam[0][0]
    r = ''
    curs.execute("select user from erq where num = ?", [num])
    ifdfpipp = curs.fetchall()
    if ifdfpipp:
        r = ifdfpipp[0][0]
    state = ''
    curs.execute("select state from erq where num = ?", [num])
    statestate = curs.fetchall()
    if statestate:
        state = statestate[0][0]
    t = ''
    curs.execute("select time from erq where num = ?", [num])
    tt = curs.fetchall()
    if tt:
        t = tt[0][0]
    s = ''
    curs.execute("select send from erq where num = ?", [num])
    ss = curs.fetchall()
    if ss:
        s = ss[0][0]
    d = ''
    curs.execute("select data from erq where num = ?", [num])
    dd = curs.fetchall()
    if dd:
        d = dd[0][0]
    l = ''
    curs.execute("select leng from erq where num = ?", [num])
    ll = curs.fetchall()
    if ll:
        l = ll[0][0]
        
    if int(l) > 0:
        l = '+' + str(int(l))
        
    if int(l) == 0:
        l = '0'
        
    if int(l) < 0:
        l = str(int(l))
    
    if acl_check(name) == 1:
        return re_error('/error/3')
        
    curs.execute("select id from history where title = ? order by id + 0 desc limit 1", [name])
    id_data = curs.fetchall()
    
    curs.execute("update erq set state = ? where num = ?", ['accept', str(num)])
    curs.execute("update erq set closer = ? where num = ?", [ip, str(num)])
    curs.execute("update erq set y = ? where num = ?", [get_time(), str(num)])
    curs.execute("update data set data = ? where title = ?", [d, name])
    curs.execute("update data set date = ? where title = ?", [get_time(), name])
    curs.execute("update erq set ap = ? where num = ?", [str(int(id_data[0][0]) + 1) if id_data else '1', str(num)])
    
    
    
    curs.execute("insert into history (id, title, data, date, ip, send, leng, hide, i, q, qn) values (?, ?, ?, ?, ?, ?, ?, '', ?, ?, ?)", [
        str(int(id_data[0][0]) + 1) if id_data else '1',
        name,
        d,
        get_time(),
        r,
        s,
        l,
        '',
        'O',
        num
    ])
    
    return redirect('/edit_request/' + str(num))
    