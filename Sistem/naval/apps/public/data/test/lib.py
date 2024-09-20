import sys
import cv2
import os
from datetime import datetime
import time

import os
import numpy as np
import urllib.request

import serial
import telebot

## WHATSAPP
import os
import sys
import time
import logging
import platformdirs
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    UnexpectedAlertPresentException,
    NoSuchElementException,
)
from webdriver_manager.chrome import ChromeDriverManager

LOGGER = logging.getLogger()


class Vision:
    def __init__(self, isUsingCam=None, addr=None, index=0):
        # write configuration
        self.frame_count = 0
        self.filenames = None
        self.fourcc = None
        self.out = None

        # get address
        self.cap = None
        self.success = False
        self.index = index
        if isUsingCam:
            while not self.success:
                try:
                    print("[INFO] Initialize Camera")
                    self.cap = cv2.VideoCapture(self.index)
                    if not self.cap.isOpened():
                        raise Exception(f"Cannot Open Camera by Index {self.index}")
                    ret, frame = self.cap.read()
                    if not ret:
                        raise Exception(f"Failed to Capture Frame by Index {self.index}")
                    self.success = True
                except Exception as err:
                    print(f"[ERROR] Camera Initialization Failed: {err}")
                    time.sleep(0.5)
                    self.index += 1
            print(f"[INFO] Camera Initialization Success")
        else:
            self.cap = cv2.VideoCapture(addr)

        # fps
        self._prev_time = 0
        self._new_time = 0

    # def writeConfig(self, name="output.mp4", types="mp4v"):  # XVID -> avi
    #     self.filenames = name
    #     self.fourcc = cv2.VideoWriter_fourcc(*types)  # format video
    #     # filename, format, FPS, frame size
    #     self.out = cv2.VideoWriter(
    #         self.filenames, self.fourcc, 15.0, (450, 337))

    def write(self, frame):
        self.out.write(frame)

    def writeImg(self, frame, path="cats-output.png"):
        filename = path
        cv2.imwrite(filename, frame)
        with open(filename, 'ab') as f:
            f.flush()
            os.fsync(f.fileno())

    def resize(self, image, width=None, height=None,
               interpolation=cv2.INTER_AREA):
        dim = None
        w = image.shape[1]
        h = image.shape[0]
        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        resized = cv2.resize(image, dim, interpolation=interpolation)
        return resized

    def __get_fps(self):
        fps = 0.0
        try:
            self._new_time = time.time()
            fps = 1 / (self._new_time - self._prev_time)
            self._prev_time = self._new_time
            fps = 30 if fps > 30 else 0 if fps < 0 else fps
        except ZeroDivisionError as e:
            pass
        return int(fps)

    def blur(self, frame=None, sigma=11):
        return cv2.GaussianBlur(frame, (sigma, sigma), 0)

    def setBrightness(self, frame, value):
        h, s, v = cv2.split(
            cv2.cvtColor(frame, cv2.COLOR_BGR2HSV))
        v = np.clip(v.astype(int) + value, 0, 255).astype(np.uint8)
        return cv2.cvtColor(
            cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)

    def setContrast(self, frame, value):
        alpha = float(131 * (value + 127)) / (127 * (131 - value))
        gamma = 127 * (1 - alpha)
        return cv2.addWeighted(
            frame, alpha, frame, 0, gamma)

    def setBrightnessNcontrast(self, frame, bright=0.0, contr=0.0, beta=0.0):
        return cv2.addWeighted(frame, 1 + float(contr)
                               / 100.0, frame, beta, float(bright))

    def read(self, frame_size=480, show_fps=False):
        try:
            success, frame = self.cap.read()
            if not success:
                raise RuntimeError
            if show_fps:
                try:  # put fps
                    cv2.putText(frame, str(self.__get_fps()) + " fps", (20, 40), 0, 1,
                                [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                except RuntimeError as e:
                    print(e)
            frame = self.resize(frame, frame_size)
            return frame
        except RuntimeError as e:
            print("[INFO] Failed to capture the Frame")

    def readFromUrl(self, url="http://192.168.200.24/cam-hi.jpg", frame_size=480, show_fps=False):
        try:
            img_resp = urllib.request.urlopen(url)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgnp, -1)
            if show_fps:
                try:  # put fps
                    cv2.putText(frame, str(self.__get_fps()) + " fps", (20, 40), 0, 1,
                                [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                except RuntimeError as e:
                    print(e)
            frame = self.resize(frame, frame_size)
            return frame
        except RuntimeError as e:
            print("[INFO] Failed to capture the Frame")

    def show(self, frame, winName="frame"):
        cv2.imshow(winName, frame)

    def wait(self, delay):
        return cv2.waitKey(delay)

    def release(self):
        self.cap.release()

    def destroy(self):
        cv2.destroyAllWindows()
class ImgRex:  # 3
    def __init__(self):
        pass

    def __map(self, x, inMin, inMax, outMin, outMax):
        return (x - inMin) * (outMax - outMin) // (inMax - inMin) + outMin

    def load(self, weight_path, cfg, classes):
        self.classes = None
        with open(classes, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.colors = np.random.uniform(
            0, 255, size=(len(self.classes), 3))  # optional
        self.net = cv2.dnn.readNet(weight_path, cfg)
        # Use DNN_BACKEND_CUDA and DNN_TARGET_CUDA for GPU support
        self.net = cv2.dnn.readNet(weight_path, cfg)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        # self.net = cv2.dnn.readNetFromDarknet(cfg, weight_path)
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i - 1]
                              for i in self.net.getUnconnectedOutLayers()]
        # self.output_layers = self.net.getUnconnectedOutLayersNames()

    @staticmethod
    def draw(frame, detection):
        if detection is not []:
            for hasil in detection:
                color = hasil["color"]
                cv2.rectangle(
                    frame, (hasil["x"], hasil["y"]), (hasil["x"] + hasil["width"], hasil["y"] + hasil["height"]), color, 2)
                tl = round(0.002 * (frame.shape[0] + frame.shape[1]) / 2) + 1
                c1, c2 = (int(hasil["x"]), int(hasil["y"])), (int(
                    hasil["width"]), int(hasil["height"]))

                tf = int(max(tl - 1, 1))  # font thickness
                t_size = cv2.getTextSize(
                    hasil["class"], 0, fontScale=tl / 3, thickness=tf)[0]
                c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3

                cv2.rectangle(frame, c1, c2, color, -1, cv2.LINE_AA)  # filled
                cv2.putText(frame, hasil["class"] + " " + str(int(hasil["confidence"] * 100)) + "%",
                            (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
                cv2.circle(frame, (
                    int(hasil["x"] + int(hasil["width"] / 2)), int(hasil["y"] + int(hasil["height"] / 2))),
                           4, color, -1)
                cv2.putText(frame, str(int(hasil["x"] + int(hasil["width"] / 2))) + ", " + str(
                    int(hasil["y"] + int(hasil["height"] / 2))), (
                                int(hasil["x"] + int(hasil["width"] / 2) + 10),
                                int(hasil["y"] + int(hasil["height"] / 2) + 10)), cv2.FONT_HERSHEY_PLAIN, tl / 2,
                            [255, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
        return frame

    def predict(self, frame, tresh_confidence = 0.0):
        blob = cv2.dnn.blobFromImage(
            frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        height, width, ch = frame.shape
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        class_ids = []
        confidences = []
        boxes = []
        center = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                # print(class_id, confidence)
                if confidence > tresh_confidence:
                    # object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    center.append([center_x, center_y])
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        values = []
        indexes = cv2.dnn.NMSBoxes(
            boxes, confidences, 0.0, 0.0)  # 0.4 changeable
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                label = str(self.classes[class_ids[i]])
                x, y, w, h = boxes[i]
                temp = {
                    "class": label,
                    "confidence": confidences[i],
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "center": center[i],
                    "color": self.colors[class_ids[i]]
                }
                values.append(temp)
        return values
def resize(image, width=None, height=None, interpolation=cv2.INTER_AREA):
        dim = None
        w = image.shape[1]
        h = image.shape[0]
        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        resized = cv2.resize(image, dim, interpolation=interpolation)
        return resized

class WhatsappClient:
    def __init__(self):

        self.WA = WhatsApp()

    def find_user(self, number):
        self.number = str(number)
        self.WA.find_user(str(number))

    def find_by_username(self, number):
        self.number = str(number)
        self.WA.find_by_username( str(number))
    def kirimText(self, text):
        self.WA.send_message(str(text))

    def kirimTextSingkat(self, text):
        self.WA.send_direct_message(str(self.number), str(text))

    def kirimGambar(self, img, caption=''):
        self.WA.send_picture(img, str(caption))

    def kirimGambarCv2(self, img, caption=''):
        # Konversi frame OpenCV menjadi data JPEG
        _, jpeg_image = cv2.imencode(".jpg", img)
        self.WA.send_picture(jpeg_image.tobytes(), str(caption))

class TelegramClient:
    def __init__(self, token):
        self.token = token
        self.bot = self._create_bot()

    def _create_bot(self):
        bot = telebot.TeleBot(self.token)
        return bot

    def send_message(self, chat_id, text):
        self.bot.send_message(chat_id, text)

    def send_imagecv2(self, chat_id, image):
        # Konversi frame OpenCV menjadi data JPEG
        _, jpeg_image = cv2.imencode(".jpg", image)
        # Kirim gambar menggunakan sendPhoto
        self.bot.send_photo(chat_id, photo=jpeg_image.tobytes())

    def start_polling(self):
        self.bot.polling(none_stop=True, interval=0, timeout=20)

    def stop_polling(self):
        self.bot.stop_polling()

class SensorData:
    def __init__(self, data_list):
        self.latitude = data_list[0]
        self.longitude = data_list[1]
        self.temperature = data_list[2]
        self.humidity = data_list[3]
        self.smoke_sensor = data_list[4]

class SensorDataReader:
    def __init__(self, port='COM6', baud_rate=9600, timeout=1, buffer_size=5, process=None):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.serial_conn = None
        self.buffer = []
        self.process = process
        self.data = None

    def open_serial_connection(self):
        try:
            self.serial_conn = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            self.serial_conn.reset_input_buffer()
            print("[INFO] Serial Communication Initialized.")
        except Exception as err:
            print(f"[ERROR] Failed to initialize serial communication: {err}")

    def close_serial_connection(self):
        try:
            if self.serial_conn and self.serial_conn.is_open:
                self.serial_conn.close()
                print("[INFO] Serial Connection closed.")
        except Exception as err:
            print(f"[ERROR] Error closing serial connection: {err}")

    def read_data(self):
        try:
            if self.serial_conn and self.serial_conn.is_open:
                buffer_data = self.serial_conn.readline().decode('utf-8', 'ignore').strip().split('#')
                if len(buffer_data) > 3:
                    self.buffer.append(buffer_data)
                    self.data = self.buffer[0]
                    if len(self.buffer) > self.buffer_size:
                        self.buffer.pop(0)

        except KeyboardInterrupt:
            print("[INFO] Keyboard Interrupt received. Closing the serial connection safely.")
            self.close_serial_connection()

        except serial.SerialException:
            print("[ERROR] Serial port disconnected. Closing the serial connection safely.")
            self.close_serial_connection()

    def get_data(self):
        try:
            return self.data
        except KeyboardInterrupt:
            print("[INFO] Keyboard Interrupt received. Closing the serial connection safely.")
            self.close_serial_connection()

        except serial.SerialException:
            print("[ERROR] Serial port disconnected. Closing the serial connection safely.")
            self.close_serial_connection()


class WhatsApp(object):
    def __init__(self, headless=False, browser=None, time_out=600):
        # CJM - 20220419: Added time_out=600 to allow the call with less than 600 sec timeout
        # web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}")

        self.BASE_URL = "https://web.whatsapp.com/"
        self.suffix_link = "https://web.whatsapp.com/send?phone={mobile}&text&type=phone_number&app_absent=1"
        self.headless= headless
        if not browser:
            browser = webdriver.Chrome(
                # ChromeDriverManager().install(),
                options=self.chrome_options,
            )

            handles = browser.window_handles
            for _, handle in enumerate(handles):
                if handle != browser.current_window_handle:
                    browser.switch_to.window(handle)
                    browser.close()

        self.browser = browser
        # CJM - 20220419: Added time_out=600 to allow the call with less than 600 sec timeout
        self.wait = WebDriverWait(self.browser, time_out)
        self.cli()
        self.login()
        self.mobile = ""

    @property
    def chrome_options(self):
        chrome_options = Options()
        chrome_options.headless = self.headless
        chrome_options.add_argument(
            "--user-data-dir=" + platformdirs.user_data_dir("alright")
        )
        if sys.platform == "win32":
            chrome_options.add_argument("--profile-directory=Default")
        else:
            chrome_options.add_argument("start-maximized")
        return chrome_options

    def cli(self):
        """
        LOGGER settings  [nCKbr]
        """
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s -- [%(levelname)s] >> %(message)s"
            )
        )
        LOGGER.addHandler(handler)
        LOGGER.setLevel(logging.INFO)

    def login(self):
        self.browser.get(self.BASE_URL)
        self.browser.maximize_window()

    def logout(self):
        prefix = "//div[@id='side']/header/div[2]/div/span/div[3]"
        dots_button = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"{prefix}/div[@role='button']",
                )
            )
        )
        dots_button.click()

        logout_item = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"{prefix}/span/div[1]/ul/li[last()]/div[@role='button']",
                )
            )
        )
        logout_item.click()

    def get_phone_link(self, mobile) -> str:
        """get_phone_link (), create a link based on whatsapp (wa.me) api

        Args:
            mobile ([type]): [description]

        Returns:
            str: [description]
        """
        return self.suffix_link.format(mobile=mobile)

    def catch_alert(self, seconds=3):
        """catch_alert()

        catches any sudden alert
        """
        try:
            WebDriverWait(self.browser, seconds).until(EC.alert_is_present())
            alert = self.browser.switch_to_alert.accept()
            return True
        except Exception as e:
            LOGGER.exception(f"An exception occurred: {e}")
            return False

    def find_user(self, mobile) -> None:
        """find_user()
        Makes a user with a given mobile a current target for the wrapper

        Args:
            mobile ([type]): [description]
        """
        try:
            self.mobile = mobile
            link = self.get_phone_link(mobile)
            self.browser.get(link)
            time.sleep(3)
        except UnexpectedAlertPresentException as bug:
            LOGGER.exception(f"An exception occurred: {bug}")
            time.sleep(1)
            self.find_user(mobile)

    def find_by_username(self, username):
        """find_user_by_name ()

        locate existing contact by username or number

        Args:
            username ([type]): [description]
        """
        search_box = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]',
                )
            )
        )
        search_box.clear()
        search_box.send_keys(username)
        search_box.send_keys(Keys.ENTER)
        try:
            opened_chat = self.browser.find_elements(
                By.XPATH, '//div[@id="main"]/header/div[2]/div[1]/div[1]/span'
            )
            if len(opened_chat):
                title = opened_chat[0].get_attribute("title")
                if title.upper() == username.upper():
                    LOGGER.info(f'Successfully fetched chat "{username}"')
                return True
            else:
                LOGGER.info(f'It was not possible to fetch chat "{username}"')
                return False
        except NoSuchElementException:
            LOGGER.exception(f'It was not possible to fetch chat "{username}"')
            return False

    def username_exists(self, username):
        """username_exists ()

        Returns True or False whether the contact exists or not, and selects the contact if it exists, by checking if the search performed actually opens a conversation with that contact

        Args:
            username ([type]): [description]
        """
        try:
            search_box = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')
                )
            )
            search_box.clear()
            search_box.send_keys(username)
            search_box.send_keys(Keys.ENTER)
            opened_chat = self.browser.find_element(
                By.XPATH,
                "/html/body/div/div[1]/div[1]/div[4]/div[1]/header/div[2]/div[1]/div/span",
            )
            title = opened_chat.get_attribute("title")
            if title.upper() == username.upper():
                return True
            else:
                return False
        except Exception as bug:
            LOGGER.exception(f"Exception raised while finding user {username}\n{bug}")

    def get_first_chat(self, ignore_pinned=True):
        """get_first_chat()  [nCKbr]

        gets the first chat on the list of chats

        Args:
            ignore_pinned (boolean): parameter that flags if the pinned chats should or not be ignored - standard value: True (it will ignore pinned chats!)
        """
        try:
            search_box = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@id="side"]/div[1]/div/div/div/div')
                )
            )
            search_box.click()
            search_box.send_keys(Keys.ARROW_DOWN)
            chat = self.browser.switch_to.active_element
            time.sleep(1)
            if ignore_pinned:
                while True:
                    flag = False
                    for item in chat.find_elements(By.TAG_NAME, "span"):
                        if "pinned" in item.get_attribute("innerHTML"):
                            flag = True
                            break
                    if not flag:
                        break
                    chat.send_keys(Keys.ARROW_DOWN)
                    chat = self.browser.switch_to.active_element

            name = chat.text.split("\n")[0]
            LOGGER.info(f'Successfully selected chat "{name}"')
            chat.send_keys(Keys.ENTER)

        except Exception as bug:
            LOGGER.exception(f"Exception raised while getting first chat: {bug}")

    def search_chat_by_name(self, query: str):
        """search_chat_name()  [nCKbr]

        searches for the first chat containing the query parameter

        Args:
            query (string): query value to be located in the chat name
        """
        try:
            search_box = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@id="side"]/div[1]/div/div/div/div')
                )
            )
            search_box.click()
            search_box.send_keys(Keys.ARROW_DOWN)
            chat = self.browser.switch_to.active_element

            # acceptable here as an exception!
            time.sleep(1)
            flag = False
            prev_name = ""
            name = ""
            while True:
                prev_name = name
                name = chat.text.split("\n")[0]
                if query.upper() in name.upper():
                    flag = True
                    break
                chat.send_keys(Keys.ARROW_DOWN)
                chat = self.browser.switch_to.active_element
                if prev_name == name:
                    break
            if flag:
                LOGGER.info(f'Successfully selected chat "{name}"')
                chat.send_keys(Keys.ENTER)
            else:
                LOGGER.info(f'Could not locate chat "{query}"')
                search_box.click()
                search_box.send_keys(Keys.ESCAPE)

        except Exception as bug:
            LOGGER.exception(f"Exception raised while getting first chat: {bug}")

    def get_list_of_messages(self):
        """get_list_of_messages()

        gets the list of messages in the page
        """
        messages = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="pane-side"]/div[2]/div/div/child::div')
            )
        )

        clean_messages = []
        for message in messages:
            _message = message.text.split("\n")
            if len(_message) == 2:
                clean_messages.append(
                    {
                        "sender": _message[0],
                        "time": _message[1],
                        "message": "",
                        "unread": False,
                        "no_of_unread": 0,
                        "group": False,
                    }
                )
            elif len(_message) == 3:
                clean_messages.append(
                    {
                        "sender": _message[0],
                        "time": _message[1],
                        "message": _message[2],
                        "unread": False,
                        "no_of_unread": 0,
                        "group": False,
                    }
                )
            elif len(_message) == 4:
                clean_messages.append(
                    {
                        "sender": _message[0],
                        "time": _message[1],
                        "message": _message[2],
                        "unread": _message[-1].isdigit(),
                        "no_of_unread": int(_message[-1])
                        if _message[-1].isdigit()
                        else 0,
                        "group": False,
                    }
                )
            elif len(_message) == 5:
                clean_messages.append(
                    {
                        "sender": _message[0],
                        "time": _message[1],
                        "message": "",
                        "unread": _message[-1].isdigit(),
                        "no_of_unread": int(_message[-1])
                        if _message[-1].isdigit()
                        else 0,
                        "group": True,
                    }
                )
            elif len(_message) == 6:
                clean_messages.append(
                    {
                        "sender": _message[0],
                        "time": _message[1],
                        "message": _message[4],
                        "unread": _message[-1].isdigit(),
                        "no_of_unread": int(_message[-1])
                        if _message[-1].isdigit()
                        else 0,
                        "group": True,
                    }
                )
            else:
                LOGGER.info(f"Unknown message format: {_message}")
        return clean_messages

    def check_if_given_chat_has_unread_messages(self, query):
        """check_if_given_chat_has_unread_messages() [nCKbr]

        identifies if a given chat has unread messages or not.

        Args:
            query (string): query value to be located in the chat name
        """
        try:
            list_of_messages = self.get_list_of_messages()
            for chat in list_of_messages:
                if query.upper() == chat["sender"].upper():
                    if chat["unread"]:
                        LOGGER.info(
                            f'Yup, {chat["no_of_unread"]} new message(s) on chat <{chat["sender"]}>.'
                        )
                        return True
                    LOGGER.info(f'There are no new messages on chat "{query}".')
                    return False
            LOGGER.info(f'Could not locate chat "{query}"')

        except Exception as bug:
            LOGGER.exception(f"Exception raised while getting first chat: {bug}")

    def send_message1(self, mobile: str, message: str) -> str:
        # CJM - 20220419:
        #   Send WhatsApp Message With Different URL, NOT using https://wa.me/ to prevent WhatsApp Desktop to open
        #   Also include the Number we want to send to
        #   Send Result
        #   0 or Blank or NaN = Not yet sent
        #   1 = Sent successfully
        #   2 = Number to short
        #   3 = Error or Failure to Send Message
        #   4 = Not a WhatsApp Number
        try:
            # Browse to a "Blank" message state
            self.browser.get(f"https://web.whatsapp.com/send?phone={mobile}&text")

            # This is the XPath of the message textbox
            inp_xpath = (
                '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
            )
            # This is the XPath of the "ok button" if the number was not found
            nr_not_found_xpath = (
                '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div'
            )

            # If the number is NOT a WhatsApp number then there will be an OK Button, not the Message Textbox
            # Test for both situations -> find_elements returns a List
            ctrl_element = self.wait.until(
                lambda ctrl_self: ctrl_self.find_elements(By.XPATH, nr_not_found_xpath)
                or ctrl_self.find_elements(By.XPATH, inp_xpath)
            )
            msg = "0"  # Not yet sent
            # Iterate through the list of elements to test each if they are a textBox or a Button
            for i in ctrl_element:
                if i.get_attribute("role") == "textbox":
                    # This is a WhatsApp Number -> Send Message

                    for line in message.split("\n"):
                        i.send_keys(line)
                        ActionChains(self.browser).key_down(Keys.SHIFT).key_down(
                            Keys.ENTER
                        ).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
                    i.send_keys(Keys.ENTER)

                    msg = f"1 "  # Message was sent successfully
                    # Found alert issues when we send messages too fast, so I called the below line to catch any alerts
                    self.catch_alert()

                elif i.get_attribute("role") == "button":
                    # Did not find the Message Text box
                    # BUT we possibly found the XPath of the error "Phone number shared via url is invalid."
                    if i.text == "OK":
                        # This is NOT a WhatsApp Number -> Press enter and continue
                        i.send_keys(Keys.ENTER)
                        msg = f"4 "  # Not a WhatsApp Number

        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"An exception occurred: {bug}")
            msg = f"3 "

        finally:
            LOGGER.info(f"{msg}")
            return msg

    def send_message(self, message):
        """send_message ()
        Sends a message to a target user

        Args:
            message ([type]): [description]
        """
        try:
            inp_xpath = (
                '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
            )
            input_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, inp_xpath))
            )
            for line in message.split("\n"):
                input_box.send_keys(line)
                ActionChains(self.browser).key_down(Keys.SHIFT).key_down(
                    Keys.ENTER
                ).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
            input_box.send_keys(Keys.ENTER)
            LOGGER.info(f"Message sent successfuly to {self.mobile}")
        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"Failed to send a message to {self.mobile} - {bug}")
            LOGGER.info("send_message() finished running!")

    def send_direct_message(self, mobile: str, message: str, saved: bool = True):
        if saved:
            self.find_by_username(mobile)
        else:
            self.find_user(mobile)
        self.send_message(message)

    def find_attachment(self):
        clipButton = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/footer//*[@data-icon="attach-menu-plus"]/..')
            )
        )
        clipButton.click()

    def send_attachment(self):
        # Waiting for the pending clock icon to disappear
        self.wait.until_not(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]//*[@data-icon="msg-time"]')
            )
        )

        sendButton = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span",
                )
            )
        )
        sendButton.click()

        # Waiting for the pending clock icon to disappear again - workaround for large files or loading videos.
        # Appropriate solution for the presented issue. [nCKbr]
        self.wait.until_not(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]//*[@data-icon="msg-time"]')
            )
        )

    def send_picture(self, picture, message):
        """send_picture ()

        Sends a picture to a target user

        Args:
            picture ([type]): [description]
        """
        try:
            filename = os.path.realpath(picture)
            print(filename)
            self.find_attachment()
            # To send an Image
            imgButton = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="main"]/footer//*[@data-icon="attach-image"]/../input',
                    )
                )
            )
            imgButton.send_keys(filename)
            inp_xpath = '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div'
            input_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, inp_xpath))
            )
            for line in message.split("\n"):
                input_box.send_keys(line)
                ActionChains(self.browser).key_down(Keys.SHIFT).key_down(
                    Keys.ENTER
                ).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
            self.send_attachment()
            LOGGER.info(f"Picture has been successfully sent to {self.mobile}")
        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"Failed to send a message to {self.mobile} - {bug}")
        finally:
            LOGGER.info("send_picture() finished running!")

    def convert_bytes(self, size) -> str:
        # CJM - 2022/06/10:
        # Convert bytes to KB, or MB or GB
        for x in ["bytes", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0

    def convert_bytes_to(self, size, to):
        # CJM - 2022 / 06 / 10:
        # Returns Bytes as 'KB', 'MB', 'GB', 'TB'
        conv_to = to.upper()
        if conv_to in ["BYTES", "KB", "MB", "GB", "TB"]:
            for x in ["BYTES", "KB", "MB", "GB", "TB"]:
                if x == conv_to:
                    return size
                size /= 1024.0

    def send_video(self, video):
        """send_video ()
        Sends a video to a target user
        CJM - 2022/06/10: Only if file is less than 14MB (WhatsApp limit is 15MB)

        Args:
            video ([type]): the video file to be sent.
        """
        try:
            filename = os.path.realpath(video)
            f_size = os.path.getsize(filename)
            x = self.convert_bytes_to(f_size, "MB")
            if x < 14:
                # File is less than 14MB
                self.find_attachment()
                # To send a Video
                video_button = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="main"]/footer//*[@data-icon="attach-image"]/../input',
                        )
                    )
                )

                video_button.send_keys(filename)

                self.send_attachment()
                LOGGER.info(f"Video has been successfully sent to {self.mobile}")
            else:
                LOGGER.info(f"Video larger than 14MB")
        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"Failed to send a message to {self.mobile} - {bug}")
        finally:
            LOGGER.info("send_video() finished running!")

    def send_file(self, filename):
        """send_file()

        Sends a file to target user

        Args:
            filename ([type]): [description]
        """
        try:
            filename = os.path.realpath(filename)
            self.find_attachment()
            document_button = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="main"]/footer//*[@data-icon="attach-document"]/../input',
                    )
                )
            )
            document_button.send_keys(filename)
            self.send_attachment()
        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"Failed to send a file to {self.mobile} - {bug}")
        finally:
            LOGGER.info("send_file() finished running!")

    def close_when_message_successfully_sent(self):
        """close_when_message_successfully_sent() [nCKbr]

        Closes the browser window to allow repeated calls when message is successfully sent/received.
        Ideal for recurrent/scheduled messages that would not be sent if a browser is already opened.
        [This may get deprecated when an opened browser verification gets implemented, but it's pretty useful now.]

        Friendly contribution by @euriconicacio.
        """

        LOGGER.info("Waiting for message status update to close browser...")
        try:
            # Waiting for the pending clock icon shows and disappear
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="main"]//*[@data-icon="msg-time"]')
                )
            )
            self.wait.until_not(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="main"]//*[@data-icon="msg-time"]')
                )
            )
        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"Failed to send a message to {self.mobile} - {bug}")
        finally:
            self.browser.close()
            LOGGER.info("Browser closed.")

    def get_last_message_received(self, query: str):
        """get_last_message_received() [nCKbr]

        fetches the last message receive in a given chat, along with couple metadata, retrieved by the "query" parameter provided.

        Args:
            query (string): query value to be located in the chat name
        """
        try:
            if self.find_by_username(query):
                self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//div[@id="main"]/div[3]/div[1]/div[2]/div[3]/child::div[contains(@class,"message-in") or contains(@class,"message-out")][last()]',
                        )
                    )
                )

                time.sleep(
                    3
                )  # clueless on why the previous wait is not respected - we need this sleep to load tha list.

                list_of_messages = self.wait.until(
                    EC.presence_of_all_elements_located(
                        By.XPATH,
                        '//div[@id="main"]/div[3]/div[1]/div[2]/div[3]/child::div[contains(@class,"message-in")]',
                    )
                )

                if len(list_of_messages) == 0:
                    LOGGER.exception(
                        "It was not possible to retrieve the last message - probably it does not exist."
                    )
                else:
                    msg = list_of_messages[-1]

                    is_default_user = self.wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//div[@id="main"]/header/div[1]/div[1]/div[1]/span',
                            )
                        )
                    ).get_attribute("data-testid")
                    if is_default_user == "default-user":
                        msg_sender = query
                    else:
                        msg_sender = msg.text.split("\n")[0]

                    if len(msg.text.split("\n")) > 1:
                        when = msg.text.split("\n")[-1]
                        msg = (
                            msg.text.split("\n")
                            if "media-play" not in msg.get_attribute("innerHTML")
                            else "Video or Image"
                        )
                    else:
                        when = msg.text.split("\n")[0]
                        msg = "Non-text message (maybe emoji?)"

                    header_group = self.wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//div[@id="main"]/header/div[1]/div[1]/div[1]/span',
                            )
                        )
                    )
                    header_text = self.wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//div[@id="main"]/header/div[2]/div[2]/span')
                        )
                    )

                    if (
                        header_group.get_attribute("data-testid") == "default-group"
                        and msg_sender.strip() in header_text.text
                    ):
                        LOGGER.info(f"Message sender: {msg_sender}.")
                    elif (
                        msg_sender.strip() != msg[0].strip()
                    ):  # it is not a messages combo
                        LOGGER.info(f"Message sender: {msg_sender}.")
                    else:
                        LOGGER.info(
                            f"Message sender: retrievable from previous messages."
                        )

                    # DISCLAIMER: messages answering other messages carry the previous ones in the text.
                    # Example: Message text: ['John', 'Mary', 'Hi, John!', 'Hi, Mary! How are you?', '14:01']
                    # TODO: Implement 'filter_answer' boolean paramenter to sanitize this text based on previous messages search.

                    LOGGER.info(f"Message text: {msg}.")
                    LOGGER.info(f"Message time: {when}.")

        except Exception as bug:
            LOGGER.exception(f"Exception raised while getting first chat: {bug}")

    def fetch_all_unread_chats(self, limit=True, top=50):
        """fetch_all_unread_chats()  [nCKbr]

        retrieve all unread chats.

        Args:
            limit (boolean): should we limit the counting to a certain number of chats (True) or let it count it all (False)? [default = True]
            top (int): once limiting, what is the *approximate* number of chats that should be considered? [generally, there are natural chunks of 10-22]

        DISCLAIMER: Apparently, fetch_all_unread_chats functionallity works on most updated browser versions
        (for example, Chrome Version 102.0.5005.115 (Official Build) (x86_64)). If it fails with you, please
        consider updating your browser while we work on an alternative for non-updated broswers.

        """
        try:
            counter = 0
            pane = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@id="pane-side"]/div[2]')
                )
            )
            list_of_messages = self.get_list_of_messages()
            read_names = []
            names = []
            names_data = []

            while True:
                last_counter = counter
                for item in list_of_messages:
                    name = item["sender"]
                    if name not in read_names:
                        read_names.append(name)
                        counter += 1
                    if item["unread"]:
                        if name not in names:
                            names.append(name)
                            names_data.append(item)

                pane.send_keys(Keys.PAGE_DOWN)
                pane.send_keys(Keys.PAGE_DOWN)

                list_of_messages = self.get_list_of_messages()
                if (
                    last_counter == counter
                    and counter
                    >= int(
                        self.wait.until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//div[@id="pane-side"]/div[2]')
                            )
                        ).get_attribute("aria-rowcount")
                    )
                    * 0.9
                ):
                    break
                if limit and counter >= top:
                    break

                LOGGER.info(f"The counter value at this chunk is: {counter}.")

            if limit:
                LOGGER.info(
                    f"The list of unread chats, considering the first {counter} messages, is: {names}."
                )
            else:
                LOGGER.info(f"The list of all unread chats is: {names}.")
            return names_data

        except Exception as bug:
            LOGGER.exception(f"Exception raised while getting first chat: {bug}")
            return []