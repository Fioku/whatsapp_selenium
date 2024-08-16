import os
import shutil
from datetime import datetime
import sys
import ctypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from ui.mainWindow import Ui_Widget
from modules.models import Numbers, File
from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import QThread, Qt, QObject, Signal, Slot
from PySide6.QtGui import QIcon
from modules.whatsapp_handler import Whatsapp_handler
import subprocess
import time

class Worker(QObject):
    finished = Signal()
    numbers_updated = Signal(list)
    new_file_detected = Signal(str, list)

    def __init__(self, ui, file_table, numbers_table):
        super().__init__()
        print("Initializing Worker...")
        self.ui = ui
        self.file_table = file_table
        self.numbers_table = numbers_table
        self.is_working = False
        print("Worker initialized.")

    def run(self):
        while self.is_working:
            to1 = self.ui.lineEdit1.text() if self.ui.is_active1.isChecked() else None
            to2 = self.ui.lineEdit2.text() if self.ui.is_active2.isChecked() else None
            folder_path = open("normal send path folder.txt", 'r').read().strip()
            download_folder = os.path.expanduser(folder_path)
            if os.path.exists(download_folder):
                try:
                    downloaded_files = sorted(os.listdir(download_folder), key=lambda x: os.path.getctime(os.path.join(download_folder, x)))
                    file_path = os.path.join(download_folder, downloaded_files[-1])
                    print(file_path)
                except:
                    print(1)
                    self.file_table.remove_file_info()
                    time.sleep(5)
                    continue
            else:
                print(f"Folder not found: {download_folder}")
                self.finished.emit()
                return

            last_record = self.file_table.get_last_record()
            main_number = os.path.basename(file_path).split('.')[0]
            file_ctime = os.path.getctime(file_path)

            if last_record:
                if last_record[1] == file_ctime and main_number == last_record[0]:
                    print('File already processed.')
                    time.sleep(5)
                    continue
                else:
                    self.file_table.update_record(main_number, file_ctime)
            else:
                self.file_table.add_file_info(main_number, file_ctime)

            numbers_list = [main_number] if len(main_number) == 11 else []
            print(numbers_list)
            if to1 is not None and len(to1) == 11:
                print(to1)
                numbers_list.append(to1)
            if to2 is not None and len(to2) == 11:
                print(to2)
                numbers_list.append(to2)

            self.numbers_table.add_number(str(main_number))

            self.new_file_detected.emit(file_path, numbers_list)
            self.numbers_updated.emit(numbers_list)

            time.sleep(25)

        self.finished.emit()

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
        self.numbers_table = Numbers()
        self.file_table = File()
        self.ui.lineEdit1.returnPressed.connect(self.ui.pushButton.click)
        self.is_login = False
        self.setWindowIcon(QIcon('icon.ico'))
        try:
            self.password = open("C:\\Program Files\\MST\\MTS_S.txt", "r").read().strip()
        except:
            self.password = open("C:\\Program Files\\mst\\mts_s.txt.txt", "r").read().strip()
        self.is_working = False
        self.numbers_list = []

    def center_window(self):
        center = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

    def set_always_on_top(self):
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    def set_buttons_events(self):
        self.ui.login_button.pressed.connect(self.is_true_password)
        self.ui.pushButton.pressed.connect(self.toggle_worker)
        self.ui.sendAllButton.pressed.connect(self.process_send_all)

    def toggle_worker(self):
        if self.is_working:
            self.stop_worker()
        else:
            self.start_worker()

    def start_worker(self):
        try:
            self.is_working = True
            self.ui.pushButton.setText('Stop')
            self.ui.sendAllButton.setEnabled(False)
            self.ui.pushButton.setStyleSheet("#pushButton {\n"
                                            "    border-radius: 3px;\n"
                                            "    background-color: red;\n"
                                            "    color: #000;\n"
                                            "}")
            self.ui.sendAllButton.setStyleSheet("#sendAllButton {\n"
                            "    border-radius: 3px;\n"
                            "    color: #000;\n"
                            "    background-color: #EEEEEE;\n"
                            "}")

            self.worker = Worker(self.ui, self.file_table, self.numbers_table)
            self.worker.is_working = True

            self.worker_thread = QThread()
            self.worker.moveToThread(self.worker_thread)

            self.worker.finished.connect(self.stop_worker)
            self.worker.numbers_updated.connect(self.handle_numbers_update)
            self.worker.new_file_detected.connect(self.process_file)

            self.worker_thread.started.connect(self.worker.run)
            self.worker_thread.start()

            print("Worker thread started.")

        except Exception as e:
            print(f"Error starting worker: {e}")
        
    def stop_worker(self):
        if self.worker:
            self.worker.is_working = False
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.worker_thread.deleteLater()
            self.worker.deleteLater()

        self.is_working = False
        self.ui.pushButton.setText('Start')
        self.ui.pushButton.setEnabled(True)
        self.ui.sendAllButton.setEnabled(True)
        self.ui.pushButton.setStyleSheet("#pushButton {\n"
                            "	background-color: #74E291;\n"
                            "   color: #000;\n"
                            "	border-radius: 3px;\n"
                            "}")
        self.ui.sendAllButton.setStyleSheet("#sendAllButton {\n"
                    "	background-color: #74E291;\n"
                    "   color: #000;\n"
                    "	border-radius: 3px;\n"
                    "}")

    @Slot(list)
    def handle_numbers_update(self, numbers_list):
        self.numbers_list.extend(numbers_list)
        print(self.numbers_list)

    @Slot(str, list)
    def process_file(self, file_path, numbers_list):
        try:
            # print(2)
            # thread = QThread()
            # handler = Whatsapp_handler(self.driver, file_path, numbers_list)
            # handler.moveToThread(thread)
            # print(333333333)
            # thread.started.connect(handler.run)
            # handler.finished.connect(thread.quit)
            # handler.finished.connect(handler.deleteLater)
            # thread.finished.connect(thread.deleteLater)
            Whatsapp_handler(self.driver, file_path, numbers_list).run()
            # thread.start()
            self.backup_file(file_path)
            self.numbers_list = []
        except Exception as e:
            print(f"Error in process_file: {e}")

    def process_send_all(self):
        from send_to_all_popup import SendToAllObj
        popup = SendToAllObj(self.driver)
        popup.show()

    def on_task_finished(self):
        self.ui.pushButton.setEnabled(True)
        self.ui.sendAllButton.setEnabled(True)
        self.ui.pushButton.setStyleSheet("background-color: #74E291; color: black; border-radius: 3px;")
        self.ui.sendAllButton.setStyleSheet("background-color: #74E291; color: black; border-radius: 3px;")
        self.ui.pushButton.setText('Start')
        self.ui.lineEdit1.setText("")
        self.numbers_list = []

    def start_ui(self):
        print(self.ui.pushButton.text())
        if self.ui.pushButton.text() == 'Start':
            self.ui.sendAllButton.setEnabled(False)
            self.ui.pushButton.setStyleSheet("#pushButton {\n"
                                            "    border: 1px solid #000;\n"
                                            "	border-radius: 3px;\n"
                                            "    background-color: red;\n"
                                            "    color: #000;\n"
                                            "}")
            self.ui.pushButton.setText('Stop')
            self.ui.sendAllButton.setStyleSheet("#sendAllButton {\n"
                            "    border: 1px solid #000;\n"
                            "    border-radius: 3px;\n"
                            "    color: #000;\n"
                            "    background-color: #EEEEEE;\n"
                            "}")
            self.is_working = True
        else:
            self.on_task_finished()

    def backup_file(self, file_path):
        log_dir = 'log'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        today = datetime.now().strftime('%Y-%m-%d')
        dated_dir = os.path.join(log_dir, today)
        if not os.path.exists(dated_dir):
            os.makedirs(dated_dir)

        shutil.copy(file_path, dated_dir)

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
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.driver.execute_script("window.lastBlobData = null;")
                self.is_login = False
            print(self.is_login)
            if not self.is_login:
                self.driver.get('https://web.whatsapp.com')
                print("Scan QR code to log in")

                WebDriverWait(self.driver, 300).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas[aria-label="Scan me!"]'))
                )
                self.is_login = True
        except Exception as e:
            print(e)
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
            self.ui.sendAllButton.show()
            self.ui.is_active1.show()
            self.ui.is_active2.show()
            self.whatsapp_login()
        else:
            sys.exit(app.exec())

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    # Re-run the script with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

if __name__ == "__main__":
    # if not is_admin():
    #     run_as_admin()
    #     sys.exit()

    # Your existing code here
    app = QtWidgets.QApplication(sys.argv)
    news_window = Widget()
    news_window.show()
    sys.exit(app.exec())