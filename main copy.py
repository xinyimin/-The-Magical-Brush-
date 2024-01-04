#coding = 'utf-8'

import sys
import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets
import Ui_interfaceUi
import Ui_loginui

user_now = ''
 
#demo
def buttonClicked(girl):
    girl.textBrowser.append("hello world! This is my first pyQt5 program.")

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(10)
        self.shadow.setYOffset(10)
        self.shadow.setColor(QtGui.QColor(0, 0, 0, 110))
        self.setGraphicsEffect(self.shadow)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui = Ui_loginui.Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda:buttonClicked(self.ui))
        self.ui.pushButton_Register.clicked.connect(lambda:self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_Login.clicked.connect(lambda:self.ui.stackedWidget_2.setCurrentIndex(1))

        # 点击pushButton_L_sure进入MainWindow
        self.ui.pushButton_L_sure.clicked.connect(self.Login_in)
                                               
        self.show()
    
    def Login_in(self):
        # 获取用户名和密码
        username = self.ui.lineEdit_L_account.text()
        password = self.ui.lineEdit_L_password.text()
        # 进行登录验证
        if username == "admin" and password == "123456":
            self.w = MainWindow()
            
            self.close()
        else:
            
            self.ui.lineEdit_L_account.clear()
            self.ui.lineEdit_L_password.clear()
            self.ui.lineEdit_L_account.setFocus()

    

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui = Ui_interfaceUi.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_home.clicked.connect(lambda:self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_my.clicked.connect(lambda:self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_web.clicked.connect(self.go_web)
        self.ui.pushButton_logout.clicked.connect(self.logout)
                                               
        self.show()

    def go_web(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.pushButton_bilibili.clicked.connect(lambda:webbrowser.open('https://www.bilibili.com/'))
        self.ui.pushButton_apple.clicked.connect(lambda:webbrowser.open('https://www.apple.com/'))
        self.ui.pushButton_csdn.clicked.connect(lambda:webbrowser.open('https://www.csdn.net/'))

        
    
    def logout(self):
        global user_now
        self.close()
        self.login = LoginWindow()
        user_now = ""


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = LoginWindow()


   
    sys.exit(app.exec_())
