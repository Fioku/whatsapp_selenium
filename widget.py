from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from form import Ui_Widget
from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import QThread, Qt
from modules.whatsapp_handler import Whatsapp_handler
import os

class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.driver = None  # Initialize driver as None
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.center_window()
        self.set_always_on_top()
        self.set_buttons_events()
        self.ui.lineEdit.returnPressed.connect(self.ui.pushButton.click)
        self.is_login = False
        
    def center_window(self):
        center = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

    def set_always_on_top(self):
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        
    def set_buttons_events(self):
        self.ui.pushButton.pressed.connect(self.process_send_button)
        
    def process_send_button(self):
        self.whatsapp_login()
        to = self.ui.lineEdit.text()
        if to:
            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton.setStyleSheet("#pushButton {\n"
                                        "	border: 1px solid #EEEEEE;\n"
                                        "}")
            self.thread = QThread()
            self.worker = Whatsapp_handler(self.driver, to)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.on_task_finished)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()

    def on_task_finished(self):
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton.setStyleSheet("#pushButton {\n"
                            "	border: 1px solid black;\n"
                            "	border-radius: 3px;\n"
                            "}")
        
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
                service = Service(os.getcwd() + r'\chromedriver-win64\chromedriver.exe')
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
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
            
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    news_window = Widget()
    news_window.show()
    sys.exit(app.exec())
