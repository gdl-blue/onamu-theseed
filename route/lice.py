from .tool.func import *

def lice_2(conn):
    curs = conn.cursor()

    try:
        skinLicense = open('./views/' + skin_check(1) + '/license.html', 'r').read()
    except:
        skinLicense = ''

    data = '''
        <h2 style="border:none">openNAMU 3.1.1-stable04 (seed) 버전 7.6.1</h2>
        이 싸이트의 많은 문구들과 기능의 원작: the seed(ACL, IPACL, 권한 부여창, 역사, 토론 모양 등) | openNAMU(이것을 기반으로 개발)<br>
        <a href="https://theseed.io/License">[the seed 라이선스 보기]</a><br><br>
        <a href="https://github.com/2du/openNAMU">[원본 판 오픈나무 소스코드]</a><br><br>
        오픈나무 라이선스
        <pre>
BSD 3-Clause License

Copyright (c) 2017-2019, 2DU
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
        </pre>
        <br><br>
        <h2 style="border:none">사용된 외부 소스</h2>
        <ul>
            <li>Jquery</li>
            <li>theseed.js <a href="//theseed.io/js/theseed.js" target=_blank>[#]</a></li>
            <li>dateformatter.js <a href="//theseed.io/js/dateformatter.js" target=_blank>[#]</a></li>
            <li>jsdifflib <a href="//github.com/wkpark/jsdifflib" target=_blank>[#]</a></li>
        </ul>
        <br><br>''' + skinLicense

    return easy_minify(flask.render_template(skin_check(),
            imp = ['라이선스', wiki_set(), custom(), other2(['', 0])],
            data = data,
            menu = 0
        ))