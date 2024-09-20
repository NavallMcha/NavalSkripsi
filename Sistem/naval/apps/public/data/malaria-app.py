import asyncio
import datetime
import random
import threading
import os
import time

import cv2

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from dotenv import load_dotenv
from utility.timer import TimerTicks
from streamlit_js_eval import streamlit_js_eval
from streamlit_option_menu import option_menu

from utility.logger import Logger as log
from utility.data import YAMLDataHandler
from streamlit_modal import Modal
from streamlit_custom_notification_box import custom_notification_box
from modules.routine import ImgRex as Yolov3

from sys import exit
from typing import Callable, NoReturn
import io
import base64
from roboflow import Roboflow
import tempfile

f: Callable[..., NoReturn] = exit


def st_main_app():
    st.set_page_config(
        page_title="Malaria Detection",
        page_icon="🏥",
        layout="wide"
    )
    hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer > a {visibility: hidden; display: none}
                    footer:after {content : "Iwan Dwi"; color: red}
                    header {visibility: hidden;}
                    </style>
                    <h1>Malaria Detection Home</h1>
                    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    sidebar_choices = st_sidebar_main()
    if sidebar_choices == "Home":
        st.sidebar.write("Preview Original Images")
        sub_sidebar_choices = st_sidebar_sub_main()
        image_file = st.file_uploader("Upload an Image", type=['jpg', 'png', 'jpeg'])
        if not image_file:
            st.error("No pictures have been uploaded")
            return None
        else:
            st.success("Image upload successful")
        original_image = Image.open(image_file)
        original_image = np.array(original_image.convert('RGB'))
        original_image = image_change_brightness(original_image, sub_sidebar_choices["param_brightness_amount"])
        original_image = image_change_blur(original_image, sub_sidebar_choices["param_blur_rate"])
        if sub_sidebar_choices["param_apply_enhancement_filter"]:
            original_image = image_change_details(original_image)
        original_image = image_resize(original_image, 480)
        height, width, channels = original_image.shape

        yolo = Yolov3()
        yolo.load("data/malaria/rbc7_yolov3_testing.weights",
                  "data/malaria/rbc7_yolov3_testing.cfg",
                  "data/malaria/rbc7_yolov3_testing.txt")

        # rf = Roboflow(api_key="fJGrgUi1rP8znwkUe4e5")
        # project = rf.workspace().project("malaria-detection-4dn5i")
        # model = project.version(5).model
        # with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as raw_image_temp_file:
        #     cv2.imwrite(raw_image_temp_file.name, original_image)
        # result_prediction = model.predict(raw_image_temp_file.name, confidence=40, overlap=30)
        # with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as result_image_temp_file:
        #     result_prediction.save(result_image_temp_file.name)
        # saved_image = cv2.imread(result_image_temp_file.name)
        # st.image(saved_image)

        detect = yolo.predict(original_image)
        infected_data = [data for data in detect if data["class"] == "infected"]
        not_infected_data = [data for data in detect if data["class"] == "not infected"]

        st.markdown("---")
        processed_image = original_image.copy()
        yolo.draw(processed_image, detect)
        st.image([processed_image])
        infected_col, not_infected_col = st.columns(2)
        with infected_col:
            st.markdown("---")
            st.write(f"Infected Count: {len(infected_data)}")
            if infected_data:
                processed_infected_image = original_image.copy()
                yolo.draw(processed_infected_image, infected_data)
                st.image([processed_infected_image])
            else:
                st.image([original_image])

        with not_infected_col:
            st.markdown("---")
            st.write(f"Not Infected Count: {len(not_infected_data)}")
            if not_infected_data:
                processed_not_infected_image = original_image.copy()
                yolo.draw(processed_not_infected_image, not_infected_data)
                st.image([processed_not_infected_image])
            else:
                st.image([original_image])

        st.sidebar.markdown("---")
        st.sidebar.write("Raw Images")
        st.sidebar.image([original_image])

        image_to_download = Image.fromarray(np.array(processed_image))

        img_bytes = io.BytesIO()
        image_to_download.save(img_bytes, format="JPEG")
        img_bytes = img_bytes.getvalue()

        b64 = base64.b64encode(img_bytes).decode()
        href = f'<a href="data:file/jpg;base64,{b64}" download="images-{time.time()}.jpg">Download Image</a>'
        st.markdown(href, unsafe_allow_html=True)

        # os.remove(raw_image_temp_file.name)
        # os.remove(result_image_temp_file.name)


def st_sidebar_main():
    # sidebar_option = ["Home", "History", "Export"]
    # sidebar_option_icon = ["house", "clock-history", "archive"]
    sidebar_option = ["Home"]
    sidebar_option_icon = ["house"]
    with st.sidebar:
        sidebar_selected = option_menu(
            menu_title="Menu",
            options=sidebar_option,
            icons=sidebar_option_icon,
            orientation="vertical"
        )
    return sidebar_selected


def st_sidebar_sub_main():
    param_blur_rate = st.sidebar.slider(
        "Change Image Blurring Value", min_value=0.5, max_value=3.5)
    param_brightness_amount = st.sidebar.slider(
        "Change Brightness and Contrast Value", min_value=-50, max_value=50, value=0)
    param_apply_enhancement_filter = st.sidebar.checkbox('Apply Enhance Image')
    return {
        "param_blur_rate": param_blur_rate,
        "param_brightness_amount": param_brightness_amount,
        "param_apply_enhancement_filter": param_apply_enhancement_filter
    }


def image_change_brightness(image, amount):
    images_return = cv2.convertScaleAbs(image, beta=amount)
    return images_return


def image_change_blur(image, amount):
    images_return = cv2.GaussianBlur(image, (11, 11), amount)
    return images_return


def image_change_details(processed_image):
    images_return = cv2.detailEnhance(processed_image, sigma_s=12, sigma_r=0.15)
    return images_return


def image_resize(image, width=None, height=None,
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


def get_binary_file_downloader_html(bin_data, file_label='File', key=None):
    bin_str = base64.b64encode(bin_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">Download {file_label}</a>'
    return href


if __name__ == '__main__':
    st_main_app()
