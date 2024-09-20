import time
import cv2
import numpy as np

from modules.utils import *
from modules.image import Vision
from modules.filters import KalmanFilter
from modules.routine import ImgRex as Yolo
from utility.data import YAMLDataHandler

# global variables
mouse_coordinate = []
mouse_coordinate_all = {}
mouse_coordinate_index = 0
coordinate_data_handler = YAMLDataHandler("out/hands-output-coordinate.yaml")


def mouseCallback(event, x, y, flags, param):
    global mouse_coordinate, mouse_coordinate_all, mouse_coordinate_index
    if event == cv2.EVENT_MOUSEMOVE:
        pass  # artwork_coordinate
    elif event == cv2.EVENT_RBUTTONDOWN:
        mouse_coordinate.append([x, y])
        if mouse_coordinate:
            mouse_coordinate_all[f"artwork_{mouse_coordinate_index}"] = mouse_coordinate
            coordinate_data_handler.update("artwork_coordinate", mouse_coordinate_all)
    elif event == cv2.EVENT_LBUTTONDOWN:
        if mouse_coordinate:
            mouse_coordinate = []
            mouse_coordinate_index += 1
            print(f"Coordinate Saved")


cv2.namedWindow('frame')
cv2.setMouseCallback('frame', mouseCallback)

if __name__ == "__main__":
    print("[INFO] Main Initialize")
    cam = Vision(isUsingCam=True, addr="data/hands/hands-video.mp4", index=0, device="windows")
    try:
        while True:
            try:
                frame = cam.read(frame_size=0, show_fps=True)
                all_areas = None
                while all_areas is None:
                    data_read = coordinate_data_handler.read()
                    if data_read is not None:
                        all_areas = data_read["artwork_coordinate"]
                try:
                    for key, value in all_areas.items():
                        coordinate_x = []
                        coordinate_y = []
                        for coordinate in value:
                            coordinate_x.append(coordinate[0])
                            coordinate_y.append(coordinate[1])
                        cv2.polylines(frame, [np.array(value, np.int32)], True, (0, 255, 0), 2)
                        center_x = int(np.mean(np.array(coordinate_x)))
                        center_y = int(np.mean(np.array(coordinate_y)))
                        cv2.circle(frame, (center_x, center_y), 3, 255, -1)
                        cv2.putText(frame, str(key), (center_x, center_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (225, 255, 255), 2, cv2.LINE_AA)
                except Exception as e:
                    print(e)
                cam.show(frame, "frame")
                if cam.wait(1) == ord('q'):
                    break
            except Exception as err:
                print(err)
        cam.release()
        cam.destroy()
    except Exception as e:
        print(f"[INFO] {time.time()} Main Initialize Failed: \n{e}")
