from .tool.func import *

def threadInfo(conn, tnum):
    curs = conn.cursor()

    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')

    curs.execute("select sub from rd where tnum = ? and removed = '1'", [tnum])
    if curs.fetchall() and admin_check() != 1:
        return re_error('/error/7000')

    if getacl(name, 'read') != 1:
        return re_error('/error/3')

    pageTitle = html.escape(sub) + " " + loadLang("등록 정보", "Properties")

    curs.execute("select ip, date, tnumber from topic where tnum = ? and id = '1'", [tnum])
    thread = curs.fetchall()

    curs.execute("select stop, pause, agree from rd where tnum = ?", [tnum])
    threadInfo = curs.fetchall()

    trdInfo = loadLang('진행 중', "Ongoing")

    if threadInfo[0][0] == 'O':
        trdInfo = loadLang('완료', "Done")
    elif threadInfo[0][1] == 'O':
        trdInfo = loadLang('동결', "Paused")
    elif threadInfo[0][2] == 'O':
        trdInfo = loadLang('합의됨', "Agreed")

    content = '''
        <ul class=wiki-list>
            <li style="margin-bottom: 30px;">''' + loadLang("상태", "Current Status") + ''': ''' + trdInfo + '''</li>
            <li>''' + loadLang("발제자", "Starter") + ''': ''' + thread[0][0] + '''</li>
            <li style="margin-bottom: 30px;">''' + loadLang("발제 날짜", "Start Date") + ''': ''' + generateTime(thread[0][1], loadLang("Y년 m월 d일", "Y-m-d")) + '''</li>

            <li>''' + loadLang("토론 번호", "Thread Number") + ''': ''' + thread[0][2] + '''</li>
            <li>''' + loadLang("토론 식별자", "Thread ID") + ''': ''' + tnum + '''</li>
        </ul>

        <div class=btns>
            <!-- ".."이 원래 상위디렉토리인데 안 되네 도스 써본 입장에서 리눅스나 HTML 개인적으로 좀 익숙하지 않은 부분이 있음 -->
            <a href=/thread/''' + tnum + ''' style="width: 100px;" class="btn btn-primary">''' + loadLang("확인", "OK") + '''</a>
        </div>
    '''

    return easy_minify(flask.render_template(skin_check(),
        imp = [pageTitle, wiki_set(), custom(), other2([0, 0])],
        data = content,
        menu = [['thread/' + sub, loadLang('토론으로', 'Back')]]
    ))

def topic_2(conn, tnum):
    curs = conn.cursor()
    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')

    curs.execute("select sub from rd where tnum = ? and removed = '1'", [tnum])
    if curs.fetchall() and admin_check() != 1:
        return re_error('/error/7000')

    tit = name + ' (토론) - ' + sub + ' - ' + wiki_set()[0]

    #구버전 브라우져는 Non-JS 페이지로 돌리기
    ua = flask.request.headers.get('User-Agent')
    nojs = flask.request.args.get('nojs', None)
    if re.search('[;] MSIE \d{1,1}[.]\d{1,5};', ua) and not(nojs): # MS IE 1.0부터 9.0까지 인식
        return redirect('/thread/' + tnum + '?nojs=1')

    if re.search('^사용자:', name):
        ns = '사용자'
    elif re.search('^분류:', name):
        ns = '분류'
    elif re.search('^틀:', name):
        ns = '틀'
    elif re.search('^휴지통:', name):
        ns = '휴지통'
    elif re.search('^파일:', name):
        ns = '파일'
    elif re.search('^연습장:', name):
        ns = '연습장'
    elif re.search('^특수기능:', name):
        ns = '특수기능'
    elif re.search('^토론:', name):
        ns = '토론'
    elif re.search('^' + wiki_set()[0] + ':', name):
        ns = wiki_set()[0]
    else:
        ns = '문서'

    ban = topic_check(name, sub)
    admin = admin_check(3)

    if getacl(name, 'read') == 0:
        return noread(conn, name)


    curs.execute("select id from topic where title = ? and sub = ? limit 1", [name, sub])
    topic_exist = curs.fetchall()
    if not topic_exist and len(sub) > 256:
        return re_error('/error/11')

    if flask.request.method == 'POST':
        if getForm('pcm', None) != 't':
            return redirect('/thread/' + tnum)
        perm = getacl(name, 'write_thread_comment')
        if perm == 0:
            return re_error('/error/3')

        curs.execute("select agree from rd where tnum = ? and agree = 'O'", [tnum])
        if curs.fetchall():
            return re_error('/error/3')

        if len(getForm('content', '')) < 1:
            return showError('내용의 값은 필수입니다.')

        curs.execute("select title from rd where tnum = ?", [tnum])
        if not(curs.fetchall()):
            return re_error('/error/7000')

        if captcha_post(flask.request.form.get('g-recaptcha-response', '')) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)

        ip = ip_check()
        today = get_time()

        curs.execute("select stop from rd where tnum = ?", [tnum])
        bbc = curs.fetchall()
        if bbc[0][0] == 'O':
            return re_error('/error/3')
        curs.execute("select pause from rd where tnum = ?", [tnum])
        bbcc = curs.fetchall()
        if bbcc[0][0] == 'O':
            return re_error('/error/3')

        curs.execute("select id from topic where tnum = ? order by id + 0 desc limit 1", [tnum])
        old_num = curs.fetchall()
        if old_num:
            num = int(old_num[0][0]) + 1
        else:
            num = 1

        match = re.search('^사용자:([^/]+)', name)
        if match:
            y_check = 0
            if ip_or_user(match.groups()[0]) == 1:
                curs.execute("select ip from history where ip = ? limit 1", [match.groups()[0]])
                u_data = curs.fetchall()
                if u_data:
                    y_check = 1
                else:
                    curs.execute("select ip from topic where ip = ? limit 1", [match.groups()[0]])
                    u_data = curs.fetchall()
                    if u_data:
                        y_check = 1
            else:
                curs.execute("select id from user where id = ?", [match.groups()[0]])
                u_data = curs.fetchall()
                if u_data:
                    y_check = 1

            if y_check == 1:
                curs.execute('insert into alarm (name, data, date) values (?, ?, ?)', [
                    match.groups()[0],
                    ip + ' - <a href="/topic/' + url_pas(name) + '/sub/' + url_pas(sub) + '">' + load_lang('user_discussion', 1) + '</a>',
                    today
                ])

        cate_re = re.compile('\[\[((?:분류|category):(?:(?:(?!\]\]).)*))\]\]', re.I)
        data = cate_re.sub('[br]', flask.request.form.get('content', 'Test'))

        for rd_data in re.findall("(?:#([0-9]+))", data):
            curs.execute("select ip from topic where title = ? and sub = ? and id = ?", [name, sub, rd_data])
            ip_data = curs.fetchall()
            if ip_data and ip_or_user(ip_data[0][0]) == 0:
                curs.execute('insert into alarm (name, data, date) values (?, ?, ?)', [ip_data[0][0], ip + ' - <a href="/topic/' + url_pas(name) + '/sub/' + url_pas(sub) + '#' + str(num) + '">' + load_lang('discussion', 1) + '</a>', today])

        data = re.sub("(?P<in>#(?:[0-9]+))", '[[\g<in>]]', data)

        data = savemark(data)

        rd_plus(name, sub, today)

        if admin_check(5) == 1 or getperm('tribune') == 1 or getperm('arbiter') == 1:
            adm = 1
        else:
            adm = 0

        if 'state' in flask.session and flask.session['state'] == 1:
            ism = 'author'
        else:
            ism = 'ip'
        curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm, tnum, ismember) values (?, ?, ?, ?, ?, ?, '', '', ?, ?, ?)", [str(num), name, sub, data, today, ip, adm, tnum, ism])
        conn.commit()

        return flask.jsonify({})

        return redirect('/thread/' + url_pas(tnum) + '#reload')
    else:
        curs.execute("select title, sub from topic where tnum = ?", [tnum])
        fet = curs.fetchall()
        if fet:
            name = fet[0][0]
            sub = fet[0][1]
        else:
            return re_error('/error/7000')
        curs.execute("select title from rd where title = ? and sub = ?", [name, sub])
        if not(curs.fetchall()):
            return re_error('/error/7000')
        curs.execute("select title from rd where title = ? and sub = ? and stop = 'O'", [name, sub])
        close_data = curs.fetchall()

        curs.execute("select title from rd where title = ? and sub = ? and stop = 'S'", [name, sub])
        stop_data = curs.fetchall()

        display = ''
        all_data = ''
        data = ''
        number = 1
        all_data += '<div id=res-container>'

        if (close_data or stop_data) and admin != 1:
            display = 'display: none;'

        curs.execute("select data, id, date, ip, block, top, adm from topic where tnum = ? order by id + 0 asc", [tnum])
        topic = curs.fetchall()

        curs.execute("select data, id, date, ip from topic where tnum = ? and top = 'O' order by id + 0 asc", [tnum])
        ptd = curs.fetchall()
        for topic_data in ptd:
            who_plus = ''

            curs.execute("select who from re_admin where what = ? order by time desc limit 1", ['notice (' + name + ' - ' + sub + '#' + topic_data[1] + ')'])
            topic_data_top = curs.fetchall()
            if topic_data_top:
                who_plus += ' <sub>(' + topic_data_top[0][0] + '에 의해 고정됨)</sub>'

            all_data += '''
                <div class="res-wrapper" data-id="P''' + topic_data[1] + '''">
                    <div class="res res-type-normal">
                        <div class="r-head pinned">
                            <a href="#''' + topic_data[1] + '''">
                                #''' + topic_data[1] + '''
                            </a> ''' + ip_pas_t(topic_data[3]) + who_plus + ''' <span style="float: right;">''' + generateTime(topic_data[2]) + '''</span>
                        </div>
                        <div class="r-body">
                            ''' + render_set(data = topic_data[0]) + '''
                        </div>
                    '''
            if getperm('htc') == 1:
                all_data += '<div class="combo admin-menu"><a class="btn btn-warning btn-sm" href="/admin/thread/' + tnum + '/' + topic_data[1] + '/unpin">[ADMIN] 고정 해제</a></div>'
            all_data += '</div></div>'


        nn = 1
        #if ptd:
            #all_data += '<hr class=\"main_hr\">'
        #all_data += '<div id="main_topic">'

        if nojs != '1':
            for topic_data in topic:
                all_data += '''
                <div class="res-wrapper res-loading" data-id="''' + str(number) + '''" data-locked="false"><div class="res res-type-normal"><div class="r-head"><span class="num"><a id="''' + str(number) + '''">#''' + str(number) + '''</a>&nbsp;</span></div><div class="r-body"></div></div></div>
                '''

                number += 1
        else:
            all_data += discussFetch(tnum, '1')

        try:
            nn = str(number)
        except:
            nn = '1'
        #all_data += '</div>'

        lnkReload = ''
        if nojs == '1':
            lnkReload = '<div class="alert alert-warning"><strong>[알림!]</strong> 토론 자동 갱신 기능이 비활성화되어있거나 브라우저가 지원하지 않습니다. 새로운 댓글을 보려면 <a href="javascript:history.go(0);">토론을 다시 불러오십시오</a>.</div>'
        if nojs != '1':
            data += '''
            </div><input type="hidden" id="isa" value="''' + str(admin) + '''">

            <script>/* topic_main_load("''' + str(tnum) + '''"); */</script>
            <SCRIPT>
            $(function() {
                discussPollStart("''' + tnum + '''");
            });
        	</SCRIPT>
            <SCRIPT>
            /*
               https://stackoverflow.com/questions/1642447/how-to-change-the-content-of-a-textarea-with-javascript
               https://stackoverflow.com/questions/3527041/prevent-any-form-of-page-refresh-using-jquery-javascript
            */

            /*
            $(function () {
                $('#postComment').on('submit',function (e) {
                      $.ajax({
                        type: 'post',
                        url: \'/thread/''' + url_pas(tnum) + '''\',
                        data: $('#postComment').serialize(),
                        error: function() {
                         alert('문제가 발생했습니다!');
                         $('#postCommentButton').removeAttr('disabled');
                         $('#conten').removeAttr('readonly');
                         $('#conten').attr('style', 'height: 100px;');
                        },
                        success: function () {
                         document.getElementById('conten').value = '';
                         var myTextArea = document.getElementById('conten');
                         myTextArea.innerHTML = '';
                         myTextArea.innerText = '';
                         $('#conten').removeAttr('readonly');
                         $('#conten').attr('style', 'height: 100px;');
                        }
                      });
                  e.preventDefault();
                });
                $("#postCommentButton").click(function() {
                    $('#conten').attr('readonly', true);
                    $('#conten').attr('style', 'background: #eceeef; height: 100px;');
                });
            });
            */

            </SCRIPT>
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

            <br>'''
        data += '''<div id="reload">''' + lnkReload + '''</div><h2 style="cursor: pointer; border: none;" class="wiki-heading">댓글 달기</h2><div id="dcf" style="display: block; ">'''

        curs.execute("select stop from rd where title = ? and sub = ?", [name, sub])
        ban = 0
        bbc = curs.fetchall()
        if bbc:
            if bbc[0][0] == 'O':
                ban = 1
            else:
                ban = 0

        curs.execute("select pause from rd where title = ? and sub = ?", [name, sub])
        banp = 0
        bbcc = curs.fetchall()
        if bbcc:
            if bbcc[0][0] == 'O':
                banp = 1
            else:
                banp = 0

        #참고용
        seedhtml = '''
            <form method="post" id="thread-status-form">
        		[ADMIN] 쓰레드 상태 변경
        		<select name="status">
        		<option value="normal">normal</option>
        		<option value="pause">pause</option>

        		</select>
        		<button id="changeBtn" class="d_btn type_blue">변경</button>
        	</form>


        	<form method="post" id="thread-document-form">
        		[ADMIN] 쓰레드 이동
        		<input type="text" name="document" value="문서명">
        		<button id="changeBtn" class="d_btn type_blue">변경</button>
        	</form>


        	<form method="post" id="thread-topic-form">
        		[ADMIN] 쓰레드 주제 변경
        		<input type="text" name="topic" value="토론명">
        		<button id="changeBtn" class="d_btn type_blue">변경</button>
        	</form>
        '''
        agnj = ''
        if nojs != '1':
            data += '''
            <script>
            /* 출처: https://theseed.io/js/theseed.js */
            /*
            var topic = "''' + tnum + '''";
            $(function() {
                $('#thread-status-form').submit(function() {
        			var self = $(this);
        			var data = self.serialize();
        			self.find("BUTTON").attr("disabled", "disabled");
        			$.ajax({
        				type: "POST",
        				url: "/admin/thread/" + topic + "/status",
        				data: data,
        				dataType: 'json',
        				success: function(data) {
        					self.find("BUTTON").removeAttr("disabled");
        					location.reload();
        				},
        				error: function(data) {
        					alert((data && data.responseJSON && data.responseJSON.status) ? data.responseJSON.status :'문제가 발생했습니다!');
        					self.find("BUTTON").removeAttr("disabled");
        				}
        			});
        			return false;
        		});
        		$('#thread-document-form').submit(function() {
        			var self = $(this);
        			var data = self.serialize();
        			self.find("BUTTON").attr("disabled", "disabled");
        			$.ajax({
        				type: "POST",
        				url: "/admin/thread/" + topic + "/document",
        				data: data,
        				dataType: 'json',
        				success: function(data) {
        					self.find("BUTTON").removeAttr("disabled");
        				},
        				error: function(data) {
        					alert((data && data.responseJSON && data.responseJSON.status) ? data.responseJSON.status :'문제가 발생했습니다!');
        					self.find("BUTTON").removeAttr("disabled");
        				}
        			});
        			return false;
        		});
        		$('#thread-topic-form').submit(function() {
        			var self = $(this);
        			var data = self.serialize();
        			self.find("BUTTON").attr("disabled", "disabled");
        			$.ajax({
        				type: "POST",
        				url: "/admin/thread/" + topic + "/topic",
        				data: data,
        				dataType: 'json',
        				success: function(data) {
        					self.find("BUTTON").removeAttr("disabled");
        				},
        				error: function(data) {
        					alert((data && data.responseJSON && data.responseJSON.status) ? data.responseJSON.status :'문제가 발생했습니다!');
        					self.find("BUTTON").removeAttr("disabled");
        				}
        			});
        			return false;
        		});
        	});
        	*/
    		</script>
            '''
        else:
            agnj = '?nojs=1'
        agreed = 0
        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'uts'])
        if curs.fetchall():
            if ban == 1:
                ct = 'normal'
            else:
                ct = 'close'
            if banp == 1:
                ct2 = 'normal'
            else:
                ct2 = 'pause'
            curs.execute("select tnum from rd where tnum = ? and agree = 'O'", [tnum])
            if curs.fetchall():
                ct3 = 'normal'
                agreed = 1
            else:
                ct3 = 'agree'
            data += '''
                <form method="post" id="thread-status-form" action="/admin/thread/''' + tnum + '''/status''' + agnj + '''">
            		[ADMIN] 쓰레드 상태 변경
            		<select name="status">
                		<option value="''' + ct + '''">''' + ct + '''</option>
                		<option value="''' + ct2 + '''">''' + ct2 + '''</option>
                		<option value="''' + ct3 + '''">''' + ct3 + '''</option>
            		</select>
            		<button id="changeBtn" class="d_btn type_blue" type=submit>변경</button>
            	</form>
                '''

        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'utd'])
        if curs.fetchall():
            data += '''
                <form method="post" id="thread-document-form" action="/admin/thread/''' + tnum + '''/document''' + agnj + '''">
            		[ADMIN] 쓰레드 이동
            		<input type="text" name="document" value="''' + name + '''">
            		<button id="changeBtn" class="d_btn type_blue" type=submit>변경</button>
            	</form>
        	'''
        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'utt'])
        if curs.fetchall():
            data += '''
                <form method="post" id="thread-topic-form" action="/admin/thread/''' + tnum + '''/topic''' + agnj + '''">
            		[ADMIN] 쓰레드 주제 변경
            		<input type="text" name="topic" value="''' + sub + '''">
            		<button id="changeBtn" class="d_btn type_blue" type=submit>변경</button>
            	</form>
        	'''
        btncls = 'btns'
        if nojs == '1':
            btncls = ''
        if admin == 0 or admin == 1:
            if ban == 1:
                data += '''
                    <form>
                        <textarea class="form-control" style="height: 100px;background:#efefef;cursor:not-allowed" name="content" disabled readonly>닫힌 토론입니다.</textarea>
                        ''' + captcha_get() + (ip_warring() if display == '' else '') + '''
                        <div class="''' + btncls + '''"><button type="button" class="btn btn-primary" style="width:120px" disabled>''' + load_lang('send') + '''</button>
                    </div></form></div>
                '''
            elif banp == 1:
                data += '''
                    <form>
                        <textarea class="form-control" style="height: 100px;background:#efefef;cursor:not-allowed" name="content" disabled readonly>pause 상태입니다.</textarea>
                        ''' + captcha_get() + (ip_warring() if display == '' else '') + '''
                        <div class="''' + btncls + '''"><button type="button" class="btn btn-primary" style="width:120px" disabled>''' + load_lang('send') + '''</button>
                    </div></form></div>
                '''
            elif agreed == 1:
                data += '''
                    <form>
                        <textarea class="form-control" style="height: 100px;background:#efefef;cursor:not-allowed" name="content" disabled readonly>합의된 토론입니다.</textarea>
                        ''' + captcha_get() + (ip_warring() if display == '' else '') + '''
                        <div class="''' + btncls + '''"><button type="button" class="btn btn-primary" style="width:120px" disabled>''' + load_lang('send') + '''</button>
                    </div></form></div>
                '''
            else:
                data += '''
                    <form method=post id=new-thread-form>
                        <input type=hidden name=pcm value=t>
                        <textarea class="form-control" style="height: 100px;" name="content" id="conten"></textarea>
                        ''' + captcha_get() + (ip_warring() if display == '' else '') + '''
                        <div class="''' + btncls + '''"><button type="submit" class="btn btn-primary" id="postCommentButton" style="width:120px">''' + load_lang('send') + '''</button>
                    </div></form></div>
                '''
        delt = ''
        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'dt'])
        if curs.fetchall():
            delt = '''<span class="pull-right"><a class="btn btn-danger btn-sm" href="/admin/thread/''' + url_pas(tnum) + '''/delete" onclick="return confirm('삭제하시겠습니까?')">[ADMIN] 삭제</a></span>'''

        curs.execute("select sub from rd where tnum = ? and removed = '1'", [tnum])
        if curs.fetchall() and admin_check() == 1:
            delt = '''<span class="pull-right"><a class="btn btn-warning btn-sm" href="/admin/thread/''' + url_pas(tnum) + '''/restore" onclick="return confirm('이 토론을 삭제복구하시겠습니까?')">[ADMIN] 삭제복구</a></span>'''

        if admin_check() == 1:
            delt += '''<span class="pull-right"><a class="btn btn-danger btn-sm" href="/admin/thread/''' + url_pas(tnum) + '''/permanent_delete" onclick="if(confirm('삭제하시겠습니까?')) {return confirm('이 토론을 완전히 삭제하시겠습니까? 복구할 수 없습니다!');} else { return false; }">[ADMIN] 완전삭제</a></span>'''

        delt += '''<span style="float: right;"><a class="btn btn-info btn-sm" href="/thread/''' + url_pas(tnum) + '''/info">토론 정보</a></span>'''

        data += '''
        <SCRIPT>
        /* https://stackoverflow.com/questions/11254429/hiding-all-elements-with-the-same-class-name */

        function toggle(className, displayState){
            var elements = document.getElementsByClassName(className)

            for (var i = 0; i < elements.length; i++){
                elements[i].parentNode.parentNode.style.display = displayState;
            }
        }

        $('#noDisplayHideAuthor').click(function(){
            if(document.getElementById('noDisplayHideAuthor').checked)
                toggle('r-hidden-body', 'none');
            else
                toggle('r-hidden-body', 'block');
        });
        </SCRIPT>

        <SCRIPT>
            /* 출처: https://theseed.io/js/theseed.js */

        	var discussObserver = new IntersectionObserver(function (entries) {
        		discussLastObserveTime = Date.now();
        		for(var i = 0; i < entries.length; i++) {
        			entries[i].target.setAttribute('data-visible', entries[i].isIntersecting);
        		}
        	});

        	$("div.res-wrapper.res-loading").each(function () {
        		discussObserver.observe(this);
        	});
        </SCRIPT>
        '''

        warn = ''
        if name == wiki_set()[0] or name == wiki_set(2):
            warn = '''<div class="alert alert-success alert-dismissible" role=alert><strong>[경고!]</strong> 이 토론은 ''' + name + ''' 문서의 토론입니다. ''' + name + ''' 문서와 관련 없는 토론은 각 문서의 토론에서 진행해 주시기 바랍니다. ''' + name + ''' 문서와 관련 없는 토론은 삭제될 수 있습니다.</div><br>'''


        htchk = ' checked=checked'
        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'htc'])
        if curs.fetchall():
            htchk = ''
        fhcnd = '<form style="float: right; "><input type="checkbox" id="noDisplayHideAuthor" ' + htchk + '><label for="noDisplayHideAuthor" style="font-size: 1rem;">숨겨진 댓글 보이지 않기</label></form>'
        if nojs == '1':
            fhcnd = ''
        return easy_minify(flask.render_template(skin_check(),
            imp = [name, wiki_set(), custom(), other2([' (' + load_lang('discussion') + ') - ' + sub, 0])],
            data = warn + fhcnd + '<input type=hidden id=numLLR name=last_loaded_res value="' + str(number - 1) + '"> <h2 class=wiki-heading style="cursor: pointer; border: none;"><span onclick="var ddd = document.getElementById(\'tb\'); if(ddd.style.display == \'block\') ddd.style.display = \'none\'; else ddd.style.display = \'block\'; ">' + sub + '</span> ' + delt + '</h2>''' + '<div style="display:block" id="tb">' + all_data + data,
            menu = [['discuss/' + url_pas(name), load_lang('list')]],
            st = 3,
            smsub = ' (토론)',
            ns = ns
        ))

def topic_2_old(conn, tnum):
    curs = conn.cursor()
    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')

    tit = name + ' (토론) - ' + sub + ' - ' + wiki_set()[0]


    if re.search('^사용자:', name):
        ns = '사용자'
    elif re.search('^분류:', name):
        ns = '분류'
    elif re.search('^틀:', name):
        ns = '틀'
    elif re.search('^휴지통:', name):
        ns = '휴지통'
    elif re.search('^파일:', name):
        ns = '파일'
    elif re.search('^' + wiki_set()[0] + ':', name):
        ns = wiki_set()[0]
    else:
        ns = '문서'

    ban = topic_check(name, sub)
    admin = admin_check(3)

    if getacl(name, 'read') == 0:
        return noread(conn, name)


    curs.execute("select id from topic where title = ? and sub = ? limit 1", [name, sub])
    topic_exist = curs.fetchall()
    if not topic_exist and len(sub) > 256:
        return re_error('/error/11')

    if flask.request.method == 'POST':
        perm = getacl(name, 'write_thread_comment')
        if perm == 0:
            return re_error('/error/3')

        curs.execute("select title from rd where tnum = ?", [tnum])
        if not(curs.fetchall()):
            return re_error('/error/7000')

        if captcha_post(flask.request.form.get('g-recaptcha-response', '')) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)

        ip = ip_check()
        today = get_time()

        curs.execute("select stop from rd where tnum = ?", [tnum])
        bbc = curs.fetchall()
        if bbc[0][0] == 'O':
            return re_error('/error/3')
        curs.execute("select pause from rd where tnum = ?", [tnum])
        bbcc = curs.fetchall()
        if bbcc[0][0] == 'O':
            return re_error('/error/3')

        curs.execute("select id from topic where tnum = ? order by id + 0 desc limit 1", [tnum])
        old_num = curs.fetchall()
        if old_num:
            num = int(old_num[0][0]) + 1
        else:
            num = 1

        match = re.search('^사용자:([^/]+)', name)
        if match:
            y_check = 0
            if ip_or_user(match.groups()[0]) == 1:
                curs.execute("select ip from history where ip = ? limit 1", [match.groups()[0]])
                u_data = curs.fetchall()
                if u_data:
                    y_check = 1
                else:
                    curs.execute("select ip from topic where ip = ? limit 1", [match.groups()[0]])
                    u_data = curs.fetchall()
                    if u_data:
                        y_check = 1
            else:
                curs.execute("select id from user where id = ?", [match.groups()[0]])
                u_data = curs.fetchall()
                if u_data:
                    y_check = 1

            if y_check == 1:
                curs.execute('insert into alarm (name, data, date) values (?, ?, ?)', [
                    match.groups()[0],
                    ip + ' - <a href="/topic/' + url_pas(name) + '/sub/' + url_pas(sub) + '">' + load_lang('user_discussion', 1) + '</a>',
                    today
                ])

        cate_re = re.compile('\[\[((?:분류|category):(?:(?:(?!\]\]).)*))\]\]', re.I)
        data = cate_re.sub('[br]', flask.request.form.get('content', 'Test'))

        for rd_data in re.findall("(?:#([0-9]+))", data):
            curs.execute("select ip from topic where title = ? and sub = ? and id = ?", [name, sub, rd_data])
            ip_data = curs.fetchall()
            if ip_data and ip_or_user(ip_data[0][0]) == 0:
                curs.execute('insert into alarm (name, data, date) values (?, ?, ?)', [ip_data[0][0], ip + ' - <a href="/topic/' + url_pas(name) + '/sub/' + url_pas(sub) + '#' + str(num) + '">' + load_lang('discussion', 1) + '</a>', today])

        data = re.sub("(?P<in>#(?:[0-9]+))", '[[\g<in>]]', data)

        data = savemark(data)

        rd_plus(name, sub, today)

        adm = admin_check(5)

        curs.execute("insert into topic (id, title, sub, data, date, ip, block, top, adm, tnum) values (?, ?, ?, ?, ?, ?, '', '', ?, ?)", [str(num), name, sub, data, today, ip, adm, tnum])
        conn.commit()

        return redirect('/thread/' + url_pas(tnum) + '#reload')
    else:
        curs.execute("select title, sub from topic where tnum = ?", [tnum])
        fet = curs.fetchall()
        if fet:
            name = fet[0][0]
            sub = fet[0][1]
        else:
            return re_error('/error/7000')
        curs.execute("select title from rd where title = ? and sub = ?", [name, sub])
        if not(curs.fetchall()):
            return re_error('/error/7000')
        curs.execute("select title from rd where title = ? and sub = ? and stop = 'O'", [name, sub])
        close_data = curs.fetchall()

        curs.execute("select title from rd where title = ? and sub = ? and stop = 'S'", [name, sub])
        stop_data = curs.fetchall()

        display = ''
        all_data = ''
        data = ''
        number = 1

        if (close_data or stop_data) and admin != 1:
            display = 'display: none;'

        curs.execute("select data, id, date, ip, block, top, adm from topic where tnum = ? order by id + 0 asc", [tnum])
        topic = curs.fetchall()

        curs.execute("select data, id, date, ip from topic where title = ? and sub = ? and top = 'O' order by id + 0 asc", [name, sub])
        for topic_data in curs.fetchall():
            who_plus = ''

            curs.execute("select who from re_admin where what = ? order by time desc limit 1", ['notice (' + name + ' - ' + sub + '#' + topic_data[1] + ')'])
            topic_data_top = curs.fetchall()
            if topic_data_top:
                who_plus += ' <span style="margin-right: 5px;">@' + topic_data_top[0][0] + ' </span>'

            all_data += '''
                <div style="overflow-x: scroll;"><table id="toron">
                    <tbody>
                        <tr>
                            <td id="toron_color_red">
                                <a href="#''' + topic_data[1] + '''">
                                    #''' + topic_data[1] + '''
                                </a> ''' + ip_pas_t(topic_data[3]) + who_plus + ''' <span style="float: right;">''' + topic_data[2] + '''</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px 10px 15px;background:#e8e8e8;color:#4a4a4a; border:none; border-radius:0; box-sizing:inherit; display:block; box-sizing:inherit; box-sizing:inherit; font-size:1rem; font-weight:400;">''' + render_set(data = topic_data[0]) + '''</td>
                        </tr>
                    </tbody>
                </table></div><br>
                <hr class=\"main_hr\"><br>

            '''
        nn = 1
        for topic_data in topic:
            curs.execute("select block, ip, date from topic where title = ? and sub = ? and id = ?", [url_pas(name), url_pas(sub), str(number)])
            admdswiwdiataa = curs.fetchall()
            user_write = topic_data[0]
            user_write = render_set(data = user_write)
            ip = ip_pas_t(topic_data[3])
            curs.execute('select acl from user where id = ?', [topic_data[3]])
            user_acl = curs.fetchall()
            blablabla = 0



            if number == 1:
                start = topic_data[3]
            if topic_data[4] == 'O':
                blind_data = 'id="toron_color_grey"'
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'htc'])
                if not(curs.fetchall()):
                    curs.execute("select who from re_admin where what = ? order by time desc limit 1", ['blind (' + name + ' - ' + sub + '#' + str(number) + ')'])
                    who_blind = curs.fetchall()
                    if who_blind:
                        user_write = '[' + who_blind[0][0] + '에 의해 숨겨진 글입니다.]'
                        blablabla = 1
                    else:
                        user_write = '[숨겨진 글입니다.]'
                        blablabla = 1
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'htc'])
                if curs.fetchall():
                    curs.execute("select who from re_admin where what = ? order by time desc limit 1", ['blind (' + name + ' - ' + sub + '#' + str(number) + ')'])
                    who_blind = curs.fetchall()
                    if who_blind:
                        user_write = '[' + who_blind[0][0] + '에 의해 숨겨진 글입니다.]<br><div class="text-line-break" style="margin: 25px 0px 0px -10px; display:block"><a class="text" onclick="$(this).parent().parent().children(\'.hidden-content\').show(); $(this).parent().css(\'margin\', \'15px 0 15px -10px\'); $(this).hide(); return false;" style="display: block; color: #fff;">[ADMIN] Show hidden content</a><div class="line"></div></div><div class="hidden-content" style="display:none">' + user_write + '</div>'
                        blablabla = 1
                    else:
                        user_write = '[숨겨진 글입니다.]<br><br>' + user_write
                        blablabla = 1
            else:
                blind_data = ''

            if topic_data[6] == '1':
                ip = '<strong>' + ip
                ip += '</strong>'
                #ip += ' <a href="javascript:void(0);" title="' + load_lang('admin') + '">★</a>'

            if ban_check(topic_data[3]):
                ip += ' <sub>(차단됨)</sub>'

            curs.execute("select date from topic where title = ? and sub = ? and id = ?", [name, sub, str(number)])
            dt = curs.fetchall()




            #if admin == 1 or blind_data == '':
                #ip += '<a href="/topic/' + url_pas(name) + '/sub/' + url_pas(sub) + '/admin/' + str(number) + '"> [도구]</a>'





            oraoraorgaanna = 0

            if topic_data[5] == '1':
                oraoraorgaanna = 1
                if topic_data[3] == start:
                    color = '_green'
                else:
                    color = ''
            elif topic_data[3] == start:
                color = '_green'
            else:
                color = ''

            if user_write == '':
                user_write = '<br>'

            if dt:
                all_data += '''
                    <div class="res-wrapper" data-id="''' + str(number) + '''">'''
                if topic_data[5] == '1':
                    all_data +=  '<div class="res res-type-status">'
                else:
                    all_data +=  '<div class="res res-type-normal">'


                all_data += '''
                        <div class="r-head'''
                if topic_data[3] == start:
                    all_data += ' first-author'
                ddd = dt[0][0].split(' ')[0]
                ttt = dt[0][0].split(' ')[1]
                all_data += '''">
                            <span class="num"><a id="''' + str(number) + '">#' + str(number) + '</a>&nbsp;</span> ' + ip + '''<span style="margin-left: 25px;float:right"><time datetime="''' + ddd + 'T' + ttt + '''.000Z" data-format="Y-m-d H:i:s">''' + dt[0][0] + '''</time></span><div class="clearfix"></div>
                        </div>
                        <div class="r-body'''
                if topic_data[4] == 'O':
                    all_data += ' r-hidden-body'

                all_data += '''">'''

            if user_write == '스레드 상태를 <b>open</b>로 변경' or user_write == '스레드 상태를 <b>open</b>로 변경 ':
                user_write = '스레드 상태를 <b>normal</b>로 변경'
            all_data += user_write + '''</div></div>
                '''
            curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'htc'])
            if curs.fetchall():
                all_data += '''
                <div class="combo admin-menu">

				<a class="btn btn-danger btn-sm" href="/admin/thread/''' + url_pas(tnum) + '''/hide/''' + str(number) + '''">'''
                if blablabla == 1:
                    all_data += '''[ADMIN] 숨기기 해제'''
                else:
                    all_data += '''[ADMIN] 숨기기'''
                all_data += '''</a></div>


            '''
            #all_data += '''<br><br>'''

            number += 1

            all_data += '</div>'

        nn = str(number)


        data += '''
            </div><input type="hidden" id="isa" value="''' + str(admin) + '''">
            <div id="plus_topic"><input id="enu" type="hidden" value="''' + nn + '''"></div>
            <script>/* topic_plus_load("''' + str(tnum) + '''", ''' + nn + '''); */</script>
            <SCRIPT>
            /*
               https://stackoverflow.com/questions/1642447/how-to-change-the-content-of-a-textarea-with-javascript
               https://stackoverflow.com/questions/3527041/prevent-any-form-of-page-refresh-using-jquery-javascript
            */
            $(function () {
                $('#postComment').on('submit',function (e) {

                          $.ajax({
                            type: 'post',
                            url: \'/thread/''' + url_pas(tnum) + '''\',
                            data: $('#postComment').serialize(),
                            error: function() {
                             alert('문제가 발생했습니다!');
                            },
                            success: function () {
                             document.getElementById('conten').value = '';
                             var myTextArea = document.getElementById('conten');
                             myTextArea.innerHTML = '';
                             myTextArea.innerText = '';
                            }
                          });
                      e.preventDefault();
                    });
            });
            </SCRIPT>
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

            <br><div id="reload"></div><h2 style="cursor: pointer; border: none;" onclick="var dc = document.getElementById(\'dcf\'); if(dc.style.display == \'block\') dc.style.display = \'none\'; else dc.style.display = \'block\'; ">댓글 달기</h2><div id="dcf" style="display: block; ">'''

        curs.execute("select stop from rd where title = ? and sub = ?", [name, sub])
        ban = 0
        bbc = curs.fetchall()
        if bbc:
            if bbc[0][0] == 'O':
                ban = 1
            else:
                ban = 0

        curs.execute("select pause from rd where title = ? and sub = ?", [name, sub])
        banp = 0
        bbcc = curs.fetchall()
        if bbcc:
            if bbcc[0][0] == 'O':
                banp = 1
            else:
                banp = 0


        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'uts'])
        if curs.fetchall():
            if ban == 1:
                ct = 'normal'
            else:
                ct = 'close'
            if banp == 1:
                ct2 = 'normal'
            else:
                ct2 = 'pause'
            data += '''
                [ADMIN] 쓰레드 상태 변경 <select style="padding: 0;border-radius: 0;border-color: gray;" name="status" id="sttssu">
                    <option value="close">''' + ct + '''</option>
                    <option value="pause">''' + ct2 + '''</option>

                </select>  <button style="padding-top: 0;padding-bottom: 0;padding-left: 6px;padding-right: 6px;border-radius: 0;border-color: gray;background-color: #eee;" type="button" onclick="location.href = '/admin/thread/''' + url_pas(tnum) + '''/tool/' + getElementById('sttssu').value;">변경</button><br />
                '''

        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'utd'])
        if curs.fetchall():
            data += '''[ADMIN] 쓰레드 이동 <input style="width:160px;border-radius: 0;padding: 0;border-color: gray;" type="text" style="width:160px" id="mvth" value="''' + name + '''">  <button type="button" onclick="location.href = '/admin/thread/''' + url_pas(tnum) + '''/move/' + getElementById('mvth').value;" style="padding-top: 0;  padding-bottom: 0;  padding-left: 6px;  padding-right: 6px;  border-radius: 0;  border-color: gray;  background-color: #eee;">변경</button><br />'''
        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'utt'])
        if curs.fetchall():
            data += '''[ADMIN] 쓰레드 주제 변경 <input style="width:160px;border-radius: 0;padding: 0;border-color: gray;" type="text" style="width:160px" id="reth" value="''' + sub + '''">  <button type="button" onclick="location.href = '/admin/thread/''' + url_pas(tnum) + '''/ren/' + getElementById('reth').value;" style="padding-top: 0;  padding-bottom: 0;  padding-left: 6px;  padding-right: 6px;  border-radius: 0;  border-color: gray;  background-color: #eee;">변경</button><br />'''

        if admin == 0 or admin == 1:
            if ban == 1:
                data += '''
                    <form>
                        <textarea style="height: 100px;background:#efefef;cursor:not-allowed" name="content" disabled readonly>닫힌 토론입니다.</textarea>
                        ''' + captcha_get() + (ip_warring() if display == '' else '') + '''
                        <button type="button" id="save" style="width:120px" disabled>''' + load_lang('send') + '''</button>
                    </form></div>
                '''
            elif banp == 1:
                data += '''
                    <form>
                        <textarea style="height: 100px;background:#efefef;cursor:not-allowed" name="content" disabled readonly>pause 상태입니다.</textarea>
                        ''' + captcha_get() + (ip_warring() if display == '' else '') + '''
                        <button type="button" id="save" style="width:120px" disabled>''' + load_lang('send') + '''</button>
                    </form></div>
                '''
            else:
                data += '''
                    <form method="post" id="postComment">
                        <textarea style="height: 100px;" name="content" id="conten"></textarea>
                        ''' + captcha_get() + (ip_warring() if display == '' else '') + '''
                        <button type="submit" id="save" style="width:120px">''' + load_lang('send') + '''</button>
                    </form></div>
                '''
        delt = ''
        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'dt'])
        if curs.fetchall():
            delt = '''<span class="pull-right"><a class="btn btn-danger btn-sm" href="/admin/thread/''' + url_pas(tnum) + '''/delete" onclick="return confirm('정말로?')">[ADMIN] 삭제</a></span>'''
        data += '''
        <SCRIPT>
        /* https://stackoverflow.com/questions/11254429/hiding-all-elements-with-the-same-class-name */

        function toggle(className, displayState){
            var elements = document.getElementsByClassName(className)

            for (var i = 0; i < elements.length; i++){
                elements[i].parentNode.parentNode.style.display = displayState;
            }
        }

        $('#noDisplayHideAuthor').click(function(){
            if(document.getElementById('noDisplayHideAuthor').checked)
                toggle('r-hidden-body', 'none');
            else
                toggle('r-hidden-body', 'block');
        });

        toggle('r-hidden-body', 'none');
        </SCRIPT>
        '''
        return easy_minify(flask.render_template(skin_check(),
            imp = [name, wiki_set(), custom(), other2([' (' + load_lang('discussion') + ') - ' + sub, 0])],
            data = '<input type=hidden name=last_loaded_res value="' + d + '"> <h2 class=wiki-heading style="cursor: pointer; border: none;"><span onclick="var ddd = document.getElementById(\'tb\'); if(ddd.style.display == \'block\') ddd.style.display = \'none\'; else ddd.style.display = \'block\'; ">' + sub + '</span> ' + delt + '<span style="float: right; "><input type="checkbox" id="noDisplayHideAuthor" checked><label for="noDisplayHideAuthor" style="font-size: 1rem;">숨겨진 댓글 보이지 않기</label></span></h2>''' + '<div style="display:block" id="tb"><div id="res-container">' + all_data + data,
            menu = [['discuss/' + url_pas(name), load_lang('list')]],
            st = 3
        ))




def topic_seed_2_3_4(conn, tnum, snum):
    curs = conn.cursor()
    curs.execute("select title, sub from topic where tnum = ?", [tnum])
    fet = curs.fetchall()
    if fet:
        name = fet[0][0]
        sub = fet[0][1]
    else:
        return re_error('/error/7000')

    tit = name + ' (토론) - ' + sub + ' - ' + wiki_set()[0]


    if getacl(name, 'read') == 0:
        return noread(conn, name)

    if re.search('^사용자:', name):
        ns = '사용자'
    elif re.search('^분류:', name):
        ns = '분류'
    elif re.search('^틀:', name):
        ns = '틀'
    elif re.search('^휴지통:', name):
        ns = '휴지통'
    elif re.search('^파일:', name):
        ns = '파일'
    elif re.search('^' + wiki_set()[0] + ':', name):
        ns = wiki_set()[0]
    else:
        ns = '문서'

    ban = topic_check(name, sub)
    admin = admin_check(3)

    curs.execute("select sub from rd where tnum = ? and removed = '1'", [tnum])
    if curs.fetchall() and admin_check() != 1:
        return re_error('/error/7000')

    if getacl(name, 'read') != 1:
        return re_error('/error/3')


    curs.execute("select id from topic where title = ? and sub = ? limit 1", [name, sub])
    topic_exist = curs.fetchall()
    if not topic_exist and len(sub) > 256:
        return re_error('/error/11')

    if 3 == 4:
        print ("bad")
    else:
        curs.execute("select title from rd where title = ? and sub = ?", [name, sub])
        if not(curs.fetchall()):
            return re_error('/error/7000')
        curs.execute("select title from rd where title = ? and sub = ? and stop = 'O'", [name, sub])
        close_data = curs.fetchall()

        curs.execute("select title from rd where title = ? and sub = ? and stop = 'S'", [name, sub])
        stop_data = curs.fetchall()

        display = ''
        all_data = ''
        data = ''
        number = 1

        if (close_data or stop_data) and admin != 1:
            display = 'display: none;'

        curs.execute("select data, id, date, ip, block, top, adm from topic where tnum = ? order by id + 0 asc", [tnum])
        topic = curs.fetchall()

        nn = 1
        number = 1
        for topic_data in topic:
            if not(number == 1) and number < snum:
                number += 1
                continue
            if number > snum + 29:
                break
            curs.execute("select block, ip, date from topic where title = ? and sub = ? and id = ?", [url_pas(name), url_pas(sub), str(number)])
            admdswiwdiataa = curs.fetchall()
            user_write = topic_data[0]
            user_write = render_set(data = user_write)
            ip = ip_pas_t(topic_data[3])
            curs.execute('select acl from user where id = ?', [topic_data[3]])
            user_acl = curs.fetchall()
            blablabla = 0


            curs.execute("select ip from topic where tnum = ? and id = '1'", [tnum])
            fet = curs.fetchall()
            if fet:
                if fet[0][0] == topic_data[3]:
                    start = 1
                else:
                    start = 0
            else:
                return ''
            if topic_data[4] == 'O':
                blind_data = 'id="toron_color_grey"'
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'htc'])
                if not(curs.fetchall()):
                    curs.execute("select who from re_admin where what = ? order by time desc limit 1", ['blind (' + name + ' - ' + sub + '#' + str(number) + ')'])
                    who_blind = curs.fetchall()
                    if who_blind:
                        user_write = '[' + who_blind[0][0] + '에 의해 숨겨진 글입니다.]'
                        blablabla = 1
                    else:
                        user_write = '[숨겨진 글입니다.]'
                        blablabla = 1
                curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'htc'])
                if curs.fetchall():
                    curs.execute("select who from re_admin where what = ? order by time desc limit 1", ['blind (' + name + ' - ' + sub + '#' + str(number) + ')'])
                    who_blind = curs.fetchall()
                    if who_blind:
                        user_write ='[' + who_blind[0][0] + '에 의해 숨겨진 글입니다.]<br><div class="text-line-break" style="margin: 25px 0px 0px -10px; color: #fff; display:block" id="shc' + str(number) + '"><a class="text" onclick="getElementById(\'hc' + str(number) + '\').style.display = \'block\';getElementById(\'shc' + str(number) + '\').style.display = \'none\';" style=" color: #fff;">[ADMIN] Show hidden content</a><div class="line"></div></div><div id="hc' + str(number) + '" style="display:none"><br>' + user_write + '</div>'
                        blablabla = 1
                    else:
                        user_write = '[숨겨진 글입니다.]<br><br>' + user_write
                        blablabla = 1
            else:
                blind_data = ''

            if topic_data[6] == '1':
                ip = '<strong>' + ip
                ip += '</strong>'
                #ip += ' <a href="javascript:void(0);" title="' + load_lang('admin') + '">★</a>'

            if ban_check(topic_data[3]) == 1:
                ip += ' <sub>(차단됨)</sub>'

            curs.execute("select date from topic where tnum = ? and id = ?", [tnum, str(number)])
            dt = curs.fetchall()




            #if admin == 1 or blind_data == '':
                #ip += '<a href="/topic/' + url_pas(name) + '/sub/' + url_pas(sub) + '/admin/' + str(number) + '"> [도구]</a>'





            oraoraorgaanna = 0

            if topic_data[5] == '1':
                oraoraorgaanna = 1
                if start == 1:
                    color = '_green'
                else:
                    color = ''
            elif start == 1:
                color = '_green'
            else:
                color = ''

            if user_write == '':
                user_write = '<br>'

            if dt:
                if topic_data[5] == '1':
                    all_data +=  '<div class="res res-type-status">'
                else:
                    all_data +=  '<div class="res res-type-normal">'


                all_data += '''
                        <div class="r-head'''
                if start == 1:
                    all_data += ' first-author'
                ddd = dt[0][0].split(' ')[0]
                ttt = dt[0][0].split(' ')[1]
                all_data += '''">
                            <span class="num"><a id="''' + str(number) + '">#' + str(number) + '</a>&nbsp;</span> ' + ip + '''<span style="margin-left: 25px;float:right"><time datetime="''' + ddd + 'T' + ttt + '''.000Z" data-format="Y-m-d H:i:s">''' + dt[0][0] + '''</time></span><div class="clearfix"></div>
                        </div>
                        <div class="r-body'''
                if topic_data[4] == 'O':
                    all_data += ' r-hidden-body'

                all_data += '''">'''

            if user_write == '스레드 상태를 <b>open</b>로 변경' or user_write == '스레드 상태를 <b>open</b>로 변경 ':
                user_write = '스레드 상태를 <b>normal</b>로 변경'
            all_data += user_write + '''</div></div>
                '''
            curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'htc'])
            if curs.fetchall():
                all_data += '''
                <div class="combo admin-menu">

				<a class="btn btn-danger btn-sm" href="/admin/topic/''' + url_pas(tnum) + '''/hide/''' + str(number) + '''">'''
                if blablabla == 1:
                    all_data += '''[ADMIN] 숨기기 해제'''
                else:
                    all_data += '''[ADMIN] 숨기기'''
                all_data += '''</a></div>


            '''
            #all_data += '''<br><br>'''

            number += 1

        nn = str(number)

        data += '''
            </div></div><input type="hidden" id="isa" value="''' + str(admin) + '''">
            <div id="plus_topic"><input id="enu" type="hidden" value="''' + nn + '''"></div>
            <script>topic_plus_load("''' + str(tnum) + '''", ''' + nn + ''');</script>
            <SCRIPT>
            /*
               https://stackoverflow.com/questions/1642447/how-to-change-the-content-of-a-textarea-with-javascript
               https://stackoverflow.com/questions/3527041/prevent-any-form-of-page-refresh-using-jquery-javascript
            */
            $(function () {
                $('#postComment').on('submit',function (e) {

                          $.ajax({
                            type: 'post',
                            url: \'/topic/''' + url_pas(name) + '''/sub/''' + url_pas(sub) + '''\',
                            data: $('#postComment').serialize(),
                            success: function () {
                             document.getElementById('conten').value = '';
                             var myTextArea = document.getElementById('conten');
                             myTextArea.innerHTML = '';
                             myTextArea.innerText = '';
                            }
                          });
                      e.preventDefault();
                    });
            });
            </SCRIPT>

            <br><div id="reload"></div><h2 style="cursor: pointer; border: none;" onclick="var dc = document.getElementById(\'dcf\'); if(dc.style.display == \'block\') dc.style.display = \'none\'; else dc.style.display = \'block\'; ">댓글 달기</h2><div id="dcf" style="display: block; ">'''

        curs.execute("select stop from rd where title = ? and sub = ?", [name, sub])
        ban = 0
        bbc = curs.fetchall()
        if bbc:
            if bbc[0][0] == 'O':
                ban = 1
            else:
                ban = 0

        curs.execute("select pause from rd where title = ? and sub = ?", [name, sub])
        banp = 0
        bbcc = curs.fetchall()
        if bbcc:
            if bbcc[0][0] == 'O':
                banp = 1
            else:
                banp = 0

        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'uts'])
        if curs.fetchall():
            if ban == 1:
                ct = 'normal'
            else:
                ct = 'close'
            if banp == 1:
                ct2 = 'normal'
            else:
                ct2 = 'pause'
            data += '''
                [ADMIN] 쓰레드 상태 변경 <select style="padding: 0;border-radius: 0;border-color: gray;" name="status" id="sttssu">
                    <option value="close">''' + ct + '''</option>
                    <option value="pause">''' + ct2 + '''</option>

                </select>  <button style="padding-top: 0;padding-bottom: 0;padding-left: 6px;padding-right: 6px;border-radius: 0;border-color: gray;background-color: #eee;" type="button" onclick="location.href = '/topic/''' + url_pas(name) + '''/sub/''' + url_pas(sub) + '''/tool/' + getElementById('sttssu').value;">변경</button><br />
                '''

        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'utd'])
        if curs.fetchall():
            data += '''[ADMIN] 쓰레드 이동 <input style="width:160px;border-radius: 0;padding: 0;border-color: gray;" type="text" style="width:160px" id="mvth" value="''' + name + '''">  <button type="button" onclick="location.href = '/topic/''' + url_pas(name) + '''/sub/''' + url_pas(sub) + '''/move/' + getElementById('mvth').value;" style="padding-top: 0;  padding-bottom: 0;  padding-left: 6px;  padding-right: 6px;  border-radius: 0;  border-color: gray;  background-color: #eee;">변경</button><br />'''
        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'utt'])
        if curs.fetchall():
            data += '''[ADMIN] 쓰레드 주제 변경 <input style="width:160px;border-radius: 0;padding: 0;border-color: gray;" type="text" style="width:160px" id="reth" value="''' + sub + '''">  <button type="button" onclick="location.href = '/topic/''' + url_pas(name) + '''/sub/''' + url_pas(sub) + '''/ren/' + getElementById('reth').value;" style="padding-top: 0;  padding-bottom: 0;  padding-left: 6px;  padding-right: 6px;  border-radius: 0;  border-color: gray;  background-color: #eee;">변경</button><br />'''

        if admin == 0 or admin == 1:
            if ban == 1:
                data += '''
                    <form>
                        <textarea style="height: 100px;background:#efefef;cursor:not-allowed" name="content" disabled readonly>닫힌 토론입니다.</textarea>
                        ''' + captcha_get() + (ip_warring() if display == '' else '') + '''
                        <button type="button" id="save" style="width:120px" disabled>''' + load_lang('send') + '''</button>
                    </form></div>
                '''
            elif banp == 1:
                data += '''
                    <form>
                        <textarea style="height: 100px;background:#efefef;cursor:not-allowed" name="content" disabled readonly>pause 상태입니다.</textarea>
                        ''' + captcha_get() + (ip_warring() if display == '' else '') + '''
                        <button type="button" id="save" style="width:120px" disabled>''' + load_lang('send') + '''</button>
                    </form></div>
                '''
            else:
                data += '''
                    <form method="post" id="postComment">
                        <textarea style="height: 100px;" name="content" id="conten"></textarea>
                        ''' + captcha_get() + (ip_warring() if display == '' else '') + '''
                        <button type="submit" id="save" style="width:120px">''' + load_lang('send') + '''</button>
                    </form></div>
                '''
        delt = ''
        curs.execute("select perm from grant where user = ? and perm = ?", [ip_check(), 'dt'])
        if curs.fetchall():
            delt = '''<span class="pull-right"><a class="btn btn-danger btn-sm" href="/topic/''' + url_pas(name) + '''/sub/''' + url_pas(sub) + '''/del" onclick="return confirm('정말로?')">[ADMIN] 삭제</a></span>'''

        return all_data

