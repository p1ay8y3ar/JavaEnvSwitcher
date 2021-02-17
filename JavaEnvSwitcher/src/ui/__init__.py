import sys
from PyQt5.QtWidgets import QMainWindow,QMessageBox
from JavaEnvSwitcher.src.ui.main import Ui_JavaEnvSwitch

class JavaEnvSwitchUI(QMainWindow,Ui_JavaEnvSwitch):
    def __init__(self,switcher):
        QMainWindow.__init__(self)
        Ui_JavaEnvSwitch.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.env_set)
        self.switcher=switcher
        self.set_label_text("当前环境为：" + self.switcher.sys_jdkenv_path())
        self.comboxtext_set(self.switcher.java_install_path())

    def set_label_text(self,labelstr):
        self.label.setText(labelstr)

    def comboxtext_set(self,strlist):
        self.comboBox.addItems(strlist)


    def env_set(self):
        current =self.comboBox.currentText() #获取当前内容
        path=current
        if self.switcher.set_new_env(path):
            self.set_label_text("当前环境为：" + self.switcher.sys_jdkenv_path())
            QMessageBox.information(self,"Set Success","设置成功，已经生效")



