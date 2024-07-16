from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from form import Ui_Widget
from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import QThread, Qt
from PySide6.QtGui import QIcon
from modules.whatsapp_handler import Whatsapp_handler
import os
import subprocess

class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.center_window()
        self.set_always_on_top()
        self.setFixedSize(self.size())
        self.set_buttons_events()
        self.ui.lineEdit1.returnPressed.connect(self.ui.pushButton.click)
        self.is_login = False
        self.setWindowIcon(QIcon('icon.ico'))
        self.password = open("C:\Program Files\MST\MTS_S.txt", "r").read().strip()

    def center_window(self):
        center = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

    def set_always_on_top(self):
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    def set_buttons_events(self):
        self.ui.login_button.pressed.connect(self.is_true_password)
        self.ui.pushButton.pressed.connect(self.process_send_button)

    def process_send_button(self):
        to1 = self.ui.lineEdit1.text()
        to2 = self.ui.lineEdit2.text() if self.ui.is_active.isChecked() else None

        valid_to1 = len(to1) == 11
        valid_to2 = len(to2) == 11 if to2 else True

        if valid_to1 and valid_to2:
            self.whatsapp_login()
            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton.setStyleSheet("#pushButton {\n"
                                        "	border: 1px solid #EEEEEE;\n"
                                        "}")

            self.thread = QThread()
            self.worker = Whatsapp_handler(self.driver, to1, to2)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.on_task_finished)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()

        else:
            self.show_error_popup("Phone numbers must be 11 digits. Please type the phone numbers again.")

    def on_task_finished(self):
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton.setStyleSheet("#pushButton {\n"
                            "	border: 1px solid black;\n"
                            "	border-radius: 3px;\n"
                            "}")
        self.ui.lineEdit1.setText("")

    def is_driver_alive(self):
        try:
            self.driver.current_url
            return True
        except:
            return False

    def whatsapp_login(self):
        try:
            if not self.driver or not self.is_driver_alive():
                chrome_options = Options()
                chromedriver_path = os.path.join(os.getcwd(), 'chromedriver-win64', 'chromedriver.exe')
                service = Service(chromedriver_path)
                chrome_options.add_argument('--disable-extensions')

                startup_info = subprocess.STARTUPINFO()
                startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                service = Service(executable_path=chromedriver_path, log_path='chromedriver.log')
                self.driver = webdriver.Chrome(service=service, options=chrome_options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
                self.driver.execute_script("window.lastBlobData = null;")
                self.is_login = False

            if not self.is_login:
                self.driver.get('https://web.whatsapp.com')
                print("Scan QR code to log in")

                WebDriverWait(self.driver, 200).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas[aria-label="Scan me!"]'))
                )
                self.is_login = True
        except Exception:
            self.is_login = False

    def show_error_popup(self, message):
        self.ui.Widget.hide()
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()
        self.ui.Widget.show()

    def is_true_password(self):
        typed_password = self.ui.key.text()
        if typed_password == self.password:
            self.ui.key.hide()
            self.ui.login_button.hide()
            self.ui.lineEdit1.show()
            self.ui.lineEdit2.show()
            self.ui.pushButton.show()
            self.ui.is_active.show()
        else:
            sys.exit(app.exec())

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    news_window = Widget()
    news_window.show()
    sys.exit(app.exec())
