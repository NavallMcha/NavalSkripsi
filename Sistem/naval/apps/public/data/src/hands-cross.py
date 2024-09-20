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
from modules.routine import ImgRex as Yolo
from flask import Flask, Response, redirect
from utility.logger import Logger as log

load_dotenv()
raspberry_ip = os.getenv('RASPBERRY_IP')
app = Flask(__name__)


def play_music():
    while not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
        pygame.time.Clock().tick(10)


def generate_frames():
    # inisialisasi camera start -------------------------
    log.loginfo("Main Initialize")
    cam = Vision(isUsingCam=True, addr="data/hands/hands-video.mp4", index=0, device="windows")
    cam.writeConfig("out/hands-output-video.mp4")
    # inisialisasi camera end -------------------------
    # inisialisasi yolo start -------------------------
    yolo = Yolo()
    # yolo.load("data/hands/hands-10.txt", "data/hands/hands-10.pt")
    yolo.load("data/hands/hands-cross-tiny-prn.weights", "data/hands/hands-cross-tiny-prn.cfg",
              "data/hands/hands-cross-tiny-prn.txt")
    # inisialisasi yolo end -------------------------
    # inisialisasi data yaml start -------------------------
    coordinate_data_handler = YAMLDataHandler("out/hands-output-coordinate.yaml")
    output_data_handler = YAMLDataHandler("out/hands-output-data.yaml")
    output_data_handler_init_data = {
        "area_state": 0,
        "confidence": str(0),
        "count": str(0),
        "fps": str(0),
        "state": 0
    }
    output_data_handler.write(output_data_handler_init_data)
    # output_data_handler.update("state", str(0))
    # output_data_handler.update("count", str(0))
    detect_hand_state_before = 0
    camera_index_before = 0
    # inisialisasi data yaml end -------------------------
    # inisialisasi coordinate start -------------------------
    all_areas = None
    while all_areas is None:
        data_read = coordinate_data_handler.read()
        if data_read is not None:
            all_areas = data_read["artwork_coordinate"]
    area_state = {}
    for area_index, (area_key, area_value) in enumerate(all_areas.items()):
        area_state[f"area_state_{area_index}"] = 0
    # inisialisasi coordinate end -------------------------
    # inisialisasi play sound start -------------------------
    pygame.init()
    warning_mp3_file = "data/hands/warn.mp3"
    pygame.mixer.init()
    pygame.mixer.music.load(warning_mp3_file)
    # inisialisasi play sound end -------------------------
    try:
        while True:
            try:
                # pembacaan kamera start -------------------------
                frame = cam.read(frame_size=0)
                # pembacaan kamera end -------------------------
                # pengaturan configurasi kamera kecerahan dll start -------------------------
                param_data_handler = YAMLDataHandler("out/hands-output-param.yaml").read()
                if param_data_handler is not None:
                    camera_index = int(param_data_handler["camera"])
                    if camera_index != camera_index_before:
                        camera_index_before = camera_index
                        cam = Vision(
                            isUsingCam=True,
                            addr="data/hands/hands-video.mp4",
                            index=camera_index,
                            device="windows"
                        )
                    yolo.setConfidence(param_data_handler["confidence"] / 100)
                    frame = cam.setBrightness(frame, param_data_handler["brightness"])
                    frame = cam.setContrast(frame, param_data_handler["contrast"])
                    # pengaturan configurasi kamera kecerahan dll end -------------------------
                    # prediksi yolo start -------------------------
                    detect = yolo.predict(frame)
                    # prediksi yolo end -------------------------
                    # pengecekan tangan pada area lukisan dan pengiriman data start -------------------------
                    fps = str(cam.get_fps())
                    detect_hand_state = 0
                    detect_hand_area = -1
                    delay_time_start = time.time()
                    for area_index, (area_key, area_value) in enumerate(all_areas.items()):
                        area_state[f"area_state_{area_index}"] = 0
                        detect_in_area = []
                        for data_detect in detect:
                            result = cv2.pointPolygonTest(np.array(area_value, np.int32),
                                                          (data_detect["x"], data_detect["y"]), False)
                            if result >= 0:
                                detect_in_area.append(data_detect)
                                yolo.draw(frame, detect_in_area)
                                area_state[f"area_state_{area_index}"] = 1 if result >= 0 else 0
                                detect_hand_state = 1
                                detect_hand_area = area_index
                        try:
                            data_handler_buffer = output_data_handler.read()
                            if data_handler_buffer is not None:
                                output_data_handler.update("fps", fps)
                                output_data_handler.update("state", detect_hand_state)
                                output_data_handler.update("area_state", area_state)
                            else:
                                data_init = {
                                    "fps": fps,
                                    "state": detect_hand_state,
                                    "area_state": area_state
                                }
                                output_data_handler.write(data_init)
                        except Exception as e:
                            log.logerr(e)
                        # pengecekan tangan pada area lukisan pengiriman data end -------------------------
                        # gambar koordinat start -------------------------
                        coordinate_x = []
                        coordinate_y = []
                        for coordinate in area_value:
                            coordinate_x.append(coordinate[0])
                            coordinate_y.append(coordinate[1])
                        cv2.polylines(frame, [np.array(area_value, np.int32)], True, (0, 255, 0), 2)
                        center_x = int(np.mean(np.array(coordinate_x)))
                        center_y = int(np.mean(np.array(coordinate_y)))
                        cv2.circle(frame, (center_x, center_y), 3, 255, -1)
                        cv2.putText(frame, str(area_key), (center_x, center_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (0, 255, 0), 2, cv2.LINE_AA)
                        # gambar koordinat end -------------------------
                    # pengiriman data seperti ada tangan atau tidak dll start -------------------------
                    if detect_hand_state:
                        cam.writeImg(frame, "out/hands-output-image.png")
                    if detect_hand_state != detect_hand_state_before:
                        detect_hand_state_before = detect_hand_state
                        if detect_hand_state:
                            delay_time_end = time.time()
                            delay_time_total = delay_time_end - delay_time_start
                            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            log.logdebug(
                                f"delay time: {delay_time_total} seconds "
                                f"on area {detect_hand_area} "
                                f"at {current_datetime}"
                            )
                            log_handler = YAMLDataHandler("out/hands-output-log.yaml")
                            log_handler_buffer = log_handler.read()
                            if log_handler_buffer is not None:
                                epoch_time = time.time()
                                log_buffer = log_handler_buffer["log"]
                                if log_buffer is None or log_buffer == 0:
                                    log_buffer = []
                                log_report = {
                                    "epoch": epoch_time,
                                    "data": {
                                        "epoch": epoch_time,
                                        "area": detect_hand_area,
                                        "time": current_datetime
                                    }
                                }
                                log_buffer.append(log_report)
                                cam.writeImg(frame, f"out/log/hands-output-image-{epoch_time}.png")
                                log_handler.update("log", log_buffer)
                                # pengiriman data seperti ada tangan atau tidak dll end -------------------------
                                # pemutaran sound start -------------------------
                                music_thread = threading.Thread(target=play_music)
                                music_thread.daemon = True
                                music_thread.start()
                                # pemutaran sound end -------------------------
                    # pengiriman video ke website start -------------------------
                    buffer = cam.image_encode(frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                    if cam.wait(1) == ord('q'):
                        break
                    # pengiriman video ke website end -------------------------
            except Exception as err:
                print(err)
        pygame.mixer.quit()
        pygame.quit()
        cam.release()
        cam.destroy()
    except Exception as e:
        print(f"[INFO] {time.time()} Main Initialize Failed: \n{e}")


# pengaturan dan konfigurasi ip start -------------------------
@app.route('/')
def index():
    return redirect('/video_feed')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, host=f'{raspberry_ip}')
    # pengaturan dan konfigurasi ip end -------------------------
