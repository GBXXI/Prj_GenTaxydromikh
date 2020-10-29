# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Gui\ui_files\PopUp_EmptyFields.ui'
#
# Created by: PySide2 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Dialog_EmptyFields(object):
    def setupUi(self, Dialog_EmptyFields):
        Dialog_EmptyFields.setObjectName("Dialog_EmptyFields")
        Dialog_EmptyFields.resize(400, 300)
        self.label = QtWidgets.QLabel(Dialog_EmptyFields)
        self.label.setGeometry(QtCore.QRect(10, 10, 381, 281))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog_EmptyFields)
        QtCore.QMetaObject.connectSlotsByName(Dialog_EmptyFields)

    def retranslateUi(self, Dialog_EmptyFields):
        _translate = QtCore.QCoreApplication.translate
        Dialog_EmptyFields.setWindowTitle(_translate("Dialog_EmptyFields", "Empty Fields"))
        self.label.setText(_translate("Dialog_EmptyFields", "Υπάρχουν κενά πεδία! \n"
"Παρακαλώ συμπληρώστετα και προσπαθήστε ξανά!"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_EmptyFields = QtWidgets.QDialog()
    ui = Ui_Dialog_EmptyFields()
    ui.setupUi(Dialog_EmptyFields)
    Dialog_EmptyFields.show()
    sys.exit(app.exec_())
