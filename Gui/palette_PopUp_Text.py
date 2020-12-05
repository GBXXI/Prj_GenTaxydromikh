# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Gui\ui_files\PopUp_instructions.ui'
#
# Created by: PySide2 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Dialog_Text(object):
    def setupUi(self, Dialog_Text):
        Dialog_Text.setObjectName("Dialog_Text")
        Dialog_Text.resize(420, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_Text)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog_Text)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setIndent(-1)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.retranslateUi(Dialog_Text)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Text)

    def retranslateUi(self, Dialog_Text):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Text.setWindowTitle(_translate("Dialog_Text", " "))
        self.label.setText(_translate("Dialog_Text", " "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_Text = QtWidgets.QDialog()
    ui = Ui_Dialog_Text()
    ui.setupUi(Dialog_Text)
    Dialog_Text.show()
    sys.exit(app.exec_())
