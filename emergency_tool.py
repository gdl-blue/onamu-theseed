from route.tool.func import *
from route.tool.mark import load_conn2, namumark

all_src = []
for i_data in os.listdir("."):
    f_src = re.search("(.+)\.db$", i_data)
    if f_src:
        all_src += [f_src.groups()[0]]

if len(all_src) == 0:
    exit()
elif len(all_src) > 1:
    db_num = 1

    for i_data in all_src:
        print(str(db_num) + ' : ' + i_data)

    print('Number : ', end = '')    
    db_name = all_src[int(number_check(input())) - 1]
else:
    db_name = all_src[0]

if len(all_src) == 1:
    print('DB\'s name : ' + db_name)

conn = sqlite3.connect(db_name + '.db', check_same_thread = False)
curs = conn.cursor()

load_conn(conn)

print('1. 역링크 초기화')
print('2. 리갭챠 삭제')
print('3. 차단 취소')
print('4. 호스트 변경')
print('5. 포트 변경')
print('6. 기본스킨 변경')
print('7. 비밀번호 변경')
print('8. 버전 초기화')
print('9. 새로운 데이터베이스 만들기')

print('선택: ', end = '')
what_i_do = input()

if what_i_do == '1':
    def parser(data):
        namumark(data[0], data[1], 1)

    curs.execute("delete from back")
    conn.commit()

    curs.execute("select title, data from data")
    data = curs.fetchall()
    num = 0

    for test in data:
        num += 1

        t = threading.Thread(target = parser, args = [test])
        t.start()
        t.join()

        if num % 10 == 0:
            print(num)
elif what_i_do == '2':
    curs.execute("delete from other where name = 'recaptcha'")
    curs.execute("delete from other where name = 'sec_re'")
elif what_i_do == '3':
    print('IP 혹은 유저 이름: ', end = '')
    user_data = input()

    if re.search("^([0-9]{1,3}\.[0-9]{1,3})$", user_data):
        band = 'O'
    else:
        band = ''

        curs.execute("insert into rb (block, end, today, blocker, why, band) values (?, ?, ?, ?, ?, ?)", 
            [user_data, 
            'release', 
            get_time(), 
            'tool:emergency', 
            '', 
            band
        ])
    curs.execute("delete from ban where block = ?", [user_data])
elif what_i_do == '4':
    print('호스트 주소: ', end = '')
    host = input()

    curs.execute("update other set data = ? where name = 'host'", [host])
elif what_i_do == '5':
    print('포트: ', end = '')
    port = int(input())

    curs.execute("update other set data = ? where name = 'port'", [port])
elif what_i_do == '6':
    print('스킨 이름: ', end = '')
    skin = input()

    curs.execute("update other set data = ? where name = 'skin'", [skin])
elif what_i_do == '7':
    print('1. sha256')
    print('2. sha3')
    print('선택 : ', end = '')
    what_i_do = int(input())

    print('사용자 이름: ', end = '')
    user_name = input()

    print('암호: ', end = '')
    user_pw = input()

    if what_i_do == '1':
        hashed = hashlib.sha256(bytes(user_pw, 'utf-8')).hexdigest()
    else:
        if sys.version_info < (3, 6):
            hashed = sha3.sha3_256(bytes(user_pw, 'utf-8')).hexdigest()
        else:
            hashed = hashlib.sha3_256(bytes(user_pw, 'utf-8')).hexdigest()
       
    curs.execute("update user set pw = ? where id = ?", [hashed, user_name])
elif what_i_do == '8':
    curs.execute("update other set data = '00000' where name = 'ver'")
else:
    print('데이터베이스 이름 (기본값 data): ', end = '')
    
    db_name = input()
    if db_name == '':
        db_name = 'data'

    sqlite3.connect(db_name + '.db', check_same_thread = False)

conn.commit()

print('OK')