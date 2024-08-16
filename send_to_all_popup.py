from modules.models import Numbers
import os
import sys
from ui.SEND_TO_ALL_POPUP import UI_Send_To_All
from modules.models import Numbers
from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import QRect, Qt, QCoreApplication
from PySide6.QtGui import QIcon
import time
from modules.whatsapp_handler import Whatsapp_handler

class SendToAllObj(QtWidgets.QWidget):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.ui = UI_Send_To_All()
        self.ui.setupUi(self)
        self.center_window()
        self.set_always_on_top()
        self.setFixedSize(self.size())
        self.set_buttons_events()
        self.checkboxes = []
        self.numbers_table = Numbers()
        self.update_number_table()
        self.setWindowIcon(QIcon('icon.ico'))

    def center_window(self):
        center = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

    def set_always_on_top(self):
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    def set_buttons_events(self):
        self.ui.selectAll.stateChanged.connect(self.update_checkboxes)
        self.ui.sendButton.pressed.connect(self.run)

    def run(self):
        checked_numbers = self.get_checked_numbers()
        if checked_numbers:
            self.ui.sendButton.setStyleSheet(u"#sendButton {\n"
                                        "	background-color: red;\n"
                                        "   color: #000;\n"
                                        "   border-radius: 3px;\n"
                                        "   font-weight: 600;\n"
                                        "}")
            self.ui.sendButton.setEnabled(False)
            self.ui.sendButton.setText('Sending..')
            QCoreApplication.processEvents()

            folder_path = open("send to all path folder.txt", 'r').read().strip()
            download_folder = os.path.expanduser(folder_path)
            if os.path.exists(download_folder):
                downloaded_files = sorted(os.listdir(download_folder), key=lambda x: os.path.getctime(os.path.join(download_folder, x)))
                file_path = os.path.join(download_folder, downloaded_files[-1])
            else:
                self.show_error_popup(f"Folder not found: {download_folder}")
                return
            Whatsapp_handler(self.driver, file_path, checked_numbers).run()

            self.ui.sendButton.setStyleSheet(u"#sendButton {\n"
                                        "	background-color: #6ec007;\n"
                                        "   color: #fffff2;\n"
                                        "   border-radius: 3px;\n"
                                        "   font-weight: 600;\n"
                                        "}")
            self.ui.sendButton.setText('Send To All')
            self.ui.sendButton.setEnabled(True)
            QCoreApplication.processEvents()

    def get_checked_numbers(self):
        checked_numbers = []
        layout = self.ui.number_table_layout
        for i in range(layout.count()):
            number_row = layout.itemAt(i).widget()
            checkbox = number_row.findChild(QtWidgets.QCheckBox, "checkbox")
            number_label = number_row.findChild(QtWidgets.QLabel, "number_phone")
            if checkbox and checkbox.isChecked():
                checked_numbers.append(number_label.text())
        return checked_numbers

    def update_checkboxes(self):
        for checkbox in self.checkboxes:
            if self.ui.selectAll.isChecked():
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)

    def update_number_table(self,):
        self.clear_number_table()
        numbers = self.numbers_table.read_numbers()
        for number in numbers:
            self.add_number_row(number=number)

    def clear_number_table(self):
        layout = self.ui.number_table_layout
        for _ in reversed(range(layout.count())):
            layout.itemAt(0).widget().setParent(None)

    def add_number_row(self, number):
        number_row = QtWidgets.QWidget(parent=self.ui.scroll_area)
        number_row.setFixedHeight(30)
        number_row.setStyleSheet("#number_row{\n"
            "    border-top: 1px solid #C7C8CC;\n"
            "    border-bottom: 1px solid #C7C8CC;\n"
            # "    border-radius: 2px;\n"
            "}"
        )
        number_row.setObjectName("number_row")
        self.ui.number_table_layout.addWidget(number_row)

        checkbox = QtWidgets.QCheckBox(parent=number_row)
        checkbox.setObjectName(u"checkbox")
        checkbox.setGeometry(QRect(0, 7, 15, 15))
        checkbox.setStyleSheet(u"#checkbox {\n"
                                     "  background-color: transparent;\n"
                                     "	border: 1px solid #C7C8CC;\n"
                                     "   border-radius: 3px;\n"
                                     "}")
        self.checkboxes.append(checkbox)
        
        number_phone = QtWidgets.QLabel(parent=number_row)
        number_phone.setObjectName(u"number_phone")
        number_phone.setGeometry(QRect(75, 7, 100, 15))
        number_phone.setStyleSheet(u"#number_phone {\n"
                                     "  color: #000;\n"
                                     "  font-weight: 600;\n"
                                     "}")
        number_phone.setText(number)
        
    def show_error_popup(self, message):
        self.ui.Widget.hide()
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()
        self.ui.Widget.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    news_window = SendToAllObj()
    news_window.show()
    sys.exit(app.exec())
