import cv2
import av
import threading
import queue
import datetime
import numpy as np
import pytesseract

from modules.Image import Vision
from modules.yolo.Yolov5 import Yolov5
from sort.sort import *
from util import readLicensePlate, insertPelanggaran, read_license_plate

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

PATH = "../assets/naval"
DB_PATH = "apps/assets/naval/result"

cv2.namedWindow('Threshold Adjuster')
cv2.namedWindow('frame')
cv2.namedWindow('binary')
cv2.namedWindow('plate')

cv2.createTrackbar('Threshold Min', 'Threshold Adjuster', 230, 255, lambda x: None)
cv2.createTrackbar('Threshold Max', 'Threshold Adjuster', 180, 255, lambda x: None)

frame_queue = queue.Queue(maxsize=10)

def frame_reader():
    container = av.open("rtsp://admin:admin@192.168.137.69:8554/Streaming/Channels/101")
    frame_generator = container.decode(video=0)

    while True:
        try:
            frame = next(frame_generator)
            frame = frame.to_ndarray(format='bgr24')
            frame = frame.astype(np.uint8)
            frame = cv2.resize(frame, (640, 480))
            frame_queue.put(frame)
        except StopIteration:
            break
        except Exception as e:
            print(e)

if __name__ == "__main__":
    cam = Vision(isUsingCam=False, addr=f"{PATH}/video/002-Naval-47.mp4", index=1, device="windows")

    reader_thread = threading.Thread(target=frame_reader)
    reader_thread.daemon = True
    reader_thread.start()

    motTracker = Sort()

    model = Yolov5()
    model.load(f"{PATH}/name/coco.txt", f"{PATH}/model/yolov5n.pt")
    model.setConfidence(0.2)

    customModel = Yolov5()
    customModel.load(f"{PATH}/name/platemotor2.txt", f"{PATH}/model/best.pt")
    customModel.setConfidence(0.2)
    detectCount = 0

    while True:
        try:
            frame = frame_queue.get()
            print(type(frame))
            height, width, _ = frame.shape
            lResult = model.predict(frame)
            lCustom = customModel.predict(frame)
            lCustomPlate = customModel.filterByClass(lCustom, "licenseplate")
            lCustomMotor = customModel.filterByClass(lCustom, "motorcycle")
            lMotor = model.filterByClass(lResult, "motorcycle")
            lPerson = model.filterByClass(lResult, "person")

            for motor in lCustomMotor:
                personData = [person for person in lPerson if model.isAreaOverlapping(person, motor)]
                personCount = len(personData)
                if personCount > 2:
                    frameNullPerson = np.zeros((height, width, 3), dtype=np.uint8)
                    for pd in personData:
                        personImg = frame[pd["y"]:pd["y"] + pd["height"], pd["y"]:pd["y"] + pd["height"]]
                        frameNullPerson[pd["y"]:pd["y"] + pd["height"], pd["y"]:pd["y"] + pd["height"]] = personImg

                    frameNullPlate = np.zeros((height, width, 3), dtype=np.uint8)
                    for plate in lCustomPlate:
                        if model.isAreaOverlapping(plate, motor, option=True):
                            detectCount += 1
                            plateImg = frame[plate["y"]:plate["y2"], plate["x"]:plate["x2"]]
                            frameNullPlate[plate["y"]:plate["y2"], plate["x"]:plate["x2"]] = plateImg

                            framePlate = frame[plate["y"]:plate["y2"], plate["x"]:plate["x2"]]
                            framePlateGray = cv2.cvtColor(framePlate, cv2.COLOR_BGR2GRAY)

                            thresh_min = cv2.getTrackbarPos('Threshold Min', 'Threshold Adjuster')
                            thresh_max = cv2.getTrackbarPos('Threshold Max', 'Threshold Adjuster')
                            _, framePlateThresh = cv2.threshold(framePlateGray, thresh_min, thresh_max, cv2.THRESH_BINARY_INV)

                            cv2.imshow("plate", framePlate)
                            cv2.imshow("binary", framePlateThresh)

                            plateText, plateScore = readLicensePlate(framePlateThresh)

                            print(f"plateText: {plateText}, plateScore: {plateScore}")

                            waktu = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")

                            nama_file_pelanggaran = f'img_pelanggaran_{waktu}.png'
                            nama_file_plat = f'img_plat_{waktu}.png'

                            nama_file_pelanggaran_save = f'{PATH}/result/{nama_file_pelanggaran}'
                            nama_file_plat_save = f'{PATH}/result/{nama_file_plat}'

                            tgl_pelanggaran = datetime.datetime.now().strftime("%Y-%m-%d")
                            jenis_pelanggaran = "penumpang lebih dari dua"
                            nomor_plat = plateText
                            gambar_pelanggaran = f"{DB_PATH}/{nama_file_pelanggaran}"
                            gambar_plat_nomor = f"{DB_PATH}/{nama_file_plat}"

                            cam.writeImage(framePlate, f'{PATH}/result/img_{detectCount}_framePlate.png')
                            cam.writeImage(framePlateGray, f'{PATH}/result/img_{detectCount}_framePlateGray.png')
                            cam.writeImage(framePlateThresh, f'{PATH}/result/img_{detectCount}_framePlateThresh.png')

                    frameDrawCopy = frame.copy()
                    model.draw(frameDrawCopy, lPerson)
                    model.draw(frameDrawCopy, lCustom)
                    topRow = np.hstack((frame, frameDrawCopy))
                    bottomRow = np.hstack((frameNullPerson, frameNullPlate))
                    frameFinal = np.vstack((topRow, bottomRow))
                    frameFinal = cam.resize(frameFinal, 1080)

            model.draw(frame, lPerson)
            model.draw(frame, lCustomPlate)
            model.draw(frame, lCustomMotor)
            cam.show(frame, 'frame')
            if cam.wait(1) == ord('q'):
                break
        except queue.Empty:
            continue
        except Exception as e:
            print(e)

    cam.release()
    cam.destroy()
