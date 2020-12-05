
import logging
import os
import sqlite3 as lite3
import sys

import formattedText
from db_sqlite3 import DataBase
from PySide2 import QtCore, QtGui, QtWidgets

from palette_EmailCRUD import Ui_Dialog_EmailCRUD
from palette_MainWindow import Ui_MainWindow
from palette_PopUp_Text import Ui_Dialog_Text

if sys.platform.startswith('win32'):
    import win32com.client as client

# ------------------------------MODULARISED LOGGER------------------------------
directory = os.getcwd()
file_handler = logging.FileHandler(f"{directory}/GenikhTaxydromikh.log")

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

log_format = logging.Formatter('%(asctime)s %(levelname)s\n%(message)s\n')

file_handler.setFormatter(log_format)

log.addHandler(file_handler)

# -----------------------------------SQlite3------------------------------------
db_file = (f"{directory}/GenikhTaxydromikh.db")

# -------------------------------Main Window GUI--------------------------------


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        # --SetUp-------------------------------------------------------------------
        super().__init__(parent)
        self.mwin = Ui_MainWindow()
        self.mwin.setupUi(self)

        self.createStatusBar()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.dbsetup()

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
        self.mwin.actionPreview.setShortcut(QtGui.QKeySequence('Ctrl+D'))
        self.mwin.actionInsert.triggered.connect(self.emailCRUD)
        self.mwin.actionInsert.setShortcut(QtGui.QKeySequence('Ctrl+F'))
        self.mwin.actionDelete.triggered.connect(self.emailCRUD)
        self.mwin.actionDelete.setShortcut(QtGui.QKeySequence('Ctrl+S'))

    # --actionInstructions------------------------------------------------------
        self.mwin.actionInstructions.triggered.connect(self.helpText_)
        self.mwin.actionInstructions.setShortcut(QtGui.QKeySequence('F1'))

    # --lineEdit_consNum--------------------------------------------------------
        self.mwin.lineEdit_consNum.setMaxLength(4)
        self.mwin.lineEdit_consNum.setValidator(QtGui.QIntValidator())

    # --comboBox_recievingStore-------------------------------------------------
        self.mwin.comboBox_recievingStore.insertItem(0, '')
        self.mwin.comboBox_recievingStore.insertItems(1,
                                                      (f'{store}' for store in self.stores.keys(
                                                      ))
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
        self.mwin.lineEdit_voucher.editingFinished.connect(self.tb_input)
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

    def dbsetup(self):

        with DataBase(db_file) as db:
            table_stores = db.table('stores')
            table_office_team = db.table('officeteam')

            self.office_team = [email[0]
                                for email in table_office_team.select_emails()]

            self.stores = {header[0]: [email[0] for email in table_stores.select_emails(header[0])]
                           for header in table_stores.select_headers}

    def helpText_(self):
        help_ = PopUpText()
        help_.setWindowTitle("Επεξηγήσεις")
        help_.popup.label.setText(formattedText.formattedText_Help)
        help_.setModal(True)
        help_.exec_()

    def emailCRUD(self):
        object_name = {
            1: 'actionPreview',
            2: 'actionInsert',
            3: 'actionDelete'
        }
        crud = EmailCRUD()

    # --comboBox_store----------------------------------------------------------
        crud.db_ = DataBase(db_file)
        crud.popup.comboBox_store.insertItem(0, '')
        crud.popup.comboBox_store.insertItems(
            1,
            crud.connection_.show_tables
        )

    # --Cases-------------------------------------------------------------------
        if self.sender().objectName() == object_name[1]:
            for widget in range(crud.popup.verticalLayout.count()):
                crud.popup.verticalLayout.itemAt(widget).widget().hide()
                crud.popup.verticalLayout_2.itemAt(widget).widget().hide()
                crud.popup.verticalLayout_3.itemAt(widget).widget().hide()

        # --pushButton_cancel---------------------------------------------------
            crud.popup.pushButton_cancel.hide()

        # --pushButton_accept---------------------------------------------------
            crud.popup.pushButton_accept.setText('OK')
            crud.popup.pushButton_accept.clicked.connect(crud.close)

        # --TabOrder------------------------------------------------------------
            crud.popup.comboBox_store.setFocus()
            crud.setTabOrder(
                crud.popup.comboBox_store, crud.popup.pushButton_accept
            )

        elif self.sender().objectName() == object_name[2]:
        # --labels--------------------------------------------------------------
            crud.popup.label_stores.setText("Group")
            crud.popup.label_officeteam.setText("Email")

        # --pushButton_accept_--------------------------------------------------
            crud.popup.pushButton_accept_store.hide()
            crud.popup.pushButton_accept_officeteam.setText('Insert')

        # --TabOrder------------------------------------------------------------
            crud.popup.comboBox_store.setFocus()
            crud.setTabOrder(
                crud.popup.comboBox_store,
                crud.popup.lineEdit_emails_stores
            )
            crud.setTabOrder(
                crud.popup.lineEdit_emails_stores,
                crud.popup.lineEdit_emails_officeteam
            )
            crud.setTabOrder(
                crud.popup.lineEdit_emails_officeteam,
                crud.popup.pushButton_accept_officeteam
            )
            crud.setTabOrder(
                crud.popup.pushButton_accept_officeteam,
                crud.popup.pushButton_accept
            )
            crud.setTabOrder(
                crud.popup.pushButton_accept,
                crud.popup.pushButton_cancel
            )

        # --pushButton_cancel---------------------------------------------------
            crud.popup.pushButton_cancel.clicked.connect(crud.close)

        # --pushButton_accept---------------------------------------------------
            crud.popup.pushButton_accept.clicked.connect(crud.table_element_insertion)
        else:
            crud.popup.pushButton_accept_store.setText('Delete')
            crud.popup.pushButton_accept_officeteam.setText('Delete')

        crud.exec_()

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
                    self.stores[self.mwin.comboBox_recievingStore.currentText()]
                )
                officeTeam = ('; ').join(self.office_team)

                try:
                    outlook = client.GetActiveObject("Outlook.Application")
                except:
                    outlook = client.Dispatch("Outlook.Application")

                message = outlook.CreateItem(0)
                message.Display()
                message.To = recipients
                message.CC = officeTeam

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
                    formattedText.formattedText_EmptyFields)
                incoplete.exec_()

        except OSError as err:
            log.warning(err)

            no_windows = PopUpText()
            no_windows.setWindowTitle("No Windows OS")
            no_windows.popup.label.setText(formattedText.formattedText_Os)
            no_windows.exec_()
            self.close()

        except Exception as err:
            log.warning(err)


class PopUpText(QtWidgets.QDialog):

    def __init__(self, parent=None):
        # --SetUp-------------------------------------------------------------------
        super().__init__(parent)
        self.popup = Ui_Dialog_Text()
        self.popup.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)


class EmailCRUD(QtWidgets.QDialog):

    def __init__(self, parent=None):
    # --SetUp-------------------------------------------------------------------
        super().__init__(parent)
        self.popup = Ui_Dialog_EmailCRUD()
        self.popup.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.db_ = None

    # --pushButton_accept-------------------------------------------------------
        self.popup.comboBox_store.activated.connect(self.table_show)

# --Methods---------------------------------------------------------------------
    @property
    def connection_(self):
        connection = self.db_
        return connection

    @connection_.setter
    def connection(self, db_):
        self.db_ = db_

    def table_show(self):
        self.popup.tableWidget.setColumnCount(0)
        self.popup.tableWidget.setRowCount(0)

        table = self.db_.table(
            self.popup.comboBox_store.currentText()
        )

        for header in table.select_headers:
            column_count = self.popup.tableWidget.columnCount()

            self.popup.tableWidget.insertColumn(column_count)
            self.popup.tableWidget.setHorizontalHeaderItem(
                column_count,
                QtWidgets.QTableWidgetItem(f'{header[0]}')
            )

            row = 0
            for email in table.select_emails(header[0]):
                row_count = self.popup.tableWidget.rowCount()

                if (
                    row_count == 0 or
                    self.popup.tableWidget.item(column_count, (row-1)) != None
                ):
                    self.popup.tableWidget.insertRow(row_count)

                self.popup.tableWidget.setItem(
                    row,
                    column_count,
                    QtWidgets.QTableWidgetItem(f'{email[0]}')
                )

                row += 1

        self.popup.tableWidget.resizeColumnsToContents()

    def table_element_insertion(self):
        print(self.popup.tableWidget.selectedIndexes()[0].column())
        # for item in self.popup.tableWidget.selectedIndexes():
        #     print(item)
        #     print(self.popup.tableWidget.horizontalHeaderItem(item.column()).text())
            # self.popup.tableWidget.verticalHeader().text()

    def reject(self):
        self.close()

    def closeEvent(self, event=None):
        self.db_.conn.close()
        if event != None:
            event.accept()


if __name__ == '__main__':
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
