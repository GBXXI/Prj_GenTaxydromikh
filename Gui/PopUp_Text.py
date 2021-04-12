
from PySide2 import QtCore, QtWidgets
from palette_PopUp_Text import Ui_Dialog_Text


class PopUpText(QtWidgets.QDialog):

    def __init__(self, parent=None):
        # --SetUp---------------------------------------------------------------
        super().__init__(parent)
        self.popup = Ui_Dialog_Text()
        self.popup.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
