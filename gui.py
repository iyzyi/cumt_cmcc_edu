import func
import sys, re, os
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QApplication, QLabel, QComboBox
from PyQt5.QtGui import QIcon

 
class GUI(QWidget):
     
    def __init__(self):
        super().__init__()
        self.initUI()
         
        
    def initUI(self):     
        

        self.user_txt = QLabel(self)
        self.user_txt.setText('学号')
        self.user_txt.move(40, 24)
        
        self.user = QLineEdit(self)
        self.user.move(100, 20)
        
        
        self.password_txt = QLabel(self)
        self.password_txt.setText('密码')
        self.password_txt.move(40, 54)

        self.password = QLineEdit(self)
        self.password.move(100, 50)
        
        
        self.operator_txt = QLabel(self)
        self.operator_txt.setText('运营商')
        self.operator_txt.move(40, 84)
        
        self.operator = QComboBox(self)
        self.operator.addItem('校园网不行')
        self.operator.addItem('中国移不动')
        self.operator.addItem('中国联不通')
        self.operator.addItem('中国电不信')
        self.operator.move(100, 80)
        
        
        self.status_txt = QLabel(self)
        self.status_txt.setText('状态')
        self.status_txt.move(40, 114)

        self.status = QLabel(self)
        self.status.setText('        ')    #四个字要用八个空格占位
        self.status.move(100, 114)
        
        
        self.btn = QPushButton('登录', self)
        self.btn.move(200, 80)
        self.btn.clicked.connect(self.pass_login)
        
        
        self.btn = QPushButton('注销', self)
        self.btn.move(200, 115)
        self.btn.clicked.connect(self.pass_logout)
        
         
        self.setGeometry(300, 300, 280, 150)
        self.setWindowTitle('CUMT校园网登录')
        self.setWindowIcon(QIcon('cumt.ico'))
        self.show()
        
        
        if os.path.exists('cumt_cmcc_edu.conf'):
            with open('cumt_cmcc_edu.conf','r')as f:
                file = f.read()
            re_param = re.search(r'"user": "(.+?)",\n"password": "(.+?)",\n"operator": "(.*?)"', str(file))
            if re_param and re_param.group(1) and re_param.group(2) and (re_param.group(3) == '' or re_param.group(3)):
                self.user.setText(re_param.group(1))
                self.password.setText(re_param.group(2))
                operators = {
                        '': 0,
                        '%40cmcc': 1,
                        '%40unicom': 2,
                        '%40telecom': 3
                        }
                self.operator.setCurrentIndex(operators[re_param.group(3)])
        

    def mk_conf(self, user, password, operator):
        if not os.path.exists('cumt_cmcc_edu.conf'):
            with open('cumt_cmcc_edu.conf','w')as f:
                file = '"user": "%s",\n"password": "%s",\n"operator": "%s"' % (user, password, operator) 
                f.write(file)
        else:
            with open('cumt_cmcc_edu.conf','r')as f:
                file = f.read()
                re_param = re.search(r'"user": "(.+?)",\n"password": "(.+?)",\n"operator": "(.*?)"', str(file))
                if re_param and re_param.group(1) and re_param.group(2):
                    if not (re_param.group(1) == user and re_param.group(2) == password and re_param.group(3) == operator):
                        with open('cumt_cmcc_edu.conf','w')as f2:
                            file = '"user": "%s",\n"password": "%s",\n"operator": "%s"' % (user, password, operator)
                            f2.write(file)


    def pass_login(self):
        
        self.status.setText('正在登录')
        
        operators = {
                '校园网不行': '',
                '中国移不动': '%40cmcc',
                '中国联不通': '%40unicom',
                '中国电不信': '%40telecom'
                }

        user = self.user.text()
        password = self.password.text()
        operator = operators[self.operator.currentText()]
        
        response = func.login(user, password, operator)
        self.status.setText(response)
        
        self.mk_conf(user, password, operator)

    
    def pass_logout(self):
        self.status.setText('正在注销')
        response = func.logout()
        self.status.setText(response)
        
        
if __name__ == '__main__':
     
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())