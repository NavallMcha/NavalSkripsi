import threading

import cv2
import os
import time
import pygame
import random
import numpy as np
import datetime

from dotenv import load_dotenv
from modules.image import Vision
from modules.utils import Drawing
from utility.timer import TimerTicks
from utility.data import YAMLDataHandler
from modules.routine import ImgBuster as Yolo
from flask import Flask, Response, redirect
from utility.logger import Logger as log

load_dotenv()
raspberry_ip = os.getenv('RASPBERRY_IP')
app = Flask(__name__)


def generate_frames():
    log.loginfo("Main Initialize")
    cam = Vision(isUsingCam=False, addr="data/parking/cctv/parking9.mp4", index=0, device="windows")
    cam2 = Vision(isUsingCam=False, addr="data/parking/cctv2/parking6.mp4", index=0, device="windows")
    cam.writeConfig("out/parking-output-video.mp4")
    cam2.writeConfig("out/parking-output-video2.mp4")
    yolo = Yolo()
    yolo.load(names="assets/class/coco.txt", weight="assets/models/coco-yolo5.pt")
    # coordinate state
    coordinate_data_handler = YAMLDataHandler("out/parking-output-coordinate.yaml")
    output_data_handler = YAMLDataHandler("out/parking-output-data.yaml")
    total_parking = 13
    area_color = [0, 0, 255]
    all_areas = None
    while all_areas is None:
        data_read = coordinate_data_handler.read()
        if data_read is not None:
            all_areas = data_read["parking_coordinate"]
    area_state = {}
    for area_index, (area_key, area_value) in enumerate(all_areas.items()):
        area_state[f"area_state_{area_index}"] = 0
    while True:
        try:
            frame = cam.read(frame_size=720, show_fps=True)
            frame2 = cam2.read(frame_size=720, show_fps=True)
            frame = cv2.vconcat([frame, frame2])
            detect = yolo.predict(frame)
            detect = [data for data in detect if data['class'] == 'car']
            detect_num = 0
            for area_index, (area_key, area_value) in enumerate(all_areas.items()):
                area_state[f"area_state_{area_index}"] = 0
                detect_in_area = []
                area_color = [0, 255, 0]
                for data_detect in detect:
                    result = cv2.pointPolygonTest(np.array(area_value, np.int32), (data_detect["x"], data_detect["y"]),
                                                  False)
                    if result >= 0:
                        detect_in_area.append(data_detect)
                        yolo.draw(frame, detect_in_area)
                        area_color = [0, 0, 255]
                        detect_num += 1
                coordinate_x = []
                coordinate_y = []
                for coordinate in area_value:
                    coordinate_x.append(coordinate[0])
                    coordinate_y.append(coordinate[1])
                # cv2.polylines(frame, [np.array(area_value, np.int32)], True, area_color, 2)
                center_x = int(np.mean(np.array(coordinate_x)))
                center_y = int(np.mean(np.array(coordinate_y)))
                # cv2.circle(frame, (center_x, center_y), 3, 255, -1)
                # cv2.putText(frame, str(area_key), (center_x, center_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
            # parking_available = len(all_areas) - detect_num
            parking_available = total_parking - detect_num
            output_data_handler_data = output_data_handler.read()
            if output_data_handler_data is not None:
                output_data_handler.update("parking_available", parking_available)
                # log.logdebug(parking_available)
            else:
                output_data_handler.write({
                    "parking_available": parking_available
                })
            cv2.putText(frame, "Parking Available: " + str(parking_available), (10, 360), 0, 1, [0, 0, 0],
                        thickness=2, lineType=cv2.LINE_AA)
            # cam.show(frame, "frame")
            # cam.write(frame)
            # print(frame.shape)
            buffer = cam.image_encode(frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            if cam.wait(1) == ord('q'):
                break
        except Exception as err:
            log.logerr(err)


@app.route('/')
def index():
    return redirect('/video_feed')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, host=f'{raspberry_ip}')
