# -*- coding:utf-8 -*-
from PyQt4 import QtCore
from export_file import do_export
import time

class HandlerThread(QtCore.QThread):
    overSignal = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(HandlerThread, self).__init__(parent)

    def set_para(self, begin_commit, end_commit, local_git_path, save_path, check_status):
        self.begin_commit = begin_commit
        self.end_commit = end_commit
        self.local_git_path = local_git_path
        self.save_path = save_path
        self.check_status = check_status

    def run(self):
        ret1 = do_export(self.begin_commit,
                        self.end_commit,
                        self.local_git_path,
                        self.save_path,
                        self.check_status)

        self.overSignal.emit([ret1,])


class ProgressThread(QtCore.QThread):
    overSignal = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(ProgressThread, self).__init__(parent)

    def run(self):
        while True:
            time.sleep(1)
            self.overSignal.emit([1,])
