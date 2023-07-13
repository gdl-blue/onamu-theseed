from .tool.func import *

def ipacl(conn):
    curs = conn.cursor()
    name = None
    if name and ip_or_user(name) == 0:
        curs.execute("select acl from user where id = ?", [name])
        user = curs.fetchall()
        if not user:
            return re_error('/error/2')

        if user and user[0][0] != 'user':
            if admin_check() != 1:
                return re_error('/error/4')

    #if ban_check(ip = ip_check(), tool = 'login') == 1:
        #return re_error('/ban')
    #--------------------------------------
    if getperm('ipa') != 1:
        return re_error('/error/3')

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0
    cidrSearchQ = re.sub('[?]', '_', re.sub('[*]', '%', flask.request.args.get('from', '')))
    if flask.request.args.get('from', None):
        curs.execute("select ip, al, start, end, log from ipacl where ip like ? || '%' order by ip asc limit ?, '50'", [cidrSearchQ, str(sql_num)])
    else:
        curs.execute("select ip, al, start, end, log from ipacl order by ip asc limit ?, '50'", [str(sql_num)])
    data_list = curs.fetchall()


    data = '''
    	<form method="post" class="settings-section">
    		<div class="form-group">
    			<label class="control-label">IP 주소 (CIDR<sup><a href="https://ko.wikipedia.org/wiki/%EC%82%AC%EC%9D%B4%EB%8D%94_(%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9)" target="_blank">[?]</a></sup>) :</label>
    			<div>
    				<input type="text" class="form-control" id="ipInput" name="ip" value="''' + flask.request.args.get('cidr', '') + '''">
    			</div>
    		</div>

    		<div class="form-group">
    			<label class="control-label">메모 :</label>
    			<div>
    				<input type="text" class="form-control" id="noteInput" name="note" value="''' + flask.request.args.get('note', '') + '''">
    			</div>
    		</div>

    		<div class="form-group">
    			<label class="control-label">차단 기간 :</label>
    			<select class="form-control" name="expire">
    				<option value="0" selected="">영구</option>
    				<option value="300">5분</option>
    				<option value="600">10분</option>
    				<option value="1800">30분</option>
    				<option value="3600">1시간</option>
    				<option value="7200">2시간</option>
    				<option value="86400">하루</option>
    				<option value="259200">3일</option>
    				<option value="432000">5일</option>
    				<option value="604800">7일</option>
    				<option value="1209600">2주</option>
    				<option value="1814400">3주</option>
    				<option value="2419200">4주</option>
    				<option value="4838400">2개월</option>
    				<option value="7257600">3개월</option>
    				<option value="14515200">6개월</option>
    				<option value="29030400">1년</option>
    			</select>
    		</div>

    		<div class="form-group">
    			<label class="control-label">로그인 허용 :</label>
    			<div class="checkbox">
    				<label>
    					<input type="checkbox" id="allowLoginInput" name="allow_login">&nbsp;&nbsp;Yes
    				</label>
    			</div>
    		</div>

    		<div class="btns" style="margin-bottom: 20px;">
    			<button type="submit" class="btn btn-primary" style="width: 90px;">추가</button>
    		</div>
    	</form>
    	<div class="line-break" style="margin: 20px 0;"></div>
    	''' + next_fix('/admin/ipacl?num=', num, data_list) + '''
    	<form class="form-inline pull-right" id="searchForm" method=get>
    		<div class="input-group">
    			<input type="text" class="form-control" id="searchQuery" name="from" placeholder="CIDR" value="''' + flask.request.args.get('from', '') + '''">
    			<span class="input-group-btn">
    				<button type=submit class="btn btn-primary">Go</button>
    			</span>
    		</div>
    	</form>
    		<div class="table-wrap">
        		<table class="table" style="margin-top: 7px;">
        			<colgroup>
        				<col style="width: 150px;">
        				<col>
        				<col style="width: 200px">
        				<col style="width: 160px">
        				<col style="width: 60px">
        				<col style="width: 60px;">
        			</colgroup>
        			<tbody>
        				<tr style="vertical-align: bottom; border-bottom: 2px solid #eceeef;">
        					<th>IP</th>
        					<th>메모</th>
        					<th>차단일</th>
        					<th>만료일</th>
        					<th style="text-align: center;">AL</th>
        					<th style="text-align: center;">작업</th>
        				</tr>'''

    for ia in data_list:
        end = generateTime(ia[3])
        if ia[3] == '' or ia[3] == '0':
            end = '영구'
        data += '''
        				<tr>
        					<td>
        						''' + ia[0] + '''
        					</td>
        					<td>
        						''' + ia[4] + '''
        					</td>
        					<td>
        						''' + generateTime(ia[2]) + '''
        					</td>
        					<td>

        						''' + end + '''

        					</td>
        					<td class="text-center">
        						''' + ia[1] + '''
        					</td>
        					<td class="text-center">
        						<form method=post onsubmit="return confirm('정말로?');" action="/admin/ipacl/remove">
        						    <input type=hidden name=ip value="''' + ia[0] + '''">
        							<input type=submit class="btn btn-sm btn-danger" value="삭제">
        						</form>
        					</td>
        				</tr>'''
    data += '''
    			</tbody>
    		</table>
    	</div>
    	<div class="text-right pull-right">
    		AL = Allow Login(로그인 허용)
    	</div>
        '''


    if flask.request.method == 'POST':
        name = name if name else flask.request.form.get('name', 'test')

        if getperm('ipa') != 1:
            return re_error('/error/3')


        #ban_insert 참고함.
        end = int(number_check(getForm('expire', '')))

        time = datetime.datetime.now()
        plus = datetime.timedelta(seconds = end)
        r_time = (time + plus).strftime("%Y-%m-%d %H:%M:%S")
        if getForm('expire', '') == '0':
            r_time = '0'

        if getForm('allow_login', 0) != 0:
            al = 'Y'
        else:
            al = 'N'

        actionIP = getForm('ip', '')
        if not(re.search('[/]\d', actionIP)):
            actionIP += '/32'

        if stringInFormat("^\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}[/]\d{1,2}$", actionIP) != 1:
            return easy_minify(flask.render_template(skin_check(),
                imp = ['IPACL', wiki_set(), custom(), other2([0, 0])],
                data = alertBalloon('IP 주소가 틀립니다.') + data,
                menu = 0,
                err = 1
            ))

        try:
            if int(re.sub("^\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}[/]", "", actionIP)) < 8:
                return easy_minify(flask.render_template(skin_check(),
                    imp = ['IPACL', wiki_set(), custom(), other2([0, 0])],
                    data = alertBalloon('/8 대역부터 가능합니다.') + data,
                    menu = 0,
                    err = 1
                ))
        except:
            pass

        curs.execute("select ip from ipacl where ip = ?", [actionIP])
        if curs.fetchall():
            return easy_minify(flask.render_template(skin_check(),
                imp = ['IPACL', wiki_set(), custom(), other2([0, 0])],
                data = alertBalloon('ipacl_already_exists') + data,
                menu = 0,
                err = 1
            ))

        curs.execute("insert into ipacl (ip, al, start, end, log) values (?, ?, ?, ?, ?)", [actionIP, al, get_time(), r_time, getForm('note', '')])
        curs.execute("insert into rb (block, end, today, blocker, why, band, ipacl) values (?, ?, ?, ?, ?, '', '1')", [actionIP, getForm('expire', ''), get_time(), ip_check(), getForm('note', '')])
        conn.commit()

        return redirect('/admin/ipacl')
    else:
        return easy_minify(flask.render_template(skin_check(),
            imp = ['IPACL', wiki_set(), custom(), other2([0, 0])],
            data = data,
            menu = 0
        ))

def ipaclDelete(conn):
    curs = conn.cursor()
    if getperm('ipa') != 1:
        return re_error('/error/3')
    curs.execute("delete from ipacl where ip = ?", [getForm('ip', '')])
    curs.execute("insert into rb (block, end, today, blocker, why, band, ipacl) values (?, 'release', ?, ?, '', '', '1')", [getForm('ip', ''), get_time(), ip_check()])

    conn.commit()

    return redirect('/admin/ipacl')