from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
from PySide6.QtCore import QObject, Signal

class Whatsapp_handler(QObject):
    finished = Signal()

    def __init__(self, driver, to1, to2=None):
        super().__init__()
        self.driver = driver
        self.main_number = open("phone.txt", "r").read().strip()
        self.to1 = to1
        self.to2 = to2
        
    def run(self):
        try:
            if not self.is_chat_open():
                self.open_praivte_chat()
            time.sleep(1)
            self.forward_message(self.to1)
            time.sleep(2)
            self.open_clint_chat()
            time.sleep(2)
            self.forward_message()
            time.sleep(2)
            self.open_praivte_chat()
            time.sleep(9)
            if self.to2:
                self.forward_message(self.to2)
                time.sleep(2)
                self.open_clint_chat()
                time.sleep(2)
                self.forward_message()
                time.sleep(2)
                self.open_praivte_chat()
        finally:
            # self.driver.quit()
            self.finished.emit()
            
    def open_praivte_chat(self):
        new_chat = WebDriverWait(self.driver, 100).until(
            EC.any_of(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[title="New chat"]')),
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[title="دردشة جديدة"]'))
            )
        )
        new_chat.click()
        time.sleep(1)
        search_input = WebDriverWait(self.driver, 100).until(
            EC.any_of(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Search input textbox"]')),
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="خانة إدخال نص البحث"]'))
            )
        )
        search_input.click()
        search_input.send_keys(self.main_number)
        time.sleep(3)
        search_input.send_keys(Keys.RETURN)

    def forward_message(self, to=None):
        try:
            attachments_icon = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="attach-menu-plus"]')))
            attachments_icon.click()
            f = open("path.txt", "r")
            download_folder = os.path.join(os.path.expanduser(f.read().strip()))
            downloaded_files = sorted(os.listdir(download_folder), key=lambda x: os.path.getctime(os.path.join(download_folder, x)))
            file_path = os.path.join(download_folder, downloaded_files[-1])
            file_input = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')[1]
            file_input.send_keys(file_path)
            
            # time.sleep(1)
            
            message_input = WebDriverWait(self.driver, 60).until(
                EC.any_of(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Add a caption"]')),
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="إضافة شرح"]'))
                )
            )
            
            if to:
                message_input.send_keys(to)
            
            # time.sleep(1)
            
            send_button = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="send"]')))
            send_button.click()
            
        except Exception:
            attachments_icon = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="attach-menu-plus"]')))
            attachments_icon.click()
            download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            downloaded_files = sorted(os.listdir(download_folder), key=lambda x: os.path.getctime(os.path.join(download_folder, x)))
            file_path = os.path.join(download_folder, downloaded_files[-1])
            file_input = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')[0]
            file_input.send_keys(file_path)
            
            # time.sleep(1)
            
            message_input = WebDriverWait(self.driver, 60).until(
                EC.any_of(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Add a caption"]')),
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="إضافة شرح"]'))
                )
            )
            message_input.send_keys(self.to)
            
            # time.sleep(1)
            
            send_button = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="send"]')))
            send_button.click()
            
    def open_clint_chat(self):
        try:
            last_message = self.get_messages_out()[-1]
            self.open_customer_chat(last_message)
        except Exception as e:
            print(e)
            
    def get_messages_out(self):
        messages_in = []
        messages_div = WebDriverWait(self.driver, 60).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div._amjv._aotl')))
        for message in messages_div:
            if message.find_elements(By.CSS_SELECTOR, 'div.message-out'):
                messages_in.append(message)
        return messages_in
    
    def open_customer_chat(self, message):
        phone_number_as_link = WebDriverWait(message, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[dir="auto"]')))
        phone_number_as_link.click()
        customer_chat = WebDriverWait(self.driver, 60).until(
            EC.any_of(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Chat with "]')),
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="الدردشة مع "]'))
            )
        )
        customer_chat.click()
            
    def is_chat_open(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Type a message"]')),
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="اكتب رسالة"]'))
                )
            )
            return True
        except TimeoutException:
            return False
