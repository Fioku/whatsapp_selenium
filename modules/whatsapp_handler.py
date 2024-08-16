from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from .models import Numbers
from PySide6.QtCore import QObject, Signal

class Whatsapp_handler(QObject):
    finished = Signal()

class Whatsapp_handler(QObject):
    finished = Signal()

    def __init__(self, driver, file_path, numbers):
        super().__init__()
        print("Initializing Whatsapp_handler...")
        self.driver = driver
        self.main_number = open("phone.txt", "r").read().strip()
        self.numbers_table = Numbers()
        self.numbers = numbers
        self.file_path = file_path
        print("Whatsapp_handler initialized.")

    def run(self):
        print("Starting WhatsApp handler...")
        try:
            for number in self.numbers:
                if not self.is_chat_open():
                    self.open_private_chat()
                time.sleep(1)
                self.forward_message(str(number))
                time.sleep(2)
                self.open_client_chat()
                time.sleep(2)
                self.forward_message()
                time.sleep(2)
                self.open_private_chat()
                time.sleep(5)
            self.delete_chat()
            print("Finished processing all numbers.")
        except Exception as e:
            print(f"Error in Whatsapp_handler run: {e}")
        finally:
            self.finished.emit()

    def open_private_chat(self):
        new_chat = WebDriverWait(self.driver, 100).until(
            EC.any_of(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[title="New chat"]')),
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[title="دردشة جديدة"]'))
            )
        )
        new_chat.click()
        time.sleep(1)
        # search_input = WebDriverWait(self.driver, 100).until(
        #     EC.any_of(
        #         EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Search input textbox"]')),
        #         EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="خانة إدخال نص البحث"]')),
        #         EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="البحث عن دردشة أو بدء دردشة جديدة"]')),
        #         EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Search or start new chat]'))
        #     )
        # )

        search_input = WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="textbox"]'))
        )
        search_input.click()

        # The search input box changes the DOM after clicking it, wait again for the input to be ready
        type_number = WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[contenteditable="true"]'))
        )
        type_number.send_keys(self.main_number)
        time.sleep(3)
        type_number.send_keys(Keys.RETURN)

    def forward_message(self, to=''):
        try:
            attachments_icon = WebDriverWait(self.driver, 60).until(
                EC.any_of(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="attach-menu-plus"]')),
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="plus"]'))
                )
            )
            attachments_icon.click()

            # download_folder = os.path.expanduser(self.folder_path)
            # downloaded_files = sorted(os.listdir(download_folder), key=lambda x: os.path.getctime(os.path.join(download_folder, x)))
            # self.file_path = os.path.join(download_folder, downloaded_files[-1])
            file_input = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')[1]
            file_input.send_keys(self.file_path)

            message_input = WebDriverWait(self.driver, 60).until(
                EC.any_of(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-placeholder="Add a caption"]')),
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-placeholder="إضافة شرح"]'))
                )
            )

            if to:
                message_input.send_keys(to)

            send_button = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="send"]')))
            send_button.click()

        except FileNotFoundError as e:
            print(f"Error: {e}")
            print(f"Attempting to handle missing folder path: {self.folder_path}")
            # Handle exception or attempt recovery
        except Exception as e:
            print(f"An error occurred: {e}")


    def open_client_chat(self):
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

    def delete_chat(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'span[class="xr9ek0c"]').click()
            time.sleep(2)
            delete_button = WebDriverWait(self.driver, 60).until(
                EC.any_of(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Delete chat"]')),
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="حذف الدردشة"]')),
                )
            )
            delete_button.click()
            time.sleep(2)
            WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.x889kno.x1a8lsjc.xbbxn1n.xxbr6pl.x1n2onr6.x1rg5ohu.xk50ysn.x1f6kntn.xyesn5m.x1z11no5.xjy5m1g.x1mnwbp6.x4pb5v6.x178xt8z.xm81vs4.xso031l.xy80clv.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x1v8p93f'))).click()
            print('done')
            time.sleep(2)
            print(333333)
        except Exception as e:
            print(e)

    def is_chat_open(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-placeholder="Type a message"]')),
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-placeholder="اكتب رسالة"]'))
                )
            )
            return True
        except TimeoutException:
            return False
