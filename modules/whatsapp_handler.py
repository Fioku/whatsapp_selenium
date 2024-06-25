from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time
import os
from PySide6.QtCore import QObject, Signal

class Whatsapp_handler(QObject):
    finished = Signal()

    def __init__(self, driver, to):
        super().__init__()
        self.driver = driver
        # self.main_number = '01068025122'
        self.main_number = '01281727282'
        self.to = to
        
    def run(self):
        try:
            if not self.is_chat_open():
                self.open_chat()
            time.sleep(1)
            self.forward_message()
            time.sleep(5)
        finally:
            # self.driver.quit()
            self.finished.emit()
            
    def open_chat(self):
        element = WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Search input textbox"]')))
        element.click()
        # time.sleep(1)
        element.send_keys(self.main_number)
        # time.sleep(1)
        search_result = WebDriverWait(self.driver, 60).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[aria-label="Search results."]')))
        for message in search_result:
            try:
                chat = WebDriverWait(message, 100).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.x1n2onr6.x14yjl9h.xudhj91.x18nykt9.xww2gxu')))
                chat.click()
                break
            except TimeoutException:
                print("Chat element is not clickable yet, continuing...")

    def forward_message(self):
        try:
            attachments_icon = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="attach-menu-plus"]')))
            attachments_icon.click()
            download_folder = os.path.join(os.path.expanduser("C:\ATTACHMENTS"))
            downloaded_files = sorted(os.listdir(download_folder), key=lambda x: os.path.getctime(os.path.join(download_folder, x)))
            file_path = os.path.join(download_folder, downloaded_files[-1])
            file_input = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')[1]
            file_input.send_keys(file_path)
            
            # time.sleep(1)
            
            message_input = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Add a caption"]')))
            message_input.send_keys(self.to)
            
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
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Add a caption"]')))
            message_input.send_keys(self.to)
            
            # time.sleep(1)
            
            send_button = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="send"]')))
            send_button.click()
            
    def is_chat_open(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Type a message"]'))
            )
            return True
        except TimeoutException:
            return False
