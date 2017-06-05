# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from log import *
from common import *
from export_file import do_export
import sys
import os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(439, 325)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 91, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 91, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(110, 30, 211, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(110, 70, 211, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(330, 30, 91, 21))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 130, 91, 31))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_3 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(110, 140, 211, 20))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(340, 140, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 170, 91, 31))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.lineEdit_4 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(110, 180, 211, 20))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(340, 180, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(150, 240, 101, 41))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 439, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        QtCore.QObject.connect(self.pushButton,   QtCore.SIGNAL(_fromUtf8("clicked()")), self.clicked_button1)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clicked_button2)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clicked_button3)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("clicked()")), self.check_button)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "开始的commit：", None))
        self.label_2.setText(_translate("MainWindow", "结束的commit：", None))
        self.checkBox.setText(_translate("MainWindow", "next commit", None))
        self.label_3.setText(_translate("MainWindow", "git库的地址：", None))
        self.pushButton.setText(_translate("MainWindow", "选择", None))
        self.label_4.setText(_translate("MainWindow", "保存位置：", None))
        self.pushButton_2.setText(_translate("MainWindow", "选择", None))
        self.pushButton_3.setText(_translate("MainWindow", "导出文件", None))

    def check_button(self):
        if self.checkBox.isChecked():
            self.lineEdit_2.setReadOnly(True)
            self.lineEdit_2.setStyleSheet("background-color:gray")
        else:
            self.lineEdit_2.setReadOnly(False)
            self.lineEdit_2.setStyleSheet("background-color:white")

    def clicked_button1(self):
        tmpDir = QtGui.QFileDialog.getExistingDirectory()
        self.lineEdit_3.setText(tmpDir)

    def clicked_button2(self):
        tmpDir = QtGui.QFileDialog.getExistingDirectory()
        self.lineEdit_4.setText(tmpDir)

    def clicked_button3(self):
        begin_commit = str(self.lineEdit.text())
        end_commit = str(self.lineEdit_2.text())
        local_git_path = str(self.lineEdit_3.text())
        save_path = str(self.lineEdit_4.text())
        check_status = self.checkBox.isChecked()

        if not check_valid_commit(begin_commit):
            self.show_msg("commit id %s is not valid" % begin_commit)
            return

        if not check_status and not check_valid_commit(end_commit):
            self.show_msg("commit id %s is not valid" % end_commit)
            return

        if not os.path.exists(local_git_path):
            self.show_msg("local_git_path %s is not valid" % local_git_path)
            return

        if not os.path.exists(save_path):
            self.show_msg("save_path %s is not valid" % save_path)
            return

        ret = do_export(begin_commit, end_commit, local_git_path, save_path, check_status)
        if ret != EXEC_SUCCESS:
            if ERROR_MAP.has_key(ret):
                self.show_msg("do_export not success because of %s" % ERROR_MAP[ret])
            else:
                self.show_msg("do_export not success because of unknown error")

    def show_msg(self, msg):
        msg_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Alert", u"导出结果为:%s" % msg)
        msg_box.exec_()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(form)
    form.show()
    sys.exit(app.exec_())
