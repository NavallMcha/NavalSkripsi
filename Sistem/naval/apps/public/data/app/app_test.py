import streamlit as st
import pandas as pd
import time
import numpy as np

from matplotlib import pyplot as plt
from sys import exit
from typing import Callable, NoReturn

f: Callable[..., NoReturn] = exit

# remove hamburger menu
# episode 0 ------------------------------------------------

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer > a {visibility: hidden; display: none}
                footer:after {content : "iMake"; color: red}

                header {visibility: hidden;}
                </style>
                <h1>Hwehwehwehwehwe</h1>
"""

hide_hamburger = """
<style>
.css-1rs6os.edgvbvh3 
{
    visibility: hidden;
}
.css-1lsmgbg.egzxvld0
{
    visibility: hidden;
}
</style>
    """

# st.markdown(hide_st_style, unsafe_allow_html=True)

# episode 1 ------------------------------------------------
# st.title("Ini Title")
# st.header("Ini Header")
# st.subheader("Ini Sub Header")
# st.text("Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia")
# st.markdown("---")
# st.markdown("[Github](https://github.com/)")
# st.caption("Ini Caption")


# episode 2 ------------------------------------------------
table = pd.DataFrame({"value1": [1, 2, 3, 4, 5, 6], "value2": [11, 12, 13, 14, 15, 16]})
# json_val = {"value1": 20}
# st.code("print('Hello')")
# st.metric(label="Speed", value="120m/s", delta="1.4ms")
# st.table(table)
# st.dataframe(table)

# episode 3 ------------------------------------------------
# st.image(image="", caption="")
# st.audio()
# st.video()

# episode 4 ------------------------------------------------
# def onChange():
#     print(f"onCheckboxChange: {st.session_state.checker}")
#
#
# state = st.checkbox("checkbox", value=True, on_change=onChange, key="checker")
# # if state:
# #     st.write("Hi")
# # else:
# #     pass
# radio = st.radio("Radio", options=("Satu", "Dua", "Tiga"))
# print(f"onRadioChanged: {radio}")
#
#
# def onClick():
#     print(f"onClicked")
#
#
# button = st.button("Click Me!", on_click=onClick)
# select = st.selectbox("Select !", options=("Satu", "Dua", "Tiga"))
# print(f"onSelectBox: {select}")
#
# multi_select = st.multiselect("Multi Select !", options=("Satu", "Dua", "Tiga"))
# print(f"onMultiSelectChanged: {multi_select}")

# episode 5 ------------------------------------------------

# st.title("Uploading Files Photo")
# image = st.file_uploader("Please Upload an Image", type=["png", "jpg"], accept_multiple_files=True)
# if image is not None:
#     st.image(image)
#
# st.title("Uploading Files Video")
# video = st.file_uploader("Please Upload an Video", type=["mp4", "mkv"])
# if video is not None:
#     st.video(video)

# slider = st.slider("This is Slider", min_value=0, max_value=200, value=100)
# print(f"onSliderChanged: {slider}")
#
# text_input = st.text_input("Enter Title: ", max_chars=20)
# print(f"onTextInput: {text_input}")
#
# time_input = st.time_input("Set Timer")
# print(f"onTimeInput: {time_input}")

# bar = st.progress(0)
# for i in range(100):
#     bar.progress(i)
#     time.sleep(0.1)

# episode 6 ------------------------------------------------
# st.markdown("<h1 style='text-align: center;'> Hwhewhehwehw </h1>", unsafe_allow_html=True)
# with st.form("Forms", clear_on_submit=True):
#     col1, col2 = st.columns(2)
#     f_name = col1.text_input("First Name")
#     l_name = col2.text_input("Second Name")
#     st.text_input("Email")
#     st.text_input("Password")
#     st.text_input("Confirm Pass")
#     day, month, year = st.columns(3)
#     day.text_input("Day")
#     month.text_input("Month")
#     year.text_input("Year")
#     s_state = st.form_submit_button("Submit")
#     if s_state:
#         if f_name == "" and l_name == "":
#             st.warning("Isi Blok")
#         else:
#             st.success("Yes Hore")

# episode 7 ------------------------------------------------
# st.sidebar.write("Yesyes")
# fig = plt.figure()
# plt.plot()

st.sidebar.radio("Beranda", options=["YES"])

