from .tool.func import *
from flask import Flask, request, render_template

def func_upload_2(conn):
    curs = conn.cursor()

    if ban_check() == 1:
        return re_error('/ban')
    
    if flask.request.method == 'POST':
        if captcha_post(flask.request.form.get('g-recaptcha-response', '')) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)

        data = flask.request.files.get('f_data', None)
        if not data:
            return re_error('/error/9')

        if int(wiki_set(3)) * 1024 * 1024 < flask.request.content_length:
            return re_error('/error/17')
        
        value = os.path.splitext(data.filename)[1]
        if not value in ['.jpeg', '.jpg', '.gif', '.png', '.webp', '.JPEG', '.JPG', '.GIF', '.PNG', '.WEBP']:
            return re_error('/error/14')
    
        if flask.request.form.get('f_name', None):
            name = flask.request.form.get('f_name', None) + value
        else:
            name = data.filename
        
        piece = os.path.splitext(name)
        if re.search('[^ㄱ-힣0-9a-zA-Z_\- ]', piece[0]):
            return re_error('/error/22')

        e_data = sha224(piece[0]) + piece[1]

        curs.execute("select title from data where title = ?", ['파일:' + name])
        if curs.fetchall():
            return re_error('/error/16')

        curs.execute("select html from html_filter where kind = 'file'")
        db_data = curs.fetchall()
        for i in db_data:
            t_re = re.compile(i[0])
            if t_re.search(name):
                return redirect('/file_filter')
            
        ip = ip_check()

        if flask.request.form.get('f_lice', None):
            lice = flask.request.form.get('f_lice', None)
        else:
            lice = '명시되지 않음'
        snd = flask.request.form.get('send', '')
                
        cate = flask.request.form.get('f_cate', None)
        if cate == 'none':
            return re_error('/error/6001')
            
        dc = format(request.form['f_dat'])
            
        if os.path.exists(os.path.join(app_var['path_data_image'], e_data)):
            os.remove(os.path.join(app_var['path_data_image'], e_data))
            
            data.save(os.path.join(app_var['path_data_image'], e_data))
        else:
            data.save(os.path.join(app_var['path_data_image'], e_data))
        
        curs.execute("insert into data (title, data) values (?, ?)", ['파일:' + name, '[[파일:' + name + ']][br][br][include(' + lice + ')][br][br]' + dc + '[br][br][[' + cate + ']]'])
        curs.execute("insert into acl (title, dec, dis, why, view) values (?, '', '', '', '')", ['파일:' + name])
        fn = request.files['f_data'].filename
        if snd == '':
            snd = '(파일 ' + fn + '을 올림)'
        history_plus(
            '파일:' + name, '[[파일:' + name + ']][br][br]라이선스: ' + lice + '[br][br]' + dc + '[br][br][[' + cate + ']]',
            get_time(), 
            ip, 
            snd,
            '0'
        )
        
        conn.commit()
        
        return redirect('/w/파일:' + name)      
    else:
        curs.execute("select title from data sort order by title")
        ctl = curs.fetchall()
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
    
        return easy_minify(flask.render_template(skin_check(), 
            imp = [load_lang('upload'), wiki_set(), custom(), other2([0, 0])],
            data =  '''
                <form method="post" enctype="multipart/form-data" accept-charset="utf8">
                    파일 선택<br>
                    <input type="file" name="f_data" id="fdb" style="width:547.5px;height:37.5px;padding-top:5px;background:#eceeef"> <br><br>
                    파일 이름<br>
                    <input name="f_name" type="text" style="width:547.5px;height:37.5px;" id="fnm"> 
                    <br><br>
                    <textarea name="f_dat" type="text" rows="25"></textarea>
                    <br><br>
                    라이선스<br>
                    <select name="f_lice" style="width:400px">''' + licelst + '''</select><br><br><p style="font-weight: boid; color: red;">[주의!] 파일문서의 라이선스(문서 본문)와 올리는 파일의 라이선스는 다릅니다. 파일의 라이선스를 올바르게 지정하였는지 확인하세요.</p><br>
                    
                    분류<br>
                    <select name="f_cate" style="width:400px">
                    <option value="none">선택</option>''' + catelst + '''
                        
                    </select>
                    ''' + captcha_get() + '''
                    <br><br><div class="form-group">
<label class="control-label" for="licenseSelect">요약</label>
<input type="text" id="logInput" class="form-control" name="send"><br><br><p>문서 편집을 <strong>저장</strong>하면 당신은 기여한 내용을 <strong>CC-BY-NC-SA 2.0 KR</strong>으로 배포하고 기여한 문서에 대한 하이퍼링크나 URL을 이용하여 저작자 표시를 하는 것으로 충분하다는 데 동의하는 것입니다. 이 <strong>동의는 철회할 수 없습니다.</strong></p><br>
</div><button id="save" type="submit">''' + '''올리기''' + '''</button>
                </form>
            ''',
            menu = [['other', load_lang('return')]]
        ))  