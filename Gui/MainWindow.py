
import sys
import datetime

# import pywin32
from PySide2 import QtCore, QtGui, QtWidgets

from palette_MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

# ------------------------------------SetUp-------------------------------------
        super().__init__(parent)
        self.mwin = Ui_MainWindow()
        self.mwin.setupUi(self)

# -------------------------------lineEdit_voucher-------------------------------
# -----------------------------------comboBox-----------------------------------
        self.mwin.comboBox.insertItems(0,
            [
                'One Salonica',
                'Mall Athens',
                'Glyfada',
                'Ermou',
                'Aiolou',
                'AEO Kalamata',
                'Golden Hall'
            ]
        )

# ---------------------------------dateTimeEdit--------------------------------- 
        self.mwin.dateTimeEdit.setDate(QtCore.QDate.currentDate())
        self.mwin.dateTimeEdit.setCalendarPopup(True)

if __name__ == '__main__':
    # Declaring our application
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
