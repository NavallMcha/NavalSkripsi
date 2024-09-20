import os
import time
import datetime
import cv2
from dotenv import load_dotenv
from utility import telegram_client
from utility.data import YAMLDataHandler
from utility.logger import Logger as log

load_dotenv()

if __name__ == '__main__':
    token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('BOT_ID').split()
    raspberry_ip = os.getenv('RASPBERRY_IP')
    client = telegram_client.TelegramClient(token)
    data_handler = YAMLDataHandler("out/hands-output-data.yaml")
    image_path = "out/hands-output-image.png"

    area_state_before = {}
    area_state_now = {}
    data_handler_buffer = data_handler.read()
    if data_handler_buffer is not None:
        area_state = data_handler_buffer["area_state"]
        for index, (key, value) in enumerate(area_state.items()):
            area_state_before[f"{key}"] = value

    # for ids in chat_id:
    #     if os.path.exists(image_path):
    #         current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         client.send_imagecv2(ids, cv2.imread(image_path))
    #         client.send_message(ids, f"[INFO] {current_datetime} Tangan Terdeteksi")
    #     log.loginfo("Done")

    while True:
        data_handler_buffer = data_handler.read()
        if data_handler_buffer is not None:
            try:
                area_state = data_handler_buffer["area_state"]
                for index, (key, value) in enumerate(area_state.items()):
                    area_state_now[f"{key}"] = value
                    if area_state_now[f"{key}"] != area_state_before[f"{key}"]:
                        area_state_before[f"{key}"] = area_state_now[f"{key}"]
                        area_now = area_state_now[f"{key}"]
                        if area_now:
                            for ids in chat_id:
                                try:
                                    if os.path.exists(image_path):
                                        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        client.send_imagecv2(ids, cv2.imread(image_path))
                                        client.send_message(ids,
                                                            f"[INFO] {current_datetime} Hands Detected on Artwork {index}")
                                        log.logdebug("Image Sent")
                                except Exception as e:
                                    print(e)
            except Exception as e:
                log.logerr(e)
