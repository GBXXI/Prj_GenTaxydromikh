
import sys

import formText
import win32com.client as client
from PySide2 import QtCore, QtGui, QtWidgets

from palette_MainWindow import Ui_MainWindow
from palette_PopUp_EmptyFields import Ui_Dialog_EmptyFields


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

# ------------------------------------SetUp-------------------------------------
        super().__init__(parent)
        self.mwin = Ui_MainWindow()
        self.mwin.setupUi(self)

        self.createStatusBar()

        # A better solution is to have the emails in an encrypted .csv file and 
            # not hardcoded, but since this project is a tool for limited use, 
            # no special care about efficiency or maintainability is given.
        self.stores = {
            'AEO ERMOU':[''],
            'AEO GLYFADA':[''],
            'AEO GOLDEN':[''],
            'AEO KALAMATA':[''],
            'AEO MALL ATHENS':[''],
            'AEO NG':[''],
            'AEO ONE SALONICA':[''],
            'AEO THESSALONIKI':['']
        }

        self.office_team = [
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
            formText.formBody(
                self.greetings,
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

            self.text_ = formText.formBody(
                self.greetings,
                self.mwin.lineEdit_consNum.text(),
                self.rows,
                self.elements_gen
            )

            self.mwin.textEdit_eMail.setText(self.text_)
        
        # TODO: Create a logger.
        except Exception as e:
            pass

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
                PopUpEmptyFields().destroy()
        
        except Exception as e:
            # TODO: Create a logger.
            pass

class PopUpEmptyFields(QtWidgets.QDialog):
    
    def __init__(self, parent=None):
# ------------------------------------SetUp-------------------------------------
        super().__init__(parent)
        self.popup = Ui_Dialog_EmptyFields()
        self.popup.setupUi(self)


if __name__ == '__main__':
    # Declaring our application
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
