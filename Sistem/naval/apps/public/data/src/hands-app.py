import asyncio
import datetime
import random
import threading
import os
import pyautogui

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from dotenv import load_dotenv
from utility.timer import TimerTicks
from streamlit_js_eval import streamlit_js_eval

from utility.logger import Logger as log
from utility.data import YAMLDataHandler
from streamlit_modal import Modal
from streamlit_custom_notification_box import custom_notification_box

# konfigurasi start -------------------------
load_dotenv()
raspberry_ip = os.getenv('RASPBERRY_IP')

# defines macros
HTTP_LINKS = f'http://{raspberry_ip}:5000'
DEFAULT_IMAGES = "data/hands/hands-output-image.jpg"
DEFAULT_VIDEOS = "data/hands/hands-output-video.mp4"


# konfigurasi end -------------------------


class MainUI:
    def __init__(self):
        # inisialisasi data start -------------------------
        self.data_handler = YAMLDataHandler("out/hands-output-data.yaml")
        self.param_data_handler = YAMLDataHandler("out/hands-output-param.yaml")
        self.log_data_handler = YAMLDataHandler("out/hands-output-log.yaml")
        # inisialisasi data end -------------------------
        # inisialisasi variabel start -------------------------
        self.warning_modal = None
        self.loop = None
        self.status_text = None
        self.status_index = None
        self.status_fps = None
        # inisialisasi variabel end -------------------------

    async def st_main_app(self):
        # web utama start -------------------------
        st.title("Museum Security System")
        st.sidebar.title("Museum Security System Sidebar")
        app_menu = st.sidebar.selectbox("App Menu", ["Main Menu", "Reports"])
        if app_menu == "Main Menu":
            # app_detection_camera = st.sidebar.selectbox("Cameras", ["Camera 1", "Camera 2"])
            app_detection_camera = "Camera 1"
            # app_detection_confidence = st.sidebar.slider("Min Detection Confidence", min_value=0.0, max_value=100.0, value=10.0)
            app_detection_confidence = 10.0
            # konfigurasi kecerahan dan kontrast start -------------------------
            app_detection_brightness = st.sidebar.slider("Set Brightness Value", min_value=0.0, max_value=100.0,
                                                         value=0.0)
            app_detection_contrast = st.sidebar.slider("Set Contrast Value", min_value=0.0, max_value=100.0, value=0.0)
            param_handler_read = self.param_data_handler.read()
            if param_handler_read is not None:  # pengiriman data ke yaml
                app_detection_camera = 0 if app_detection_camera == "Camera 1" else 1
                self.param_data_handler.update("confidence", app_detection_confidence)
                self.param_data_handler.update("brightness", app_detection_brightness)
                self.param_data_handler.update("contrast", app_detection_contrast)
                self.param_data_handler.update("camera", app_detection_camera)
            else:
                parameters_set = {
                    "confidence": app_detection_confidence,
                    "brightness": app_detection_brightness,
                    "contrast": app_detection_contrast
                }
                self.param_data_handler.write(parameters_set)
            # inisialisasi variabel end -------------------------
            st.set_option("deprecation.showfileUploaderEncoding", False)
            st.markdown("---")
            # video frame start -------------------------
            iframe_code = f'<iframe src="{HTTP_LINKS.strip()}" width="100%" height="{480}" frameborder="0"></iframe>'
            components.html(iframe_code, height=480)
            st.markdown("---")
            # video frame end -------------------------
        # menu report atau history atau log start -------------------------
        elif app_menu == "Reports":
            btn_delete_log = st.sidebar.button("Delete Log")
            if btn_delete_log:
                log_init = {
                    "log": []
                }
                self.log_data_handler.write(log_init)
                self.delete_all_images_in_folder("out/log")
            log_handler = self.log_data_handler.read()
            if log_handler is not None:
                log_buffer = log_handler["log"]
                # sorted_log = sorted(log_buffer, key=lambda x: x['epoch'])
                # sorted_formatted_log = []
                st.markdown("---")
                index_title_col, epoch_title_col, area_title_col, images_title_col = st.columns(4)
                with index_title_col:
                    st.write("Number")
                with epoch_title_col:
                    st.write("Time")
                with area_title_col:
                    st.write("on Area")
                with images_title_col:
                    st.write("Images")
                st.markdown("---")
                for logs_index, logs in enumerate(log_buffer):  # sorted log
                    index_col, epoch_col, area_col, images_col = st.columns(4)
                    with index_col:
                        st.text(logs_index + 1)
                    with epoch_col:
                        epoch = datetime.datetime.fromtimestamp(logs["epoch"]).strftime('%Y-%m-%d %H:%M:%S')
                        st.text(epoch)
                    with area_col:
                        st.text(f"Area {logs['data']['area']}")
                    with images_col:
                        st.image(f"out/log/hands-output-image-{logs['epoch']}.png")
                    st.markdown("---")
        st.sidebar.markdown("---")
        # menu report atau history atau log end -------------------------

    async def update_realtime_data(self):
        # informasi fps, dll tapi ga kepake dan notif start -------------------------
        toast_time = TimerTicks()
        toast_time.begin(200)
        state_value_before = [0, 0, 0]
        state_value_now = [0, 0, 0]
        state_all_before = False
        state_to_closed = False
        await asyncio.sleep(1.0)
        while True:
            data_handler_read = self.data_handler.read()
            if data_handler_read is not None:
                if toast_time.tick():
                    try:
                        for index, (key, value) in enumerate(data_handler_read["area_state"].items()):
                            state_value_now[index] = value
                            if state_value_now[index] != state_value_before[index]:
                                state_value_before[index] = state_value_now[index]
                                if state_value_now[index]:
                                    pass
                                    # st.toast(f"Warning Hands on Artwork {index}", icon="⚠️")
                        state_all = bool(int(data_handler_read['state']))
                        # if state_all:
                        #     state_to_closed = True
                        # if state_to_closed:
                        # log.loginfo("hai")
                        # if state_to_closed:
                        #     self.warning_modal = Modal("Warning ⚠️", key=f"modal-key", max_width=400)
                        #     if not self.warning_modal.is_open():
                        #         self.warning_modal.open()
                        #     if self.warning_modal.is_open():
                        #         with self.warning_modal.container():
                        #             # st.subheader("Hands on Artwork")
                        #             st.write("Please check for artwork !")
                        #             st.image("out/hands-output-image.png")
                        #             close = st.button("Closed")
                        #             if close:
                        #                 log.logwarn("closed")
                        #                 pyautogui.hotkey("ctrl", "F5")
                        #                 # streamlit_js_eval(js_expressions="parent.window.location.reload()")
                        #                 break

                        if state_all != state_all_before:
                            state_all_before = state_all
                            if state_all:
                                self.warning_modal = Modal("Warning ⚠️", key=f"modal-key", max_width=400)
                                if not self.warning_modal.is_open():
                                    self.warning_modal.open()
                                if self.warning_modal.is_open():
                                    with self.warning_modal.container():
                                        # st.subheader("Hands on Artwork")23
                                        st.write("Please check for artwork !")
                                        st.image("out/hands-output-image.png")
                                        close = st.button("Closed")
                                        if close:
                                            log.logwarn("closed")
                                            pyautogui.hotkey("ctrl", "F5")
                                            # streamlit_js_eval(js_expressions="parent.window.location.reload()")
                                            break
                    except Exception as e:
                        log.logsilent(e)
                # informasi fps, dll tapi ga kepake dan notif end -------------------------
            await asyncio.sleep(0.25)
        log.logerr("restarted")
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

    @staticmethod
    def delete_all_images_in_folder(folder_path):
        # fungsi untuk hapus logs start -------------------------
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                file_path = os.path.join(folder_path, filename)
                os.remove(file_path)
                # fungsi untuk hapus logs end -------------------------


async def main():
    # memanggil fungsi utama -------------------------
    ui = MainUI()
    main_task = asyncio.create_task(ui.st_main_app())
    data_task = asyncio.create_task(ui.update_realtime_data())
    await asyncio.gather(main_task, data_task)
    # memanggil fungsi utama -------------------------


if __name__ == '__main__':
    # memulai fungsi utama -------------------------
    asyncio.run(main())
