from .tool.func import *
from flask import Flask, request, render_template

def func_seed_upload_2(conn):
    curs = conn.cursor()

    if ban_check() == 1:
        return re_error('/ban')

    if flask.request.method == 'POST':
        if captcha_post(flask.request.form.get('g-recaptcha-response', '')) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)

        data = flask.request.files['file']
        if not data:
            return re_error('/error/9')

        if int(wiki_set(3)) * 1024 * 1024 < flask.request.content_length and admin_check() != 1:
            return re_error('/error/17')

        value = os.path.splitext(data.filename)[1]
        fnex = os.path.splitext(flask.request.form['document'])[1]
        if not value.upper() in ['.JPEG', '.JPG', '.JFIF', '.JPE', '.GIF', '.PNG', '.WEBP', '.BMP', '.DIB', '.TIF', '.TIFF', '.PCX', '.RLE', '.WDP']:
            return re_error('/error/14')

        if fnex != value:
            return showError(load_lang('file_extension_error'))

        if flask.request.form['document']:
            name = flask.request.form['document']
        else:
            name = '파일:' + data.filename

        if not(re.search('^파일:', name)):
            return showError(load_lang('file_name_error'))

        if getacl(name, 'edit') != 1:
            return showError(re_balloon('/ban', 1, name))

        piece = os.path.splitext(re.sub('^파일:', '', name))
        #if re.search('[^ㄱ-힣0-9a-zA-Z_\- ]', piece[0]):
         #   return re_error('/error/22')

        e_data = sha224(piece[0]) + piece[1]

        curs.execute("select title from data where title = ? COLLATE NOCASE", ['파일:' + name])
        if curs.fetchall():
            return re_error('/error/16')

        curs.execute("select html from html_filter where kind = 'file'")
        db_data = curs.fetchall()
        for i in db_data:
            t_re = re.compile(i[0])
            if t_re.search(name):
                return redirect('/file_filter')

        if flask.request.form["f_cate"] == 'add':
            curs.execute("select data from data where title = ?", ['분류:파일/' + flask.request.form["custom_category"]])
            if curs.fetchall():
                return showError(load_lang('file_category_already_exists'))
            else:
                cateName = flask.request.form["custom_category"]
                if re.search("^\s", cateName) or re.search("\s$", cateName) or len(cateName) < 1:
                    return showError(load_lang('file_category_name_invalid'))
                cateName = '분류:파일/' + cateName
                curs.execute("insert into data (title, data, date) values (?, '[[분류:파일]]', ?)", [cateName, get_time()])
                history_plus(
                    cateName, '[[분류:파일]]',
                    get_time(),
                    ip_check(),
                    '자동 파일 분류 생성',
                    '+9',
                    '새 문서'
                )

        ip = ip_check()

        if flask.request.form['f_lice']:
            lice = flask.request.form['f_lice']
        else:
            lice = '명시되지 않음'
        snd = flask.request.form['log']

        dc = format(request.form['text'])

        if not(re.search('^파일:', name)):
            return re_error('/error/22')

        if os.path.exists(os.path.join(app_var['path_data_image'], e_data)):
            os.remove(os.path.join(app_var['path_data_image'], e_data))

            data.save(os.path.join(app_var['path_data_image'], e_data))
        else:
            data.save(os.path.join(app_var['path_data_image'], e_data))

        curs.execute("insert into data (title, data, date) values (?, ?, ?)", [name, dc, get_time()])

        fn = request.files['file'].filename
        if snd == '':
            snd = '파일 ' + fn + '을 올림'
        history_plus(
            name, dc,
            get_time(),
            ip,
            snd,
            '+' + str(len(dc)),
            '새 문서'
        )

        curs.execute("delete from back where link = ?", [name])
        curs.execute("delete from back where title = ? and type = 'no'", [name])

        render_set(
            title = name,
            data = dc,
            num = 1
        )

        conn.commit()

        return redirect("/w/" + name)
    else:
        curs.execute("select title from data sort order by title")
        ctl = curs.fetchall()
        ltl = curs.fetchall()
        licelst = ''
        catelst = ''
        for cl in ctl:
            if re.search('^분류:파일/', cl[0]):
                catelst += '<option value="분류:파일/' + cl[0].replace('분류:파일/', '') + '">' + cl[0].replace('분류:파일/', '') + '</option>'
            if re.search('^틀:이미지 라이선스/', cl[0]):
                sel = ''
                if cl[0] == '틀:이미지 라이선스/제한적 이용':
                    sel = 'selected="selected"'
                licelst += '<option value="틀:이미지 라이선스/' + cl[0].replace('틀:이미지 라이선스/', '') + '" ' + sel + '>' + cl[0].replace('틀:이미지 라이선스/', '') + '</option>'
        fileSelectingControl = '''
            <input type="file" name="file" style="display:none;" id="fileInput">
            <div class="row">
                <div class="col-xs-12 col-md-7 form-group">
                    <label class="control-label" for="fakeFileInput">''' + load_lang('selectfile') + '''</label>
                    <div class="input-group">
                        <input type="text" class="form-control" id="fakeFileInput" readonly="">
                        <span class="input-group-btn">
                            <button class="btn btn-secondary" type="button" id="fakeFileButton">Select</button>
                        </span>
                    </div>
                </div>
            </div>
        '''

        if re.search('[;] MSIE \d{1,1}[.]\d{1,5};', flask.request.headers.get('User-Agent')):
            fileSelectingControl = '''
                <input type="file" name="file" id="fileInput">
            '''

        return easy_minify(flask.render_template(skin_check(),
            imp = [load_lang('upload'), wiki_set(), custom(), other2([0, 0])],
            data =  '''
                <form method="post" id="uploadForm" enctype="multipart/form-data" accept-charset="utf8">
                    <div class=form-group>
                    <input type=hidden name=identifier value="namufix 호환용">
                    <input type=hidden name=baserev value="namufix 호환용">
                    ''' + fileSelectingControl + '''
                    <div class="row">
<div class="col-xs-12 col-md-7 form-group">
<label class="control-label" for="fakeFileInput">파일 이름</label>
<input type="text" class="form-control" name="document" id=documentInput value="">
</div>
</div>
                    </div>

                    <div>
                    <textarea name="text" type="text" rows="25" id="textInput" class=form-control>''' + getConfig('upload_template', '') + '''</textarea></div><div class=form-group>
                    <script>
                    $(function() {
                        $('#licenseSelect').change(function() {
                            if($(this).val() == 'custom') {
                                $('#customLicense').show();
                                $('#customLicense').css('display', 'inline-block');
                            } else {
                                $('#customLicense').hide();
                            }
                        });
                    });
                    </script>
                    <label>''' + load_lang('file_license') + '''</label><br>
                    <select id="licenseSelect" name="f_lice" style="width:400px; display: inline-block;" class=form-control>''' + licelst + '''<option value=custom>''' + load_lang('custom') + '''...</option></select>
                    <input type=text placeholder=내용 name=custom_license id=customLicense style="display: none; width: 300px;" class=form-control>
                    <p style="font-weight: boid; color: red;">[주의!] 파일문서의 라이선스(문서 본문)와 올리는 파일의 라이선스는 다릅니다. 파일의 라이선스를 올바르게 지정하였는지 확인하세요.</p></div><div class=form-group>
                    <script>
                    $(function() {
                        $('#categorySelect').change(function() {
                            if($(this).val() == 'add') {
                                $('#customCategory').show();
                                $('#customCategory').css('display', 'inline-block');
                            } else {
                                $('#customCategory').hide();
                            }
                        });
                    });
                    </script>
                    <label>''' + load_lang('category') + '''</label><br>
                    <select id="categorySelect" name="f_cate" style="width:400px; display: inline-block;" class=form-control>
                    <option value>선택</option>''' + catelst + '''<option value=add>''' + load_lang('add') + '''...</option>
                    </select>
                    <input type=text name=custom_category id=customCategory style="display: none; width: 300px;" class=form-control placeholder="새 분류 이름">
                    </div>
                    ''' + captcha_get() + '''
                    <div class="form-group">
<label class="control-label" for="licenseSelect">''' + load_lang('loginput') + '''</label>
<input type="text" id="logInput" class="form-control" name="log"><p>''' + getConfig('edit_warning', '') + '''</p>
</div><div class=btns><button class="btn btn-primary" id="uploadBtn" type="submit">''' + load_lang('uploadbtn') + '''</button></div>
                </form>
            ''',
            menu = [['other', load_lang('return')]]
        ))