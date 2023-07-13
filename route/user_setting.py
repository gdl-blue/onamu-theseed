from .tool.func import *

def user_info(conn):
    curs = conn.cursor()

    ip = ip_check()

    curs.execute("select acl from user where id = ?", [ip])
    data = curs.fetchall()
    if ban_check() == 0:
        if data:
            acl = load_lang('member')
            if admin_check(5) == 1:
                acl = loadLang('관리자', "Administrator")
            if getperm('arbiter') == 1:
                acl = loadLang("중재자", "Arbiter")
            if getperm('tribune') == 1:
                acl = loadLang("호민관", "Tribune")
            if admin_check() == 1:
                acl = loadLang("개발자", "Developer")
        else:
            if islogin() == 1:
                acl = loadLang("일반 사용자", "Member")
            else:
                acl = loadLang("로그인하지 않음", "Please Login!")
    else:
        acl = load_lang('blocked')

        match = re.search("^([0-9]{1,3}\.[0-9]{1,3})", ip)
        if match:
            match = match.groups()[0]
        else:
            match = '-'

        curs.execute("select end, login, band from ban where block = ? or block = ?", [ip, match])
        block_data = curs.fetchall()
        if block_data:
            if block_data[0][0] != '':
                acl += ' (' + load_lang('period') + ' : ' + block_data[0][0] + ')'
            else:
                acl += ' (' + load_lang('limitless') + ')'

            if block_data[0][1] != '':
                acl += ' (' + load_lang('login_able') + ')'

            if block_data[0][2] == 'O':
                acl += ' (' + load_lang('band_blocked') + ')'

    curs.execute('select count(name) from alarm where name = ?', [ip_check()])
    notificationData = curs.fetchall()
    if notificationData:
        plus2 = '<li><a href="/member/notifications">' + loadLang("알림", "Notifications") + ' (' + str(notificationData[0][0]) + ')</a></li>'
    else:
        plus2 = '<li><a href="/member/notifications">' + loadLang('알림', 'Notifications') + '</a></li>'

    if custom()[2] != 0:
        ip_user = '<a href="/w/사용자:' + ip + '">' + ip + '</a>'

        spin = custom()[20]

        plus = '''
            <li><a href="/member/logout">''' + load_lang('logout') + '''</a></li>
            <li><a href="/member/mypage">''' + load_lang('user_setting') + '''</a></li>
        '''

        if spin != '00000000':
            plus += '<li style="margin-bottom: 10px;">지원 PIN: ' + spin + '</li>'

        plus2 += '<li><a href="/member/starred_documents">' + load_lang('watchlist') + '</a></li>'
        plus3 = '<li><a href="/acl/사용자:' + url_pas(ip) + '">' + loadLang('사용자 문서 ACL', 'My User Document\'s ACL') + '</a></li>'
    else:
        ip_user = ip

        plus = '''
            <li><a href="/member/login">''' + load_lang('login') + '''</a></li>
            <li><a href="/member/signup">''' + load_lang('register') + '''</a></li>
        '''
        plus3 = ''

        curs.execute("select data from other where name = 'email_have'")
        test = curs.fetchall()
        if test and test[0][0] != '':
            plus += '<li><a href="/pass_find">' + load_lang('password_search') + '</a></li>'

    if 'state' in flask.session and flask.session['state'] == 1:
        ismember = 'author'
    else:
        ismember = 'ip'
    #endif

    return '''
            <h2 class=wiki-heading>''' + loadLang('내 계정', 'My Account') + '''</h2>
            <div class=wiki-heading-content>
            <ul>
                <li>''' + ip_user + ' (' + acl + ''')</li>
                <li><a href="/contribution/''' + ismember + '''/''' + url_pas(ip) + '''/document">''' + loadLang('내 문서 기여 내역', 'My document contributions') + '''</a></li>
                <li style="margin-bottom: 10px;"><a href="/contribution/''' + ismember + '''/''' + url_pas(ip) + '''/discuss">''' + loadLang('내 토론 참여 내역', 'My discussion history') + '''</a></li>
                ''' + plus + '''
            </ul>
            </div>
            <h2 class=wiki-heading>''' + load_lang('tool') + '''</h2>
            <div class=wiki-heading-content>
            <ul>
                ''' + plus3 + '''
                <li><a href="/custom_head">''' + loadLang('사용자 지정 &lt;HEAD&gt; 코드', 'Custom &lt;HEAD&gt; Code') + '''</a></li>
            </ul>
            </div>
            <h2 class=wiki-heading>''' + load_lang('other') + '''</h2>
            <div class=wiki-heading-content>
            <ul>
            ''' + plus2 + '''
            <li>
                <a href="/member/ip_whitelist">IP ''' + loadLang('허용 목록', 'Whitelist') + '''</a>
            </li>
            </ul>
            </div>
        '''

def user_setting_2(conn, server_init):
    curs = conn.cursor()

    support_language = server_init.server_set_var['language']['list']

    if islogin() != 1:
        return redirect("/member/login?redirect=/member/mypage")


    ip = ip_check()
    user_state = flask.request.args.get('user', 'ip')

    if user_state == 'ip':
        if flask.request.method == 'POST':
            curs.execute('select data from user_set where name = ? and id = ?', ['lang', ip_check()])
            if curs.fetchall():
                curs.execute("delete from user_set where name = ? and id = ?", ['lang', ip_check()])
            curs.execute("insert into user_set (name, id, data) values (?, ?, ?)", ['lang', ip_check(), getForm('lang', '')])

            auto_list = ['email', 'skin', 'color', 'wallpaper_code']
            curs.execute("select data from user_set where name = 'skin' and id = ?", [ip_check()])
            skd = curs.fetchall()
            if not(skd):
                skd = [[getForm('skin', '')]]
            for auto_data in auto_list:
                curs.execute('select data from user_set where name = ? and id = ?', [auto_data, ip])
                if curs.fetchall():
                    curs.execute("update user_set set data = ? where name = ? and id = ?", [flask.request.form.get(auto_data, ''), auto_data, ip])
                else:
                    curs.execute("insert into user_set (name, id, data) values (?, ?, ?)", [auto_data, ip, flask.request.form.get(auto_data, '')])

            #구버전 브라우져는 색구성표 목록 갱신이 안 된되는 관계로..
            ua = flask.request.headers.get('User-Agent')
            if re.search('[;] MSIE \d{1,1}[.]\d{1,5};', ua): # MS IE 1.0부터 9.0까지 인식
                if skd[0][0] != getForm('skin', ''):
                    try:
                        defaultSkinColor = open('./views/' + skin_check(1) + '/dfltcolr.scl', 'r').read()
                    except:
                        defaultSkinColor = 'default'
                    curs.execute('select data from user_set where name = \'color\' and id = ?', [ip])
                    if curs.fetchall():
                        curs.execute("update user_set set data = ? where name = 'color' and id = ?", [defaultSkinColor, ip])

            if getForm("regenspin", 0) != 0:
                curs.execute("delete from spin where username = ?", [ip])
                curs.execute("insert into spin (username, pin) values (?, ?)", [ip, rndval("01234567890", 8)])

            conn.commit()

            return redirect('/member/mypage')
        else:
            curs.execute('select data from user_set where name = "email" and id = ?', [ip])
            data = curs.fetchall()
            if data:
                email = data[0][0]
            else:
                email = '-'

            div2 = load_skin()
            div3 = ''

            curs.execute("select data from user_set where name = 'lang' and id = ?", [ip_check()])
            data = curs.fetchall()
            if not data:
                curs.execute('select data from other where name = "language"')
                data = curs.fetchall()
                if not data:
                    data = [['en-US']]

            for lang_data in [['ko-KR', '한국어'], ['en-US', 'English (Uncompleted)']]:
                if data and data[0][0] == lang_data[0]:
                    div3 += '<option value="' + lang_data[0] + '" selected>' + lang_data[1] + '</option>'
                else:
                    div3 += '<option value="' + lang_data[0] + '">' + lang_data[1] + '</option>'

            oauth_provider = load_oauth('_README')['support']
            oauth_content = '<ul>'
            for i in range(len(oauth_provider)):
                try:
                    uid = flask.session['id']
                except:
                    uid = ''
                curs.execute('select name, picture from oauth_conn where wiki_id = ? and provider = ?', [uid, oauth_provider[i]])
                oauth_data = curs.fetchall()
                if len(oauth_data) == 1:
                    oauth_content += '<li>{} - {}</li>'.format(oauth_provider[i].capitalize(), load_lang('connection') + ' : <img src="{}" width="17px" height="17px">{}'.format(oauth_data[0][1], oauth_data[0][0]))
                else:
                    oauth_content += '<li>{} - {}</li>'.format(oauth_provider[i].capitalize(), load_lang('connection') + ' : <a href="/oauth/{}/init">{}</a>'.format(oauth_provider[i], load_lang('connect')))

            oauth_content += '</ul>'

            http_warring = '<hr class=\"main_hr\"><span onclick="egg=egg+1;if(egg>67)location.href=\'/views/easter_egg.html\';">' + load_lang('http_warring') + '</span>'

            curs.execute('select data from other where name = ?', ['skin'])
            ds = curs.fetchall()
            if not(ds):
                ds = [['기본스킨']]

            curs.execute("select data from user_set where id = ? and name = 'color'", [ip_check()])
            mycolor = curs.fetchall()
            if not(mycolor):
                try:
                    defaultSkinColor = open('./views/' + skin_check(1) + '/dfltcolr.scl', 'r').read()
                except:
                    defaultSkinColor = 'default'
                mycolor = [[defaultSkinColor]]

            try:
                rawSkinColorList = open('./views/' + skin_check(1) + '/colors.scl', 'r').read()
                skinColorList = ''
                for i in rawSkinColorList.split(';'):
                    vName = i.split(',')[0]
                    dName = i.split(',')[1]

                    df = ''
                    if vName == mycolor[0][0]:
                        df = ' selected'

                    skinColorList += '<option value="' + html.escape(vName) + '"' + df + '>' + html.escape(dName) + '</option>'
            except:
                skinColorList = '<option value=default>' + load_lang('default') + '</option>'

            curs.execute("select data from user_set where id = ? and name = 'wallpaper_code'", [ip_check()])
            mybgcd = curs.fetchall()
            if not(mybgcd):
                bgclrcss = '-'
            else:
                bgclrcss = mybgcd[0][0]

            curs.execute("select name, ip, ua, today from ua_d where name = ? COLLATE NOCASE order by today desc limit 100", [ip_check()])
            loginhis = '<table class=table><thead><tr><td><strong>Date</strong></td><td><strong>IP</strong></td><td><strong>' + load_lang('user_agent') + '</strong></td></tr></thead><tbody id>'
            for data in curs.fetchall():
                loginhis += '<tr><td>' + generateTime(data[3]) + '</td><td>' + data[1] + '</td><td>' + data[2] + '</td></tr>'
            loginhis += '</tbody></table>'


            xptlst = '''
            <div style="display:inline-block;float:left;width: 48%">
                        색상표<br><select size=5 class="form-control" name="color" style="width:100%" id="skinColorSelect">''' + skinColorList + '''</select></div>
                        <div style="display:inline-block;float:right;width: 48%">스킨<br><select class="form-control" size=5 name="skin" style="width:100%"><option value="default" selected>기본스킨 (''' + ds[0][0] + ''')</option>''' + div2 + '''</select></div><br><br><br><br><br><br>'''

            if custom()[2] == 0:
                 nodisplay = ' nodisplay'
            else:
                 nodisplay = ''

            return easy_minify(flask.render_template(skin_check(),
                imp = [ip_check() + ' ' + loadLang('등록 정보', "Properties"), wiki_set(), custom(), other2([0, 0])],
                data = '''
                    <form method="post">
                        <style>
                            .tab-pane {
                                padding: 10px;
                            }
                        </style>
                        <ul class="nav nav-tabs" role="tablist" style="height: 38px;">
                            <li class="nav-item nodisplay">
                                <a class="nav-link data-toggle="tab" href="#overview" role="tab">''' + loadLang("개요", "Overview") + '''</a>
                            </li>
                            <li class="nav-item''' + nodisplay + '''">
                                <a class="nav-link active" data-toggle="tab" href="#wallpaper" role="tab">''' + load_lang("background") + '''</a>
                            </li>
                            <li class="nav-item nodisplay">
                                <a class=nav-link data-toggle="tab" href="#loginHistory" role="tab">''' + load_lang("loginhis") + '''</a>
                            </li>
                            <li class="nav-item''' + nodisplay + '''">
                                <a class=nav-link data-toggle="tab" href="#colorScheme" role="tab">''' + load_lang("colorscheme") + '''</a>
                            </li>
                            <li class=nav-item>
                                <a class=nav-link data-toggle="tab" href="#userSettings" role="tab">''' + loadLang("효과", "Effects") + '''</a>
                            </li>
                            <li class="nav-item''' + nodisplay + '''">
                                <a class=nav-link data-toggle="tab" href="#personalInfo" role="tab">''' + load_lang("settings") + '''</a>
                            </li>
                        </ul>

                        <div class="tab-content bordered">
                            <div class=tab-pane id=overview>
                                ''' + user_info(conn) + '''
                            </div>
                            <div class="tab-pane active" id=wallpaper>
                                <div class=form-group>
                                    <P>''' + loadLang("초기화하려면 CSS를 대시(-)로 설정하십시오.", "Set the CSS code to dash('-) to reset the background.") + '''</P>
                                    <div id=previewFrame style="border: 5px solid #f3f3f3; border-radius: 5px; width: 160px; height: 130px; box-shadow: 0px 3px 5px #ccc; text-align: center; vertical-align: middle;">―――――<br>―――――<br>―――――</div>
                                            <br>
                                    CSS: <input value="''' + html.escape(bgclrcss) + '''" type=text id=wallpaperCode name=wallpaper_code class=form-control style="width: 250px; display: inline-block;">

                                    <br>
                                    <div style="float: right;">
                                        <a style="width: 100px;" href="/member/custom_head" class="btn btn-secondary">''' + load_lang("advanced") + '''...</a>
                                    </div>
                                    <label>''' + load_lang("color") + ''':&nbsp;</label><input type=color style="width: 100px;" id=colorSelect><br>
                                    <label>''' + loadLang("이미지 주소", "Image URL") + ''':&nbsp;</label><input class=form-control type=text style="width: 250px; display: inline-block;" id=txtImageURL>
                                    <script>
                                        $(function() {
                                            $('#colorSelect').change(function() {
                                                $('#wallpaperCode').val($(this).val());
                                                $('#previewFrame').css('background', $('#wallpaperCode').val());
                                            });

                                            $(document).on("propertychange change keyup paste input", '#wallpaperCode', function() {
                                                $('#previewFrame').css('background', $('#wallpaperCode').val());
                                            });

                                            $(document).on("propertychange change keyup paste input", '#txtImageURL', function() {
                                                $('#wallpaperCode').val("url('" + $('#txtImageURL').val() + "');");
                                            });
                                        });
                                    </script>
                                </div>
                            </div>
                            <div class=tab-pane id=colorScheme>
                                <script>
                                    $(function() {
                                        $('#skinSelect').change(function() {
                                            $('#skinPrevImg').attr('src', "/skins/" + $(this).val() + "/preview.png");
                                            var scl = '', rscl;
                                            $.get('/skins/' + $(this).val() + '/colors.scl', function(response) {
                                                rscl = response;
                                                if(rscl.includes('404')) {
                                                    rscl = "default,''' + load_lang('default') + '''";
                                                }
                                                for(var i=0; i<(rscl.split(';').length); i++) {
                                                    scl += '<option value="' + rscl.split(';')[i].split(',')[0] + '">' + rscl.split(';')[i].split(',')[1] + '</option>';
                                                }

                                                document.getElementById('skinColorSelect').innerHTML = scl;
                                            });

                                            if($(this).val() == 'default') {
                                                var sknnm = $('#skinSelect option:selected').text().replace(/^''' + load_lang("default") + ''' [(]/, '').replace(/[)]$/, '');
                                                $('#skinPrevImg').attr('src', "/skins/" + sknnm + "/preview.png");

                                                var scl = '', rscl;
                                                $.get('/skins/' + sknnm + '/colors.scl', function(response) {
                                                    rscl = response;
                                                    if(rscl.includes('404')) {
                                                        rscl = "default,''' + load_lang('default') + '''";
                                                    }

                                                    for(var i=0; i<(rscl.split(';').length); i++) {
                                                        scl += '<option value="' + rscl.split(';')[i].split(',')[0] + '">' + rscl.split(';')[i].split(',')[1] + '</option>';
                                                    }

                                                    document.getElementById('skinColorSelect').innerHTML = scl;
                                                });
                                            }
                                        });
                                    });
                                </script>
                                <img src="/skins/''' + html.escape(skin_check(1)) + '''/preview.png" style="display:inline-block; border: 2px inset #aaa;" id=skinPrevImg><br><br>

                                <div class=form-group>''' + load_lang("window_and_buttons") + ''':<br><select style="width: 250px;" class="form-control" name="skin" id=skinSelect><option value="default" selected>''' + load_lang("default") + ''' (''' + ds[0][0] + ''')</option>''' + div2 + '''</select></div>
                                <div class=form-group>
                                <script>$(function() { $('#skinColorSelect').val(\'''' + mycolor[0][0] + '''\'); });</script>
                                <label>''' + load_lang("color_scheme") + ''':</label>
                                <br>
                                <a style="float: right; width: 100px;" class="btn btn-secondary" href="/member/advanced_style">''' + load_lang("advanced") + '''...</a>
                                <select style="width: 250px;" class="form-control" name="color" id="skinColorSelect">''' + skinColorList + '''</select></div>
                            </div>
                            <div class=tab-pane id=loginHistory>
                                <p>''' + load_lang("last_100_logins") + '''</p>
                                ''' + "loginhis" + '''
                            </div>
                            <div class=tab-pane id=userSettings>
                                <P>개발중인 기능입니다. 기다려 주십시오. 설정 적용은 아직 안됩니다.</P>

                                <fieldset>
                                    <legend>토론 기능</legend>

                                    <label><input type=checkbox name=topicurl> 토론 주소는 순번으로</label><br>
                                    <label><input type=checkbox name=oldhideint> 숨겨진 댓글을 기존 방식으로 표시</label><br>
                                    <label><input type=checkbox name=showhiddenres> 숨겨진 댓글을 기본으로 표시</label><br>
                                </fieldset>
                            </div>
                            <div class="tab-pane" id=personalInfo>
                                <div class=form-group><label>''' + load_lang("username") + ''':</label><br><input class="form-control" type="text" readonly value="''' + ip + '''"></div>
                                <div class=form-group><label>''' + load_lang("password") + ''':</label><br><a href="/pw_change" class="btn btn-secondary">''' + load_lang("change_password") + '''...</a></div>
                                <a style="float: right; text-decoration: underline;" href="/settings">''' + load_lang("skin_settings") + '''...</a>
                                <div class=form-group><label>''' + load_lang("email_address") + ''':</label><br><input class="form-control" type="text" readonly value="''' + email + '''"><a href="/email_change" class="btn btn-secondary">''' + load_lang("change_address") + '''...</a></div>
                                <div class=form-group>
                                    <label>언어/Language: </label><br>
                                    <select name="lang" class=form-control id=languageSelect>
                                        ''' + div3 + '''
                                    </select>
                                </div>
                                <div class=form-group>
                                    <label>''' + loadLang("지원 PIN 다시 생성", "Regenerate Support PIN") + ''': </label>
                                    <div class=checkbox>
                                        <label><input type=checkbox name=regenspin>
                                            ''' + loadLang("설정 적용 시 다시 생성하기를 원합니다.", "Regenerate Support PIN when I apply the settings") + '''
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div style="display:none"><hr class=\"main_hr\"><span>''' + load_lang('language') + '''</span>

                        <span>''' + load_lang('oauth_connection') + '''</span>
                        ''' + oauth_content + '''</div><div class="btns">
                        <button type="reset" class="form control btn btn-secondary">''' + load_lang("reset") + '''</button> <button type="button" onclick="history.go(0);" class="form control btn btn-secondary">''' + load_lang("cancel") + '''</button> <button type="submit" class="form control btn btn-primary">''' + load_lang("apply") + '''</button></div>
                        ''' + http_warring + '''
                    </form>
                ''',
                menu = [['user', load_lang('return')]],
                is_mypage = 1
            ))
    else:
        pass

def advancedStyle(conn):
    curs = conn.cursor()

    if 'state' in flask.session and flask.session['state'] == 1:
        test = 2
    else:
        return redirect('/member/login?redirect=/member/advanced_style')
    content = '''
        <form method=post>
            <style id=cssAdvStyleTable>
                table {
                    width: 100%;
                }

                td {
                    padding: 5px;
                    border: 1px dashed #eceeef;
                }

                div.tab-content {
                    overflow: scroll;
                    height: 360px;
                }

                div.tab-pane {
                    padding: 5px;
                }

                a.nav-link {
                    display: inline-block !important;
                }

                .table-wiki-quote {
                    padding: 10px;
                    background: #eceeef;
                    border: 2px dashed #ccc;
                    border-left: 5px solid #0080C8;
                    display: inline-block;
                }

                .btns * {
                    float: right;
                }

                input[type="range"], input[type="range"]:focus {
                    padding: 0 !important;
                }

                #lblChkBGT {
                    float: right;
                }

            </style>

            <script id=core-config-helper>
                if(typeof jQuery === 'undefined') {
                    alert("이 페이지는 jQuery가 지원되지 않는 인터넷 탐색기에서 사용이 불가합니다.");
                    location.href = '/member/mypage';
                }

                $(function() {
                    for(var i=1; i<=''' + str(advCount) + '''; i++) {
                        $('textarea[name="CSS' + String(i) + '"]').text(
                            $('style#CSS-' + String(i)).html()
                        );
                    }

                    $("select#selElement").change(function() {
                        try {
                            $("option#0").remove();
                        } catch(e) {}

                        var cssval = $("textarea#JSC" + $("#selElement").children(":selected").attr("id")).text().split(";");
                        var csslst = [
                            "txtPadding", "txtBgolor", "txtBorderWidth", "txtBorderStyle", "selBorderStyle", "txtBorderColor",
                            "txtBorderRadius1", "txtBorderRadius2", "txtBorderRadius3", "txtBorderRadius4",
                            "selFont", "txtTextColor", "txtFontSize", "bs", "ud", "fw", "ia", "txtMargin", "selSizeUnit", "selCursor"
                        ];

                        for(var i=0; i<csslst.length; i++) {
                            try {
                                $("#" + csslst[i]).val(cssval[i]);
                            } catch(e) {}
                        }
                    });

                    $("table#css-config tbody tr input, table#css-config tbody tr select:not(#selElement)").change(function() {
                        var fw, ia, ud, sd, bs, bg;

                        if ($('input#chkBold').is(':checked')) {
                            fw = "bold";
                        } else {
                            fw = "normal";
                        }
                        if ($('input#chkItalic').is(':checked')) {
                            ia = "italic";
                        } else {
                            ia = "normal";
                        }
                        if ($('input#chkUnderline').is(':checked')) {
                            ud = "underline";
                        } else {
                            ud = "";
                        }
                        if ($('input#chkStrike').is(':checked')) {
                            sd = "line-through";
                        } else {
                            sd = "";
                        }
                        if(Number($("input#txtBoxShadow").val()) == -1) {
                            bs = "none";
                        } else {
                            bs = String($("input#txtBoxShadowX").val()) + "px " + String($("input#txtBoxShadowY").val()) + "px " + String($("input#txtBoxShadow").val()) + "px gray";
                        }

                        bg = String($("#txtBgolor").val());

                        if(Number($("input#chkBGT").is(':checked'))) {
                            bg = "transparent";
                        }

                        var sheet = "" +
                            $("#selElement").children(":selected").attr("value") + " { " +
                                " padding: " + String($("#txtPadding").val()) + "px !important; " +
                                " margin: " + String($("#txtMargin").val()) + "px !important; " +
                                " background: " + bg + " !important; " +
                                " border-width: " + String($("#txtBorderWidth").val()) + "px !important; " +
                                " border-style: " + String($("#selBorderStyle").val()) + " !important; " +
                                " border-color: " + String($("#txtBorderColor").val()) + " !important; " +
                                " border-top-left-radius: " + String($("#txtBorderRadius1").val()) + "px !important; " +
                                " border-top-right-radius: " + String($("#txtBorderRadius2").val()) + "px !important; " +
                                " border-bottom-right-radius: " + String($("#txtBorderRadius3").val()) + "px !important; " +
                                " border-bottom-left-radius: " + String($("#txtBorderRadius4").val()) + "px !important; " +
                                ' font-family: "' + String($("#selFont").val()) + '" !important; ' +
                                " color: " + String($("#txtTextColor").val()) + " !important; " +
                                " cursor: " + String($("#selCursor").val()) + " !important; " +
                                " font-size: " + String($("#txtFontSize").val()) + String($("#selSizeUnit").val()) + " !important; " +
                                " box-shadow: " + bs + " !important; " +
                                " text-decoration: " + ud + " " + sd + " !important; " +
                                " font-weight: " + fw + " !important; " +
                                " font-style: " + ia + " !important; " +
                            " } ";

                        $("textarea#JSC" + $("#selElement").children(":selected").attr("id")).text(
                            String($("#txtPadding").val()) + ";" +
                            bg + ";" +
                            String($("#txtBorderWidth").val()) + ";" +
                            String($("#selBorderStyle").val()) + ";" +
                            String($("#txtBorderColor").val()) + ";" +
                            String($("#txtBorderRadius1").val()) + ";" +
                            String($("#txtBorderRadius2").val()) + ";" +
                            String($("#txtBorderRadius3").val()) + ";" +
                            String($("#txtBorderRadius4").val()) + ";" +
                            String($("#selFont").val()) + ";" +
                            String($("#txtTextColor").val()) + ";" +
                            String($("#txtFontSize").val()) + ";" +
                            bs + ";" +
                            ud + ";" +
                            fw + ";" +
                            ia + ";" +
                            String($("#txtMargin").val()) + ";" +
                            String($("#selSizeUnit").val()) + ";" +
                            String($("#selCursor").val()) +
                        "");

                        $("style#CSS-" + $("#selElement").children(":selected").attr("id")).html(".tab-pane " + sheet);
                        $('textarea[name="CSS' + $("#selElement").children(":selected").attr("id") + '"]').text(sheet);
                    });

                    $("button#cmdResetSE").click(function() {
                        if(confirm('저장하지 않은 내용을 모두 잃게 됩니다!')) {
                            $("style#CSS-" + $("#selElement").children(":selected").attr("id")).html("");
                            $('textarea[name="CSS' + $("#selElement").children(":selected").attr("id") + '"]').text("");
                        }
                    });
                });
            </script>

            <ul class="nav nav-tabs">
                <li class=nav-item>
                    <a href=#discuss class="nav-link active">토론의 댓글 래퍼</a>
                    <a href=#article class=nav-link>위키 본문 및 컨트롤</a>
                </li>
            </ul>

            <div class="tab-content bordered">
                <div class="tab-pane active" id=discuss>
                    <div id=res-container>
                        <div class=res-wrapper>
                            <div class="res res-type-normal">
                                <div class="r-head first-author">
                                    <a id=1>#1</a> <a>샘플 발제자</a> <span style="float: right;">1983-04-22 12:45:59</span>
                                </div>
                                <div class=r-body>
                                    샘플 내용
                                </div>
                            </div>
                        </div>
                        <div class=res-wrapper>
                            <div class="res res-type-normal">
                                <div class=r-head>
                                    <a id=2>#2</a> <a>샘플 숨겨진 댓글</a> <span style="float: right;">1983-04-22 12:45:59</span>
                                </div>
                                <div class="r-body r-hidden-body">
                                    [고길동에 의해 숨겨진 글입니다.]
                                </div>
                            </div>
                        </div>
                        <div class=res-wrapper>
                            <div class="res res-type-status">
                                <div class=r-head>
                                    <a id=3>#3</a> <a>샘플 상태 표시 댓글</a> <span style="float: right;">1983-04-22 12:45:59</span>
                                </div>
                                <div class=r-body>
                                    스레드 상태를 <strong>close</strong>로 변경
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class=tab-pane id=article>
                    <div class=wiki-article>
                        <div class=wiki-content>
                            <div class="alert alert-danger">
                                <strong>[오류!]</strong> 오류가 발생했습니다.
                            </div>
                            <div class="alert alert-warning">
                                <strong>[경고!]</strong> 주의하십시오.
                            </div>
                            <div class="alert alert-success">
                                <strong>[주의!]</strong> 한글 MS-DOS 6.20이 성공적으로 설치됐습니다. 시스템을 재시동하십시오.
                            </div>
                            <div class="alert alert-info">
                                Windows XP는 최고의 운영 체제 중 하나입니다. 물론 이 의견은 사람마다 다르겠지만요.
                            </div>

                            <div class=wiki-textbox>
                                글상자 내용
                            </div><br>

                            <input value="글자 입력 상자" type=text class=form-control style="width: 250px; display: block;">

                            <button type=button class="btn btn-secondary" style="display: inline-block;">일반 단추</button>&nbsp;
                            <button type=button class="btn btn-primary" style="display: inline-block;">저장 단추</button>&nbsp;
                            <button type=button class="btn btn-danger" style="display: inline-block;">위험 단추</button>&nbsp;
                            <button type=button class="btn btn-info" style="display: inline-block;">정보 단추</button>&nbsp;
                            <button type=button class="btn btn-secondary disabled" disabled style="display: inline-block;">흐려진 단추</button>&nbsp;

                            <hr>

                            <p>아기공룡 둘리는 1987년의 애니메이션이다. 오프닝과 엔딩의 가사는 같으며 다음과 같다. 2절까지 있다.

                            <div class="wiki-quote table-wiki-quote">
                                요리보고 조리봐도 음~ 알 수 없는 둘리~ 둘리~<br>
                                빙하타고 내려와~ 친-구를 만났지만<br>
                                일억년 전 옛날이 너무나 그리워<br>
                                보-고-픈 엄마찾아 모두 함께 나-가자 하 하~ 하 하~<br>
                                외로운 둘리는 귀여운 아기공룡. 호이~ 호이~ 둘리는<br>
                                초능력 내 친구~<br>

                                <hr>

                                기쁠때도~ 슬플때도~ 우리 곁엔 둘리~ 둘리~<br>
                                오랜세월 흘~러온~~ 둘리와 친구되어~<br>
                                고~향은 다르지만 모두 다 한 마음<br>
                                아득한 엄마나라 우리함께 떠~나~자~ 하하~ 하하~<br>
                                외~로운 둘리는 귀여운 아기공룡. 호이~ 호이~ 둘리는<br>
                                초능력 내 친구~
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <table id=css-config>
                <colgroup>
                    <col style="width: 37.5%;">
                    <col style="width: 15.625%;">
                    <col style="width: 15.625%;">
                    <col style="width: 15.625%;">
                    <col style="width: 15.625%;">
                </colgroup>

                <tbody>
                    <tr>
                        <td>
                            <label>항목:</label>
                            <select id=selElement class=form-control>
                                <option id=0 selected style="font-style: italic;">[항목을 선택하십시오.]</option>
                                <option id=1 value=".r-head">참여자 댓글 머리</option>
                                <option id=2 value=".r-head.first-author">발제자 댓글 머리</option>
                                <option id=3 value=".r-body">댓글 내용</option>
                                <option id=4 value=".r-body.r-hidden-body">숨겨진 댓글 내용</option>
                                <option id=5 value=".res-type-status .r-body">상태 댓글 내용</option>

                                <option id=6 value=".form-control">양식 컨트롤</option>
                                <option id=28 value=".form-control[disabled], .form-control[readonly]">사용불가 양식 컨트롤</option>
                                <option id=24 value=".form-control:focus">활성 양식 컨트롤</option>

                                <option id=7 value=".btn.btn-secondary">단추 표면</option>
                                <option id=8 value=".btn.btn-primary">저장 단추 표면</option>
                                <option id=9 value=".btn.btn-danger">위험성 단추 표면</option>
                                <option id=25 value=".btn.btn-warning">경고성 단추 표면</option>
                                <option id=10 value=".btn.btn-info">링크 단추 표면</option>
                                <option id=11 value=".btn:hover">마우스를 올린 단추</option>
                                <option id=12 value=".btn:active">누른 단추</option>
                                <option id=13 value=".btn[disabled], .btn.disabled">흐려진 단추</option>

                                <option id=14 value=".wiki-quote">인용문</option>
                                <option id=15 value=".wiki-textbox">글상자</option>

                                <option id=26 value="code">한 줄 코드</option>
                                <option id=27 value="pre">소스 코드</option>

                                <option id=16 value=".nav.nav-tabs .nav-link.active">활성 탭</option>
                                <option id=17 value=".nav.nav-tabs .nav-link">비활성 탭</option>

                                <option id=18 value=".wiki-article">위키 본문</option>

                                <option id=19 value=".alert-danger">오류 풍선</option>
                                <option id=20 value=".alert-warning">경고 풍선</option>
                                <option id=21 value=".alert-info">정보 알림 풍선</option>
                                <option id=22 value=".alert-success">성공 알림 풍선</option>

                                <option id=23 value="a">하이퍼링크</option>
                            </select>
                        </td>

                        <td>
                            <label>테두리 굵기: </label><br>
                            <input group=border type=range min=0 max=6 step=1 id=txtBorderWidth class=form-control value=1>
                        </td>

                        <td>
                            <label>배경색: </label><label id=lblChkBGT><input type=checkbox id=chkBGT> 투명</label><br>
                            <input group=color type=color id=txtBgolor class=form-control value=#FFFFFF>
                        </td>

                        <td>
                            <label>테두리 색: </label><br>
                            <input group=border group=border type=color id=txtBorderColor class=form-control value=transparent>
                        </td>

                        <td>
                            <label>둥근 모서리: </label><br>
                            <input group=border type=text id=txtBorderRadius1 style="width: 20%; display: inline-block" min=0 max=25 value=0>
                            <input group=border type=text id=txtBorderRadius2 style="width: 20%; display: inline-block" min=0 max=25 value=0>
                            <input group=border type=text id=txtBorderRadius3 style="width: 20%; display: inline-block" min=0 max=25 value=0>
                            <input group=border type=text id=txtBorderRadius4 style="width: 20%; display: inline-block" min=0 max=25 value=0>
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <label>글꼴 스타일:</label><br>
                            <select group=font id=selFont class=form-control>
                                <option value=dshfbhkdsbha>미설정</option>
                                <option>굴림</option>
                                <option>굴림체</option>
                                <option>돋움</option>
                                <option>돋움체</option>
                                <option>고딕</option>
                                <option>궁서</option>
                                <option>궁서체</option>
                                <option>바탕</option>
                                <option>바탕체</option>
                                <option>명조</option>
                                <option>둥근모꼴 일반체</option>
                                <option>새굴림</option>
                                <option value=IHIYAGI_SYS>이야기체</option>
                                <option value=DOSMyongjo>도스 명조</option>
                                <option value=Sam3KRFont>삼국지 3</option>
                                <option>Fixedsys</option>
                                <option value=System>Windows 3.1</option>
                                <option>Terminal</option>
                                <option>monochrome</option>
                                <option>Consolas</option>
                                <option>Lucinda Console</option>
                                <option>Courier New</option>
                                <option>펜흘림</option>
                                <option>태 나무</option>
                                <option>한양해서</option>
                                <option>문체부 쓰기 정체</option>
                                <option>문체부 쓰기 흘림체</option>
                                <option>문체부 궁체 흘림체</option>
                                <option>Arial</option>
                                <option>Webdings</option>
                                <option>Wingdings</option>
                                <option>Wingdings 2</option>
                                <option>Wingdings 3</option>
                                <option>Impact</option>
                            </select>
                        </td>

                        <td>
                            <label>글꼴 색:</label><br>
                            <input group=font type=color id=txtTextColor class=form-control value=#000000>
                        </td>

                        <td>
                            <label>글꼴 크기:</label><br>
                            <input group=font type=number id=txtFontSize class=form-control value=12>
                            <select id=selSizeUnit style="float: right;">
                                <option value=pt selected>포인트</option>
                                <option value=px>픽셀</option>
                                <option value=rem>가변단위-rem</option>
                                <option value=em>가변단위-em</option>
                            </select>
                        </td>

                        <td>
                            <label group=font id=lblChkBold><input group=font type=checkbox id=chkBold> 굵게</label><br>
                            <label group=font id=lblChkItalic><input group=font type=checkbox id=chkItalic> 기울게</label>
                        </td>

                        <td>
                            <label group=font id=lblChkUnderline><input type=checkbox id=chkUnderline> 밑줄</label><br>
                            <label group=font id=lblChkStrike><input type=checkbox id=chkStrike> 취소선</label>
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <label>테두리 모양: </label><br>
                            <select group=border id=selBorderStyle class=form-control>
                                <option value=solid selected>단색</option>
                                <option value=dotted>점선</option>
                                <option value=dashed>파선</option>
                                <option value=inset>입체 안쪽</option>
                                <option value=outset>입체 바깥쪽</option>
                            </select>
                        </td>

                        <td>
                            <label>안쪽 여백: </label><br>
                            <input group=padding type=range min=0 max=12 step=3 id=txtPadding class=form-control value=9>

                            <label>바깥 여백: </label><br>
                            <input group=margin type=range min=0 max=10 step=1 id=txtMargin class=form-control value=0>
                        </td>

                        <td>
                            <label>그림자 X좌표: </label><br>
                            <input group=shadow type=range min=1 max=7 step=1 id=txtBoxShadowX class=form-control value=1>

                            <label>그림자 Y좌표: </label><br>
                            <input group=shadow type=range min=1 max=7 step=1 id=txtBoxShadowY class=form-control value=1>
                        </td>

                        <td>
                            <label>그림자 흐리기: </label><br>
                            <input group=shadow type=range min=-1 max=5 step=1 id=txtBoxShadow class=form-control value=-1>
                        </td>

                        <td>
                            <label>커서: </label><br>
                            <select group=cursor id=selCursor class=form-control>
                                <option value=default selected>보통 선택</option>
                                <option value=not-allowed>사용불가능</option>
                                <option value=crosshair>정밀도 선택</option>
                                <option value=e-resize>수평 크기 조정</option>
                                <option value=n-resize>수직 크기 조정</option>
                                <option value=move>이동</option>
                                <option value=pointer>연결 선택</option>
                                <option value=wait>사용 중</option>
                                <option value=progress>백그라운드 작업</option>
                                <option value=text>I-빔</option>
                                <option value=cell>셀 선택</option>
                            </select>
                        </td>
                    </tr>
                </tbody>
            </table>

            <div>
                <button type=button id=cmdResetSE class="btn btn-danger">이 항목 초기화</button>

                <button type=button id=cmdCancel onclick="if(confirm('저장하지 않은 내용을 모두 잃게 됩니다!')) location.href = '/member/mypage';" class="btn btn-danger pull-right">취소</button>
                <button type=submit class="btn btn-primary pull-right">적용</button>
            </div>
    '''

    for i in range(1, advCount + 1):
        content += '<textarea style="display: none;" name=CSS' + str(i) + '></textarea>'

        curs.execute("select data from user_set where name = 'advjst" + str(i) + "' and id = ?", [ip_check()])
        try:
            jst = curs.fetchall()[0][0]
        except:
            jst = ''
        content += '<textarea style="display: none;" name=JSC' + str(i) + ' id=JSC' + str(i) + '>' + jst + '</textarea>'

    content += '</form>'

    if flask.request.method == 'POST':
        for i in range(1, advCount + 1):
            cSht = getForm("CSS" + str(i), '') + " "
            cStx = getForm("JSC" + str(i), '') + " "

            curs.execute("delete from user_set where id = ? and name = 'advjst" + str(i) + "'", [ip_check()])
            curs.execute("insert into user_set (id, name, data) values (?, 'advjst" + str(i) + "', ?)", [ip_check(), cStx])
            curs.execute("update user_set set data = ? where id = ? and name = 'advjst" + str(i) + "'", [cStx, ip_check()])

            curs.execute("delete from user_set where id = ? and name = 'advstyle" + str(i) + "'", [ip_check()])
            curs.execute("insert into user_set (id, name, data) values (?, 'advstyle" + str(i) + "', ?)", [ip_check(), cSht])
            curs.execute("update user_set set data = ? where id = ? and name = 'advstyle" + str(i) + "'", [cSht, ip_check()])

            conn.commit()

        return redirect('/member/advanced_style')

    return easy_minify(flask.render_template(skin_check(),
        imp = ['고급 화면 배색', wiki_set(), custom(), other2([0, 0])],
        data = content,
        menu = 0
    ))


