from .tool.func import *

def main_other_2(conn):
    curs = conn.cursor()

    return easy_minify(flask.render_template(skin_check(),
        imp = ['특수 기능', wiki_set(), custom(), other2([0, 0])],
        data = '''
            <h2>기여 내역</h2>
            <ul>
            <li><a href="/contribution/document">문서 기여 목록</a></li>
            <li><a href="/contribution/discuss">토론 기여 목록</a></li>
            </ul>
            <br>
            <h2>문서 분류</h2>
            <ul>
                <li><a href="/AdminList">''' + load_lang('admin_list') + '''</a></li>
                <li><a href="/OngoingDiscussions">''' + load_lang('open_discussion_list') + '''</a></li>
                <li><a href="/TitleIndex">''' + load_lang('all_document_list') + '''</a></li>
                <li><a href="/NeededPages">작성이 필요한 문서</a></li>
                <li><a href="/OrphanedPages">고립된 문서</a></li>
                <li><a href="/UncategorizedPages">분류가 없는 문서</a></li>
                <li><a href="/OldPages">오래된 문서</a></li>
                <li><a href="/LongestPages">내용이 긴 문서</a></li>
                <li><a href="/ShortestPages">내용이 짧은 문서</a></li>
                <li><a href="/RandomPage">RandomPage</a></li>
                <li><a href="/BlockHistory">''' + load_lang('recent_ban') + '''</a></li>
                <li><a href="/UserList">''' + load_lang('member_list') + '''</a></li>
            </ul>
            <br>
            <h2>''' + load_lang('other') + '''</h2>
            <ul>
                <li><a href="/Upload">''' + load_lang('upload') + '''</a></li>
                <li><a href="/manager/10">''' + load_lang('search') + '''</a></li>
                <li><a href="/License">라이선스</a></li>
            </ul>
            <br>
            <h2>''' + load_lang('admin') + ''' 도구</h2>
            <ul>
                <li><a href="/manager/1">''' + load_lang('admin_tool') + '''</a></li>
            </ul>
        ''',
        menu = 0
    ))