from .tool.func import *

def main_error_404_2(conn):
    curs = conn.cursor()

    return re_error('/error/3000')
    
def rtrt_2(conn):
    curs = conn.cursor()

    return redirect('/w/' + wiki_set(2))
    
def notav_2(conn):
    curs = conn.cursor()

    return re_error('/error/3001')