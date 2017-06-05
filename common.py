# -*- coding:utf-8 -*-
import re
import errno
import os

EXEC_SUCCESS = 0
GET_COMMIT_ERROR = 1
GET_FILE_ERROR = 2
MAKE_DIR_ERROR = 3
EXPORT_FILE_ERROR = 4

ERROR_MAP = {
    EXEC_SUCCESS: "Success",
    GET_COMMIT_ERROR: "Get commit Error",
    GET_FILE_ERROR: "Get File Error",
    MAKE_DIR_ERROR: "Make Save Dir Error",
    EXPORT_FILE_ERROR: "Export File Error",
}

def check_valid_commit(commit_id):
    # commit id只有40个字符
    if len(commit_id) != 40:
        return False

    # 只有字符和数字
    if re.match('^[0-9a-z]+$', commit_id):
        return True
    else:
        return False

def make_dir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def Schedule(a,b,c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print '%.2f%%' % per
