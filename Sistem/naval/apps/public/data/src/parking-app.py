import asyncio
import datetime
import random
import threading
import os

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

load_dotenv()
raspberry_ip = os.getenv('RASPBERRY_IP')
HTTP_LINKS = f'http://{raspberry_ip}:5000'


def st_main_app():
    st.set_page_config(
        page_title="Polinema Parking",
        page_icon=":bar_chart:",
        layout="wide"
    )
    st_sidebar_main()
    st.title("Polinema Parking Detection")
    st.markdown("---")
    iframe_code = f'<iframe src="{HTTP_LINKS.strip()}" width="{720}" height="{830}" frameborder="0"></iframe>'
    components.html(iframe_code, height=830, width=720)


def st_sidebar_main():
    st.sidebar.markdown("---")
    st.sidebar.subheader("Parking Detection Sidebar")
    sidebar_option = ["Home", "History", "Export"]
    sidebar_option_icon = ["house", "clock-history", "archive"]
    with st.sidebar:
        sidebar_selected = option_menu(
            menu_title="Menu",
            options=sidebar_option,
            icons=sidebar_option_icon,
            orientation="vertical"
        )
    return sidebar_selected


if __name__ == '__main__':
    st_main_app()
