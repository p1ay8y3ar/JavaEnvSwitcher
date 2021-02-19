import sys
from PyQt5.QtWidgets import QMainWindow,QMessageBox,QFileDialog
from PyQt5.QtCore import QDir

from JavaEnvSwitcher.src.ui.main import Ui_JavaEnvSwitch

class JavaEnvSwitchUI(QMainWindow,Ui_JavaEnvSwitch):
    def __init__(self,switcher):
        QMainWindow.__init__(self)
        Ui_JavaEnvSwitch.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.env_set)
        self.btn_load.clicked.connect(self.load_local_path)
        self.switcher=switcher
        self.set_label_text("当前环境为：" + self.switcher.sys_jdkenv_path())
        self.comboxtext_set(self.switcher.java_install_path())

    def set_label_text(self,labelstr):
        self.label.setText(labelstr)

    def comboxtext_set(self,strlist):
        self.comboBox.addItems(strlist)


    def load_local_path(self):
        '''
        槽函数
        :return:
        '''
        tmp = []
        filepath =QFileDialog.getExistingDirectory(self.centralwidget,"Choose JDK local path")

        if filepath=="":return None
        filepath=QDir.toNativeSeparators(filepath)
        tmp.append(filepath)
        self.comboxtext_set(tmp)


    def env_set(self):
        current =self.comboBox.currentText() #获取当前内容
        path=current
        if self.switcher.set_new_env(path):
            self.set_label_text("当前环境为：" + self.switcher.sys_jdkenv_path())
            QMessageBox.information(self,"Set Success","设置成功，已经生效")
        else:
            QMessageBox.information(self, "Set Failed", "设置失败，请检查路径")


