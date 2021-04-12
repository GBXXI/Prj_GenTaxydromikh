
import logging
import os

import formattedText
from PySide2 import QtCore, QtGui, QtWidgets

from palette_EmailCRUD import Ui_Dialog_EmailCRUD
from PopUp_Text import PopUpText

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



class EmailCRUD(QtWidgets.QDialog):

    def __init__(self, db_connection, sender, parent=None):
    # --SetUp-------------------------------------------------------------------
        super().__init__(parent)
        self.popup = Ui_Dialog_EmailCRUD()
        self.popup.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.db_connection = db_connection
        self.sender = sender
        self.buffer = dict()

        object_name = {
            1: 'actionPreview',
            2: 'actionInsert',
            3: 'actionDelete'
        }

    # --State_changes-----------------------------------------------------------
        self.popup.comboBox_store.activated.connect(self.table_show)
        self.popup.tableWidget.itemSelectionChanged.connect(self.lineEdit_selection)

    # --comboBox_store----------------------------------------------------------
        # self.db_connection = DataBase(MainWindow.db_file)
        self.popup.comboBox_store.insertItem(0, '')
        self.popup.comboBox_store.insertItems(1,
            self.db_connection.show_views
        )

    # --pushButton_accept_------------------------------------------------------
        self.popup.pushButton_accept_officeteam.setEnabled(False)
        self.popup.pushButton_accept_officeteam.hide()

    # --lineEdit_emails_--------------------------------------------------------
        self.popup.lineEdit_emails_officeteam.setValidator(
            QtGui.QRegExpValidator(
                r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
            )
        )

        self.popup.lineEdit_emails_officeteam.textChanged.connect(
            self.valid_input
        )

    # --pushButton_cancel-------------------------------------------------------
        self.popup.pushButton_cancel.clicked.connect(self.reject)

    # --Cases-------------------------------------------------------------------
        if self.sender == object_name[1]:
        # --Title---------------------------------------------------------------
            self.setWindowTitle("Preview")

        # --Hiding Elements-----------------------------------------------------
            for widget in range(self.popup.verticalLayout.count()):
                self.popup.verticalLayout.itemAt(widget).widget().hide()
                self.popup.verticalLayout_2.itemAt(widget).widget().hide()
                self.popup.verticalLayout_3.itemAt(widget).widget().hide()

        # --pushButton_cancel---------------------------------------------------
            self.popup.pushButton_cancel.hide()

        # --pushButton_accept---------------------------------------------------
            self.popup.pushButton_accept.setText('OK')
            self.popup.pushButton_accept.clicked.connect(self.close)

        # --TabOrder------------------------------------------------------------
            self.popup.comboBox_store.setFocus()
            self.setTabOrder(
                self.popup.comboBox_store, self.popup.pushButton_accept
            )

        else:
        # --labels--------------------------------------------------------------
            self.popup.label_stores.setText("Group")
            self.popup.label_officeteam.setText("Email")

        # --pushButton_accept_--------------------------------------------------
            self.popup.pushButton_accept_store.hide()
            self.popup.pushButton_accept_officeteam.clicked.connect(
                self.table_update_view
            )

        # --TabOrder------------------------------------------------------------
            self.popup.comboBox_store.setFocus()
            self.setTabOrder(
                self.popup.comboBox_store,
                self.popup.lineEdit_emails_stores
            )
            self.setTabOrder(
                self.popup.lineEdit_emails_stores,
                self.popup.lineEdit_emails_officeteam
            )
            self.setTabOrder(
                self.popup.lineEdit_emails_officeteam,
                self.popup.pushButton_accept_officeteam
            )
            self.setTabOrder(
                self.popup.pushButton_accept_officeteam,
                self.popup.pushButton_accept
            )
            self.setTabOrder(
                self.popup.pushButton_accept,
                self.popup.pushButton_cancel
            )

        # --pushButton_accept---------------------------------------------------
            # self.popup.pushButton_accept.clicked.connect(
            #     self.table_db_update
            # )

            self.popup.pushButton_accept.clicked.connect(
                self.accept
            )

            if self.sender == object_name[2]:
            # --Title-----------------------------------------------------------
                self.setWindowTitle("Insert")

            # --pushButton_accept_----------------------------------------------
                self.popup.pushButton_accept_officeteam.setText("Insert")

            elif self.sender == object_name[3]:
            # --Title-----------------------------------------------------------
                self.setWindowTitle("Delete")

            # --pushButton_accept_----------------------------------------------
                self.popup.pushButton_accept_officeteam.setText("Delete")

            # --lineEdit_emails_------------------------------------------------
                self.popup.lineEdit_emails_stores.setReadOnly(True)
                self.popup.lineEdit_emails_officeteam.setReadOnly(True)


# --Methods---------------------------------------------------------------------
    @property
    def _connection(self):
        connection = self.db_connection
        return connection

    @_connection.setter
    def connection(self, db_connection):
        self.db_connection = db_connection

    def add_to_buffer(self, key, value):
        if (self.buffer.get(key, set()) != set()):
            self.buffer[key].update(set([value]))
        else:
            self.buffer[key] = set([value])

    def valid_input(self):
        if self.popup.lineEdit_emails_officeteam.hasAcceptableInput():
            self.popup.pushButton_accept_officeteam.show()
            self.popup.pushButton_accept_officeteam.setEnabled(True)
        else:
            self.popup.pushButton_accept_officeteam.hide()
            self.popup.pushButton_accept_officeteam.setEnabled(False)

    def table_show(self):
        self.popup.tableWidget.setColumnCount(0)
        self.popup.tableWidget.setRowCount(0)

        self.table = self.db_connection.table(
            self.popup.comboBox_store.currentText()
        )

        for header in self.table.select_headers:
            column_count = self.popup.tableWidget.columnCount()

            self.popup.tableWidget.insertColumn(column_count)
            self.popup.tableWidget.setHorizontalHeaderItem(
                column_count,
                QtWidgets.QTableWidgetItem(f'{header[0]}')
            )

            row = 0
            for email in self.table.select_emails(header[0]):
                row_count = self.popup.tableWidget.rowCount()

                if (
                    row_count == 0 or
                    self.popup.tableWidget.item((row-1), column_count) != None
                ):
                    self.popup.tableWidget.insertRow(row_count)

                self.popup.tableWidget.setItem(
                    row,
                    column_count,
                    QtWidgets.QTableWidgetItem(f'{email[0]}')
                )

                row += 1

        self.popup.tableWidget.resizeColumnsToContents()
        self.popup.tableWidget.setEditTriggers(
            QtWidgets.QTableWidget.NoEditTriggers
        )

    def lineEdit_selection(self):
        if self.popup.tableWidget.selectedIndexes() != []:
            try:
                column_num = self.popup.tableWidget.selectedIndexes()[-1].column()
                row_num = self.popup.tableWidget.selectedIndexes()[-1].row()
                header_object = self.popup.tableWidget.horizontalHeaderItem(
                    column_num
                )
                header_text = header_object.text()
                self.popup.lineEdit_emails_stores.setText(header_text)

            # --Showing the last selected item ---------------------------------
                if self.popup.tableWidget.item(
                    row_num,
                    column_num
                ):
                    self.popup.lineEdit_emails_officeteam.setText(
                        self.popup.tableWidget.item(
                            row_num,
                            column_num
                        ).text()
                    )
                else:
                    self.popup.lineEdit_emails_officeteam.setText("")

            except Exception as err:
                log.warning(err)

    def table_update_view(self):
        object_action = {
            1: 'Insert',
            2: 'Delete'
        }

        items = self.popup.tableWidget.findItems(
            self.popup.lineEdit_emails_officeteam.text(),
            QtCore.Qt.MatchWildcard
        )

        if self.sender().text() == object_action[1]:
            try:
                if items:
                    self.popup.tableWidget.clearSelection()
                    for item in items:
                        item.setSelected(True)
                        self.popup.tableWidget.scrollToItem(
                            item,
                            QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible
                        )
                    existing = PopUpText()
                    existing.setWindowTitle("Existing email")
                    existing.popup.label.setTextFormat(
                        QtCore.Qt.RichText
                    )
                    existing.popup.label.setText(
                        formattedText.existing_email(item.text())
                    )
                    existing.exec_()
                else:
                    self.add_to_buffer(
                        self.popup.lineEdit_emails_stores.text(),
                        self.popup.lineEdit_emails_officeteam.text()
                    )

                    column = 0
                    while column < self.popup.tableWidget.columnCount():
                        if (
                            self.popup.lineEdit_emails_stores.text() ==
                            self.popup.tableWidget.horizontalHeaderItem(column).text()
                        ):

                            row = 0
                            while row < self.popup.tableWidget.rowCount():

                                if (
                                    self.popup.tableWidget.item(row, column) ==
                                    None
                                ):
                                    self.popup.tableWidget.setItem(
                                        row,
                                        column,
                                        QtWidgets.QTableWidgetItem(
                                            self.popup.lineEdit_emails_officeteam.text()
                                        )
                                    )
                                    break
                                row += 1
                            else:
                                self.popup.tableWidget.insertRow(
                                    self.popup.tableWidget.rowCount()
                                )
                                self.popup.tableWidget.setItem(
                                    (self.popup.tableWidget.rowCount() - 1),
                                    column,
                                    QtWidgets.QTableWidgetItem(
                                        self.popup.lineEdit_emails_officeteam.text()
                                    )
                                )
                            break
                        column += 1
                    else:
                        self.popup.tableWidget.insertColumn(
                            self.popup.tableWidget.columnCount()
                        )
                        self.popup.tableWidget.setHorizontalHeaderItem(
                            (self.popup.tableWidget.columnCount() - 1),
                            QtWidgets.QTableWidgetItem(
                                self.popup.lineEdit_emails_stores.text()
                            )
                        )
                        # Recursion
                        self.table_update_view()

                new_item = self.popup.tableWidget.findItems(
                                self.popup.lineEdit_emails_officeteam.text(),
                                QtCore.Qt.MatchWildcard
                            )
                if new_item[0] != None:
                    self.popup.tableWidget.clearSelection()
                    new_item[0].setSelected(True)
                    self.popup.tableWidget.scrollToItem(
                        new_item[0],
                        QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible
                    )
                    self.popup.lineEdit_emails_officeteam.clear()

            except Exception as err:
                log.warning(err)

        elif self.sender().text() == object_action[2]:
            try:
                for item in items:
                    item.setSelected(True)
                    self.popup.tableWidget.scrollToItem(
                        item,
                        QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible
                    )

                self.add_to_buffer(
                    self.popup.lineEdit_emails_stores.text(),
                    self.popup.lineEdit_emails_officeteam.text()
                )
                self.popup.tableWidget.takeItem(item.row(), item.column())
                self.popup.lineEdit_emails_officeteam.clear()

            except Exception as err:
                log.warning(err)

        self.db_update = self.sender().text()


    def table_db_update(self):
        for key in self.buffer.keys():
            for element in self.buffer[key]:
                {
                    "Insert": lambda k,e: self.db_connection.email_insert(k, [e]),
                    "Delete": lambda k,e: self.db_connection.email_delete(k, e)

                }.get(self.db_update)(key, element)

    def accept(self):
        self.table_db_update()
        self.db_connection.cleanup(
            self.popup.comboBox_store.currentText()
        )
        self.close()

    def reject(self):
        self.close()

    def closeEvent(self, event=None):
        self.db_connection.conn.close()
