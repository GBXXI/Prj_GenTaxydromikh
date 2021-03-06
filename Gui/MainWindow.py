
import logging
import os
import sys

import formattedText
from PySide2 import QtCore, QtGui, QtWidgets

from palette_MainWindow import Ui_MainWindow
from palette_PopUp_EmptyFields import Ui_Dialog_EmptyFields
from palette_PopUp_Instructions import Ui_Dialog_Instructions

# ------------------------------MODULARISED LOGGER------------------------------
directory = os.getcwd()

if sys.platform.startswith('win32'):
    import win32com.client as client
    
    file_handler = logging.FileHandler(directory+r"\GenikhTaxydromikh.log")

else:
    file_handler = logging.FileHandler(directory+"/GenikhTaxydromikh.log")
    
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

log_format = logging.Formatter('%(asctime)s %(levelname)s\n%(message)s\n')

file_handler.setFormatter(log_format)

log.addHandler(file_handler)

# ------------------------------------------------------------------------------

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

# ------------------------------------SetUp-------------------------------------
        super().__init__(parent)
        self.mwin = Ui_MainWindow()
        self.mwin.setupUi(self)

        self.createStatusBar()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)


        # A better solution is to have the emails in an encrypted .csv file and 
            # not hardcoded, but since this project is a tool for limited use, 
            # no special care about efficiency or maintainability is given.
        self.stores = {
            'AEO ERMOU':['', ''],
            'AEO GLYFADA':['', ''],
            'AEO GOLDEN':['', ''],
            'AEO KALAMATA':['', ''],
            'AEO MALL ATHENS':['', ''],
            'AEO NG':['', ''],
            'AEO ONE SALONICA':['', ''],
            'AEO THESSALONIKI':['', '']
        }

        self.office_team = [
            '',
            ''
        ]

# -----------------------------------TabOrder-----------------------------------
        self.mwin.lineEdit_consNum.setFocus()
        self.setTabOrder(self.mwin.lineEdit_consNum, self.mwin.comboBox_recievingStore)
        self.setTabOrder(self.mwin.comboBox_recievingStore, self.mwin.lineEdit_senderName)
        self.setTabOrder(self.mwin.lineEdit_senderName, self.mwin.lineEdit_voucher)
        self.setTabOrder(self.mwin.lineEdit_voucher, self.mwin.pushButton_send)
        self.setTabOrder(self.mwin.pushButton_send, self.mwin.pushButton_cancel)

# ----------------------------------actionExit----------------------------------
        self.mwin.actionExit.triggered.connect(self.close)
        self.mwin.actionExit.setShortcut(QtGui.QKeySequence('Alt+F4'))
        
# ------------------------------actionInstructions------------------------------
        self.mwin.actionInstructions.triggered.connect(self.helpText_)
        self.mwin.actionInstructions.setShortcut(QtGui.QKeySequence('F1'))

# -------------------------------lineEdit_consNum-------------------------------
        self.mwin.lineEdit_consNum.setMaxLength(4)
        self.mwin.lineEdit_consNum.setValidator(QtGui.QIntValidator())

# ---------------------------comboBox_recievingStore----------------------------
        self.mwin.comboBox_recievingStore.insertItem(0, '')
        self.mwin.comboBox_recievingStore.insertItems(1,
            [f'{store}' for store in self.stores.keys()]
        )

# ------------------------------dateTimeEdit_date-------------------------------
        self.mwin.dateTimeEdit_date.setDate(QtCore.QDate.currentDate())
        self.mwin.dateTimeEdit_date.setTime(QtCore.QTime.currentTime())
        self.mwin.dateTimeEdit_date.setCalendarPopup(True)

        self.greetings = ['Καλημέρα', 'Καλησπέρα']
        if QtCore.QTime.currentTime().hour() < 12:
            self.greetings = self.greetings[0]
        else:
            self.greetings = self.greetings[1]

# -----------------------------lineEdit_senderName------------------------------
        self.mwin.lineEdit_senderName.setValidator(QtGui.QRegExpValidator(r'[Α-Ω]\.?\s[Α-Ω]*'))

# -------------------------------lineEdit_voucher-------------------------------
        # In this lineEdit widget, there is no use of the QIntValidator as the
            # widget above, because a bug causes the widget to surpass the 
            # maximum allowed characters length, which results for an invalid 
            # input. Thus it is considered more intuitive for the user to deal 
            # with the following bug, which is easily bypassed by just pressing 
            # the 'home' button, on the keyboard.
        self.mwin.lineEdit_voucher.setInputMask('9999999999')
        # BUG: Find why the cursor is not placed on the beginning when selected
        # by clicking on the widget.
        self.mwin.lineEdit_voucher.setCursorPosition(0)
        self.mwin.lineEdit_voucher.setMaxLength(10)
        self.mwin.lineEdit_voucher.setClearButtonEnabled(True)
        self.mwin.lineEdit_voucher.editingFinished.connect(self.tb_input)
        self.mwin.lineEdit_voucher.editingFinished.connect(self.entries)

# -----------------------------tableWidget_voucher------------------------------
        self.mwin.tableWidget_voucher.setColumnCount(1)
        self.mwin.tableWidget_voucher.setHorizontalHeaderLabels(
            [
                'Voucher #'
            ]
        )

# ------------------------------pushButton_delete-------------------------------
        self.mwin.pushButton_delete.clicked.connect(self.deleteItem)
        self.mwin.pushButton_delete.clicked.connect(self.entries)

# --------------------------------textEdit_eMail--------------------------------
        self.mwin.textEdit_eMail.setReadOnly(True)
        self.mwin.textEdit_eMail.setText(
            formattedText.formattedBody(
                self.greetings,
                '####',
                '####',
                '####',
                '####'
            )
        )

# -------------------------------pushButton_send--------------------------------
        self.mwin.pushButton_send.clicked.connect(self.e_mail)
        self.mwin.pushButton_send.setDefault(True)

# ------------------------------pushButton_cancel-------------------------------
        self.mwin.pushButton_cancel.clicked.connect(self.close)
        self.mwin.pushButton_cancel.setAutoDefault(True)
        
# -----------------------------------Methods------------------------------------    

    def helpText_(self):

        PopUpInstructions().setModal(True)
        PopUpInstructions().exec_()

    # Self-indulgence Function.
    def createStatusBar(self):
        
        self.myStatus = QtWidgets.QStatusBar()
        self.myStatus.showMessage('Created by GBXXI')
        self.setStatusBar(self.myStatus)
   
    def tb_input(self):
        
        self.mwin.tableWidget_voucher.insertRow(0)
        
        self.rows = self.mwin.tableWidget_voucher.rowCount()
        item = self.mwin.lineEdit_voucher.displayText()
        
        self.mwin.tableWidget_voucher.setItem(0, 0, QtWidgets.QTableWidgetItem(
                                                                f'{item}'))
        
        self.mwin.lcdNumber_boxes.display(self.rows)

        self.mwin.lineEdit_voucher.clear()     

    def deleteItem(self):

        for item in self.mwin.tableWidget_voucher.selectedIndexes():
            self.mwin.tableWidget_voucher.removeRow(item.row())

        self.rows = self.mwin.tableWidget_voucher.rowCount()
        self.mwin.lcdNumber_boxes.display(self.rows)

    def entries(self):
        
        try:
            self.elements_gen = (
                f'<li>{self.mwin.tableWidget_voucher.item(i, 0).text()}</li>' 
                for i in range(self.rows)
            )

            self.text_ = formattedText.formattedBody(
                self.greetings,
                self.mwin.lineEdit_consNum.text(),
                self.rows,
                self.elements_gen,
                self.mwin.lineEdit_senderName.text()
            )

            self.mwin.textEdit_eMail.setText(self.text_)
        
        except Exception as err:
            log.exception(err)

    def e_mail(self):

        try:        
            if (
                self.mwin.lineEdit_consNum.text() != '' and
                self.mwin.lineEdit_senderName.text() !='' and
                self.mwin.comboBox_recievingStore.currentText() != '' and
                self.rows > 0
            ):

                recipients = ('; ').join(
                    self.stores[self.mwin.comboBox_recievingStore.currentText()]
                )
                officeTeam = ('; ').join(self.office_team)

                outlook = client.Dispatch("Outlook.Application")
                message = outlook.CreateItem(0)
                message.Display()
                message.To = recipients
                message.CC = officeTeam

                message.Subject = f"""Άμεση Αποστολή {
                    self.mwin.comboBox_recievingStore.currentText()
                }"""

                message.HTMLBody = f"{self.text_}"
                message.Send()
            else:
                PopUpEmptyFields().setModal(True)
                PopUpEmptyFields().exec_()
        
        except Exception as err:
            no_windows = PopUpEmptyFields()
            no_windows.popup.label.setText(formattedText.formattedText_Os)
            log.exception(err)
            no_windows.exec_()
            self.close()


class PopUpEmptyFields(QtWidgets.QDialog):
    
    def __init__(self, parent=None):
# ------------------------------------SetUp-------------------------------------
        super().__init__(parent)
        self.popup = Ui_Dialog_EmptyFields()
        self.popup.setupUi(self)


class PopUpInstructions(QtWidgets.QDialog):

    def __init__(self, parent=None):
# ------------------------------------SetUp-------------------------------------
        super().__init__(parent)
        self.popup = Ui_Dialog_Instructions()
        self.popup.setupUi(self)


if __name__ == '__main__':
    # Declaring our application
    app = QtWidgets.QApplication(sys.argv)

    app.setStyle('fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.black)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
