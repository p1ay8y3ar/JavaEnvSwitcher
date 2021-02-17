from JavaEnvSwitcher.src.ui import JavaEnvSwitchUI
from PyQt5.QtWidgets import  QApplication
import  sys
from JavaEnvSwitcher.src.exefile import is_admin
from JavaEnvSwitcher.src.exefile.switcher import Switcher

import platform

if __name__ =="__main__":

    if not is_admin():
        sys.exit(0)

    app=QApplication(sys.argv)
    switcher = Switcher()
    UiSet=JavaEnvSwitchUI(switcher)
    UiSet.show()
    sys.exit(app.exec_())