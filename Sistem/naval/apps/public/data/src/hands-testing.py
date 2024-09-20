import cv2
import os
import time
import random
import numpy as np

from modules.image import Vision
from modules.utils import Drawing
from utility.timer import TimerTicks
from utility.data import YAMLDataHandler
from modules.routine import ImgRex as Yolo
from utility.logger import Logger as log

if __name__ == '__main__':
    log.loginfo("Main Initialize")
    cam = Vision(isUsingCam=True, addr="data/hands/hands-video.mp4", index=0, device="windows")
    cam.writeConfig("out/hands-output-video.mp4")
    yolo = Yolo()
    # yolo.load(
    #     names="data/hands/hands-10.txt",
    #     weight="data/hands/hands-10.pt"
    # )
    yolo.load(
        weight_path="data/hands/hands-cross-tiny-prn.weights",
        cfg="data/hands/hands-cross-tiny-prn.cfg",
        classes="data/hands/hands-cross-tiny-prn.txt"
    )
    while True:
        try:
            frame = cam.read(frame_size=0, show_fps=True)
            detect = yolo.predict(frame)
            yolo.draw(frame, detect)
            cam.show(frame, "frame")
            if cam.wait(1) == ord('q'):
                break
        except Exception as err:
            log.logerr(err)

# import streamlit as st
# from streamlit_autorefresh import st_autorefresh
#
# # Run the autorefresh about every 2000 milliseconds (2 seconds) and stop
# # after it's been refreshed 100 times.
# count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")
#
# # The function returns a counter for number of refreshes. This allows the
# # ability to make special requests at different intervals based on the count
# if count == 0:
#     st.write("Count is zero")
# elif count % 3 == 0 and count % 5 == 0:
#     st.write("FizzBuzz")
# elif count % 3 == 0:
#     st.write("Fizz")
# elif count % 5 == 0:
#     st.write("Buzz")
# else:
#     st.write(f"Count: {count}")
