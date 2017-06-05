# -*- coding:utf-8 -*-
import os
import re
import urllib
from datetime import datetime
from log import debug_log
from common import *

DEFAULT_REMOTE_PATH = "https://raw.githubusercontent.com"
DEFAULT_USER_NAME = "LiXinKing"
DEFAULT_PROJECT_NAME = "login"

REMOTE_PATH = DEFAULT_REMOTE_PATH
USER_NAME = DEFAULT_USER_NAME
PROJECT_NAME = DEFAULT_PROJECT_NAME

def load_config():
    global REMOTE_PATH
    global USER_NAME
    global PROJECT_NAME

    REMOTE_PATH = DEFAULT_REMOTE_PATH
    USER_NAME = DEFAULT_USER_NAME
    PROJECT_NAME = DEFAULT_PROJECT_NAME

    f = open("config.ini")
    for line in f.readlines():
        info_lst = line.split("=")
        if len(info_lst) != 2:
            debug_log("load_config:not = in opt config")
            continue
        if info_lst[0].strip() == "REMOTE_PATH":
            REMOTE_PATH = info_lst[1].strip()
        elif info_lst[0].strip() == "USER_NAME":
            USER_NAME = info_lst[1].strip()
        elif info_lst[0].strip() == "PROJECT_NAME":
            PROJECT_NAME = info_lst[1].strip()
        else:
            debug_log("load_config:Error opt config %s" % info_lst[0])

def download_file(commit, path, local_path):
    ex_path = REMOTE_PATH + "/" + USER_NAME + "/" + PROJECT_NAME
    commit_path = "/" + commit + "/" + path
    local_file_path = local_path + path

    if not make_dir_p(os.path.dirname(local_file_path)):
        debug_log("download_file:make dir %s error" % local_file_path)
        return False

    debug_log("download_file:download path is %s" % (ex_path + commit_path))
    try:
        urllib.urlretrieve(ex_path + commit_path, local_path + path, Schedule)
    except Exception, e:
        debug_log(str(e))
        return False
    return True

def export(commit_lst, save_path, date_tag, file_lst):
    for commit in commit_lst:
        local_file_path = save_path + date_tag + ("/new/" if commit == commit_lst[0] else "/old/")
        debug_log("export:local_file_path is %s" % local_file_path)

        # 拷贝到指定目录去
        for file_name in file_lst:
            debug_log("export:downloading %s..." % file_name)
            if not download_file(commit, file_name, local_file_path):
                return False
    return True

def make_export_dir(save_path, date_tag):
    try:
        #创健目录
        make_dir_p(save_path + date_tag + "/" + "new")
        make_dir_p(save_path + date_tag + "/" + "old")
    except Exception, e:
        debug_log(str(e))
        return False

    return True

def get_real_commit(begin_commit, git_path):
    os.chdir(git_path)
    log_info = os.popen("git log %s -2" % begin_commit).read()
    regex = re.compile("commit (\w*)")
    commit_lst = regex.findall(log_info)
    return commit_lst

def get_export_file(begin_commit, git_path):
    os.chdir(git_path)
    file_info = os.popen("git diff-tree -r --no-commit-id --name-only %s" % begin_commit).readlines()
    file_info = [file_name.strip('\n') for file_name in file_info]
    return file_info

def do_export(begin_commit, end_commit, git_path, save_path, check_status):
    #获取当前目录
    cur_cwd = os.getcwd()

    # 做一下反斜替换
    git_path = git_path.replace("\\",'/')
    save_path = save_path.replace("\\",'/')

    # 读取配置数据
    load_config()

    # 获取真实的commit,end_commit可能没有填写
    if check_status:
        commit_lst = get_real_commit(begin_commit, git_path)
    else:
        commit_lst = [begin_commit, end_commit]

    # 获取要到处的文件列表
    file_lst = get_export_file(begin_commit, git_path)

    #切换会当前路径
    os.chdir(cur_cwd)

    # 对文件和commit做一个校验
    if len(commit_lst) != 2 or not check_valid_commit(commit_lst[0]) or not check_valid_commit(commit_lst[1]):
        return GET_COMMIT_ERROR

    if len(file_lst) == 0:
        return GET_FILE_ERROR

    # 获取时间标记
    date_tag = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    # 创建指定的目录
    if not make_export_dir(save_path, date_tag):
        debug_log("do_export:make dir %s error" % save_path)
        return MAKE_DIR_ERROR

    if not export(commit_lst, save_path, date_tag, file_lst):
        debug_log("do_export:export file error")
        return EXPORT_FILE_ERROR

    return EXEC_SUCCESS
