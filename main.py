import install_ui
import reg_ui
import auth_ui
import main_ui
import install_ui

import patoolib.programs
import patoolib.programs.rar
from PyQt5 import QtCore, QtGui, QtWidgets

import auth_reg
import launcher
import simple_calc
import db_helper
import cfg
from cfg import MYSQL_IP, MYSQL_PORT, DATABASE, MYSQL_PASS, MYSQL_USER
import threading
import sys

class MainWindow(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    install_signal = QtCore.pyqtSignal(str, name='install_signal')
    db = db_helper.dbClient(MYSQL_IP, MYSQL_PORT, DATABASE,  MYSQL_USER, MYSQL_PASS)
    def __init__(self, username, permissions, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = main_ui.Ui_MainWindow()
        self.setupUi(self)
        self.username = username
        self.permissions = permissions
        self.apps = []
        self.install_window = InstallWindow()

        self.install_signal.connect(self._installed, QtCore.Qt.QueuedConnection)
        self.pushButton.clicked.connect(lambda checked, button=self.pushButton.text() : self._lineEdit_change(button))
        self.pushButton_2.clicked.connect(lambda checked, button=self.pushButton_2.text() : self._lineEdit_change(button))
        self.pushButton_3.clicked.connect(
            lambda checked, button=self.pushButton_3.text(): self._lineEdit_change(button))
        self.pushButton_4.clicked.connect(
            lambda checked, button=self.pushButton_4.text(): self._lineEdit_change(button))
        self.pushButton_5.clicked.connect(lambda checked, button=self.pushButton_5.text() : self._lineEdit_change(button))
        self.pushButton_6.clicked.connect(
            lambda checked, button=self.pushButton_6.text(): self._lineEdit_change(button))
        self.pushButton_7.clicked.connect(
            lambda checked, button=self.pushButton_7.text(): self._lineEdit_change(button))
        self.pushButton_8.clicked.connect(
            lambda checked, button=self.pushButton_8.text(): self._lineEdit_change(button))
        self.pushButton_9.clicked.connect(
            lambda checked, button=self.pushButton_9.text(): self._lineEdit_change(button))
        self.pushButton_10.clicked.connect(
            lambda checked, button=self.pushButton_10.text(): self._lineEdit_change(button))
        self.pushButton_11.clicked.connect(
            lambda checked, button=self.pushButton_11.text(): self._lineEdit_change(button))
        self.pushButton_12.clicked.connect(
            lambda checked, button=self.pushButton_12.text(): self._lineEdit_change(button))
        self.pushButton_13.clicked.connect(
            lambda checked, button=self.pushButton_13.text(): self._lineEdit_change(button))
        self.pushButton_14.clicked.connect(
            lambda checked, button=self.pushButton_14.text(): self._lineEdit_change(button))
        self.pushButton_15.clicked.connect(
            lambda checked, button=self.pushButton_15.text(): self._lineEdit_change(button))

        self.pushButton_18.clicked.connect(self._reinstall_handler)
        self.pushButton_18.setEnabled(False)
        self.pushButton_16.setEnabled(False)
        self.pushButton_16.setText('Выберите бизнес-приложение')
        self.label_3.setText("Пользователь: " + username)
        self.pushButton_17.clicked.connect(self._reload)
        self._set_app_list()

        if self.apps:
            self.listWidget.clicked.connect(self._update_button_text)
            self.pushButton_16.clicked.connect(self._start_handler)

        self.button_state_flag = True # кнопка в состоянии "Запустить"

    def _reload(self):
        lines = []
        lines = self.db.get_table(lines)
        self.tableWidget.setRowCount(len(lines))
        j = 0
        lines.reverse()
        for i in lines:
            self.tableWidget.setItem(j, 0, QtWidgets.QTableWidgetItem(i[0]))
            self.tableWidget.setItem(j, 1, QtWidgets.QTableWidgetItem(i[1]))
            self.tableWidget.setItem(j, 2, QtWidgets.QTableWidgetItem(str(i[3])))
            self.tableWidget.setItem(j, 3, QtWidgets.QTableWidgetItem(i[2]))
            self.tableWidget.setItem(j, 4, QtWidgets.QTableWidgetItem(str(i[4])))
            self.tableWidget.setItem(j, 5, QtWidgets.QTableWidgetItem(str(i[5])))
            j = j + 1
        self.tableWidget.resizeColumnsToContents()

    def _reinstall_handler(self):
        self.install_window.show()
        selected = self.listWidget.currentRow()
        selected_app = self.apps[selected]
        threading.Thread(target=launcher.install, args=(selected_app, self.install_signal)).start()

    def _lineEdit_change(self, button):
        now_text = self.lineEdit.text()
        text_split = now_text.split()
        if '=' in now_text.split():
            self.lineEdit.setText(text_split[4])
        elif button == 'C':
            self.lineEdit.setText('')
        elif button in '+-*/':
            set_text = now_text + ' ' + button + ' '
            self.lineEdit.setText(set_text)
        else:
            if button == '=':
                operation = simple_calc.operation(now_text)
                result = operation.__str__()
                self.lineEdit.setText(result)
                operation = result.split(' ')
                self.db.add_log_line_math(self.username, operation)
            else:
                self.lineEdit.setText(now_text + button)

    def _set_app_list(self):
        if self.permissions == '':
            appname = 'Обратитесь к администратору информационной'
            self.listWidget.addItem(QtWidgets.QListWidgetItem(appname))
            appname = 'системы для получения прав доступа к'
            self.listWidget.addItem(QtWidgets.QListWidgetItem(appname))
            appname = 'встроенным бизнес-приложениями'
            self.listWidget.addItem(QtWidgets.QListWidgetItem(appname))
        else:
            for i in self.permissions:
                self.apps.append(i)
                appname = cfg.app_names.get(i)
                self.listWidget.addItem(QtWidgets.QListWidgetItem(appname))

    def _update_button_text(self):
        self.pushButton_16.setEnabled(True)
        selected = self.listWidget.currentRow()
        selected_app = self.apps[selected]
        if launcher.is_app_installed(selected_app):
            self.pushButton_18.setEnabled(True)
            self.pushButton_16.setText('Запустить')
            self.button_state_flag = True
        else:
            self.pushButton_18.setEnabled(False)
            self.pushButton_16.setText('Установить')
            self.button_state_flag = False

    def _start_handler(self):
        if self.button_state_flag:
            selected = self.listWidget.currentRow()
            selected_app = self.apps[selected]
            threading.Thread(target= launcher.launch, args=(selected_app, self.username,)).start()
        else:
            self.install_window.show()
            selected = self.listWidget.currentRow()
            selected_app = self.apps[selected]
            threading.Thread(target= launcher.install, args=(selected_app, self.install_signal)).start()

    def _installed(self):
        self.install_window.close()
        self.pushButton_16.setText('Запустить')
        self.button_state_flag = True

class RegWindow(QtWidgets.QMainWindow, reg_ui.Ui_reg):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = reg_ui.Ui_reg()
        self.setupUi(self)
        self.label_4.setVisible(False)

        self.pushButton.clicked.connect(self._reg)

    def _reg(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        response = auth_reg.reg(username, password)
        if response == 'REGNO':
            self.label_4.setText("Пользователь уже зарегистрирован")
            self.label_4.setVisible(True)
        elif response == 'ERR':
            self.label_4.setText("Проблемы с соединением")
            self.label_4.setVisible(True)
        else:
            self.mainui = MainWindow(username, '')
            threading.Thread(target=self.mainui.show())
            self.close()

class AuthWindow(QtWidgets.QMainWindow, auth_ui.Ui_auth):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = auth_ui.Ui_auth()
        self.setupUi(self)
        self.label.setVisible(False)
        self.pushButton_4.clicked.connect(self._toReg)
        self.pushButton_3.clicked.connect(self._auth)

    def _toReg(self):
        self.Reg = RegWindow()
        self.Reg.show()

    def _auth(self):
        username = self.lineEdit_4.text()
        password = self.lineEdit_3.text()
        permissions = auth_reg.auth(username, password)
        if permissions == 'NOAUTH':
            self.label.setText("Неверный логин или пароль")
            self.label.setVisible(True)
        elif permissions == 'ERR':
            self.label.setText("Проблемы с соединением")
            self.label.setVisible(True)
        else:
            self.mainui = MainWindow(username, permissions)
            threading.Thread(target=self.mainui.show())
            self.close()

class InstallWindow(QtWidgets.QMainWindow, install_ui.Ui_Form):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = install_ui.Ui_Form()
        self.setupUi(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec_())
