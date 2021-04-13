
import logging
import os
import sqlite3 as lite3
import sys

import formattedText
from db_sqlite3 import DataBase
from PySide2 import QtCore, QtGui, QtWidgets

from Email_CRUD import EmailCRUD
from PopUp_Text import PopUpText
from palette_MainWindow import Ui_MainWindow

if sys.platform.startswith('win32'):
    import win32com.client as client

# ------------------------------MODULARISED LOGGER------------------------------
directory = os.getcwd()
file_handler = logging.FileHandler(f"{directory}/GenikhTaxydromikh.log")

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

log_format = logging.Formatter(
    '%(filename)s '
    '%(asctime)s %(levelname)s\n'
    '%(funcName)s\n%(message)s\n'
)

file_handler.setFormatter(log_format)

log.addHandler(file_handler)


# -------------------------------Main Window GUI--------------------------------
class MainWindow(QtWidgets.QMainWindow):

    db_file = (f"{directory}/GenikhTaxydromikh.db")

    def __init__(self, parent=None):

        # --SetUp-------------------------------------------------------------------
        super().__init__(parent)
        self.mwin = Ui_MainWindow()
        self.mwin.setupUi(self)

        self.createStatusBar()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.carbon_copy = []
        self.recipients = {}

    # --DataBase Setup----------------------------------------------------------
        if not os.path.exists(MainWindow.db_file):
                DataBase(MainWindow.db_file).setup()

                # os.remove(MainWindow.db_file)

                # no_db = PopUpText()
                # no_db.setWindowTitle("No Database")
                # no_db.popup.label.setTextFormat(QtCore.Qt.RichText)
                # no_db.popup.label.setText(formattedText.No_db)
                # no_db.setModal(True)
                # no_db.exec_()
        else:
            self.email_recievers()

    # --TabOrder----------------------------------------------------------------
        self.mwin.lineEdit_consNum.setFocus()
        self.setTabOrder(self.mwin.lineEdit_consNum,
                         self.mwin.comboBox_recievingStore)
        self.setTabOrder(self.mwin.comboBox_recievingStore,
                         self.mwin.lineEdit_senderName)
        self.setTabOrder(self.mwin.lineEdit_senderName,
                         self.mwin.lineEdit_voucher)
        self.setTabOrder(self.mwin.lineEdit_voucher, self.mwin.pushButton_send)
        self.setTabOrder(self.mwin.pushButton_send,
                         self.mwin.pushButton_cancel)

    # --actionExit--------------------------------------------------------------
        self.mwin.actionExit.triggered.connect(self.close)
        self.mwin.actionExit.setShortcut(QtGui.QKeySequence('Alt+F4'))
        self.mwin.actionExit.setShortcut(QtGui.QKeySequence('Ctrl+Q'))

    # --menuEmails--------------------------------------------------------------
        self.mwin.actionPreview.triggered.connect(self.emailCRUD)
        self.mwin.actionPreview.setShortcut(QtGui.QKeySequence('Ctrl+S'))
        self.mwin.actionInsert.triggered.connect(self.emailCRUD)
        self.mwin.actionInsert.setShortcut(QtGui.QKeySequence('Ctrl+I'))
        self.mwin.actionDelete.triggered.connect(self.emailCRUD)
        self.mwin.actionDelete.setShortcut(QtGui.QKeySequence('Ctrl+D'))

    # --actionInstructions------------------------------------------------------
        self.mwin.actionInstructions.triggered.connect(self.help_text)
        self.mwin.actionInstructions.setShortcut(QtGui.QKeySequence('F1'))

    # --lineEdit_consNum--------------------------------------------------------
        self.mwin.lineEdit_consNum.setMaxLength(4)
        self.mwin.lineEdit_consNum.setValidator(QtGui.QIntValidator())

    # --comboBox_recievingStore-------------------------------------------------
        self.mwin.comboBox_recievingStore.insertItem(0, '')
        self.mwin.comboBox_recievingStore.insertItems(1,
            (f'{store}' for store in self.recipients.keys())
        )

    # --dateTimeEdit_date-------------------------------------------------------
        self.mwin.dateTimeEdit_date.setDate(QtCore.QDate.currentDate())
        self.mwin.dateTimeEdit_date.setTime(QtCore.QTime.currentTime())
        self.mwin.dateTimeEdit_date.setCalendarPopup(True)

        self.greetings = ['Καλημέρα', 'Καλησπέρα']
        if QtCore.QTime.currentTime().hour() < 12:
            self.greetings = self.greetings[0]
        else:
            self.greetings = self.greetings[1]

    # --lineEdit_senderName-----------------------------------------------------
        self.mwin.lineEdit_senderName.setValidator(
            QtGui.QRegExpValidator(r'[Α-Ω]\.?\s[Α-Ω]*'))
        self.mwin.lineEdit_senderName.setCompleter(
            QtWidgets.QCompleter(
                [
                    'Γ. Μπιτσώνης',
                    'Σ. Κάτσαρη',
                    'Χ. Λόγγρος',
                    'Σ. Κουκέας'
                ]
            )
        )

    # --lineEdit_voucher--------------------------------------------------------
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
        self.mwin.lineEdit_voucher.editingFinished.connect(self.tb_show)
        self.mwin.lineEdit_voucher.editingFinished.connect(self.entries)

    # --tableWidget_voucher-----------------------------------------------------
        self.mwin.tableWidget_voucher.setColumnCount(1)
        self.mwin.tableWidget_voucher.setHorizontalHeaderLabels(
            [
                'Voucher #'
            ]
        )

    # --pushButton_delete-------------------------------------------------------
        self.mwin.pushButton_delete.clicked.connect(self.deleteItem)
        self.mwin.pushButton_delete.clicked.connect(self.entries)

    # --textEdit_eMail----------------------------------------------------------
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

    # --pushButton_send---------------------------------------------------------
        self.mwin.pushButton_send.clicked.connect(self.e_mail)
        self.mwin.pushButton_send.setDefault(True)

    # --pushButton_cancel-------------------------------------------------------
        self.mwin.pushButton_cancel.clicked.connect(self.close)
        self.mwin.pushButton_cancel.setAutoDefault(True)

# -----------------------------------Methods------------------------------------

    def email_recievers(self):

        with DataBase(MainWindow.db_file) as db:
            table_recipients = db.table('Recipients')
            table_carbon_copy = db.table('CarbonCopy')

            self.carbon_copy = [email[0]
                                for email in table_carbon_copy.select_emails()]

            self.recipients = {header[0]: [email[0] for email in table_recipients.select_emails(header[0])]
                           for header in table_recipients.select_headers}

    def help_text(self):
        help_ = PopUpText()
        help_.setWindowTitle("Επεξηγήσεις")
        help_.popup.label.setText(formattedText.Help)
        help_.setModal(True)
        help_.exec_()

    def emailCRUD(self):
        crud = EmailCRUD(
            DataBase(MainWindow.db_file),
            self.sender().objectName()
        )

        crud.exec_()

    # Self-indulgence Function.
    def createStatusBar(self):

        self.myStatus = QtWidgets.QStatusBar()
        self.myStatus.showMessage('Created by GBXXI')
        self.setStatusBar(self.myStatus)

    def tb_show(self):

        self.mwin.tableWidget_voucher.insertRow(0)

        self.rows = self.mwin.tableWidget_voucher.rowCount()
        item = self.mwin.lineEdit_voucher.displayText()

        self.mwin.tableWidget_voucher.setItem(0, 0,
            QtWidgets.QTableWidgetItem(f'{item}')
        )

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
            log.warning(err)

    def e_mail(self):

        try:
            if (
                self.mwin.lineEdit_consNum.text() != '' and
                self.mwin.lineEdit_senderName.text() != '' and
                self.mwin.comboBox_recievingStore.currentText() != '' and
                self.rows > 0
            ):
                recipients = ('; ').join(
                    self.recipients[self.mwin.comboBox_recievingStore.currentText()]
                )
                carbon_copy = ('; ').join(self.carbon_copy)

                try:
                    outlook = client.GetActiveObject("Outlook.Application")
                except:
                    outlook = client.Dispatch("Outlook.Application")

                message = outlook.CreateItem(0)
                message.Display()
                message.To = recipients
                message.CC = carbon_copy

                message.Subject = f"""Άμεση Αποστολή {
                    self.mwin.comboBox_recievingStore.currentText()
                }"""

                message.HTMLBody = f"{self.text_}"
                # message.Send()
            else:
                incoplete = PopUpText()
                incoplete.setModal(True)
                incoplete.setWindowTitle("Κενά Πεδία")
                incoplete.popup.label.setText(
                    formattedText.EmptyFields)
                incoplete.exec_()

        except OSError as err:
            log.warning(err)

            no_windows = PopUpText()
            no_windows.setWindowTitle("No Windows OS")
            no_windows.popup.label.setText(formattedText.Os)
            no_windows.exec_()
            self.close()

        except Exception as err:
            log.warning(err)


def main():
    # Declaring our application
    app = QtWidgets.QApplication(sys.argv)


# ---------------------------------Window Style---------------------------------
    app.setStyle('fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(79, 79, 79))
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


if __name__ == '__main__':
    main()
