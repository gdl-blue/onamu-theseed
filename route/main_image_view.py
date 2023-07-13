from .tool.func import *

def main_image_view_2(conn, name, app_var):
    curs = conn.cursor()

    return flask.send_from_directory('./' + app_var['path_data_image'], name)