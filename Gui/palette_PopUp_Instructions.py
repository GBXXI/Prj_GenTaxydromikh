# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Gui\ui_files\PopUp_instructions.ui'
#
# Created by: PySide2 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Dialog_Instructions(object):
    def setupUi(self, Dialog_Instructions):
        Dialog_Instructions.setObjectName("Dialog_Instructions")
        Dialog_Instructions.resize(420, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_Instructions)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog_Instructions)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setIndent(-1)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.retranslateUi(Dialog_Instructions)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Instructions)

    def retranslateUi(self, Dialog_Instructions):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Instructions.setWindowTitle(_translate("Dialog_Instructions", "Επεξηγήσεις"))
        self.label.setText(_translate("Dialog_Instructions", "<html>\n"
"\n"
"    <head />\n"
"\n"
"    <body>\n"
"        <ol style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"            <li align=\"justify\"\n"
"                style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\n"
"                Σε περίπτωση που ο κέρσορας στην γραμμή εισαγωγής των voucher <br />βρίσκεται στο μέσο του πεδίου, δεν\n"
"                θα μπορέσει να εισάγει το <br />σκαναρισμένο barcode. Πιέστε το πλήκτρο Home, ώστε να μπορέσετε <br />να\n"
"                σκανάρετε. <br /></li>\n"
"            <li align=\"justify\"\n"
"                style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\n"
"                Το όνομα του αποστολέα γίνεται δεκτό <u>μόνο με ελληνικούς κεφαλαίους</u></li>\n"
"            <p align=\"justify\">χαρακτήρες και πρέπει να είναι της μορφής:</p>\n"
"            <p align=\"justify\">Ο. ΕΠΩΝΥΜΟ </p>\n"
"            <li align=\"justify\"\n"
"                style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\n"
"                Για να γίνει επιτυχώς η αποστολή του e-mail, πρέπει ΟΛΑ τα στοιχεία<br />του πίνακα να είναι\n"
"                συμπληρωμένα.</li>\n"
"        </ol>\n"
"    </body>\n"
"\n"
"</html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_Instructions = QtWidgets.QDialog()
    ui = Ui_Dialog_Instructions()
    ui.setupUi(Dialog_Instructions)
    Dialog_Instructions.show()
    sys.exit(app.exec_())
