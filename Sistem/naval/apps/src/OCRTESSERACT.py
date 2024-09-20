# import cv2
# import numpy as np
# import pytesseract
# from pytesseract import Output

# def detect_license_plate(image):
#     # Convert image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Apply GaussianBlur to reduce noise and improve edge detection
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)

#     # Perform edge detection
#     edged = cv2.Canny(blurred, 50, 200)

#     # Find contours in the edged image
#     contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

#     # Loop over the contours to find the license plate contour
#     license_plate_contour = None
#     for contour in contours:
#         approx = cv2.approxPolyDP(contour, 10, True)
#         if len(approx) == 4:
#             license_plate_contour = approx
#             break

#     return license_plate_contour

# def four_point_transform(image, pts):
#     rect = np.zeros((4, 2), dtype="float32")

#     # Order the points in the correct order: top-left, top-right, bottom-right, bottom-left
#     s = np.sum(pts, axis=1)
#     rect[0] = pts[np.argmin(s)]
#     rect[2] = pts[np.argmax(s)]

#     diff = np.diff(pts, axis=1)
#     rect[1] = pts[np.argmin(diff)]
#     rect[3] = pts[np.argmax(diff)]

#     (tl, tr, br, bl) = rect

#     # Compute the width of the new image
#     widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
#     widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
#     maxWidth = max(int(widthA), int(widthB))

#     # Compute the height of the new image
#     heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
#     heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
#     maxHeight = max(int(heightA), int(heightB))

#     # Construct the destination points
#     dst = np.array([
#         [0, 0],
#         [maxWidth - 1, 0],
#         [maxWidth - 1, maxHeight - 1],
#         [0, maxHeight - 1]], dtype="float32")

#     # Compute the perspective transform matrix and apply it
#     M = cv2.getPerspectiveTransform(rect, dst)
#     warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

#     return warped

# def preprocess_for_ocr(image):
#     # Convert to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Apply thresholding to get binary image
#     _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
#     # Additional noise reduction and morphological transformations if needed
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#     processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

#     return processed

# def main(image_path):
#     # Load the image
#     image = cv2.imread(image_path)

#     # Detect the license plate contour
#     plate_contour = detect_license_plate(image)
#     if plate_contour is None:
#         print("License plate not found")
#         return

#     # Apply the four-point transform to obtain a top-down view of the license plate
#     warped = four_point_transform(image, plate_contour.reshape(4, 2))

#     # Preprocess the image for OCR
#     preprocessed_warped = preprocess_for_ocr(warped)

#     # Perform OCR using Tesseract
#     custom_config = r'--oem 3 --psm 8'  # Configure Tesseract to use default engine and single word mode
#     text = pytesseract.image_to_string(preprocessed_warped, config=custom_config)
#     print("Detected Text:", text)

#     # Save or display the output
#     cv2.imshow("Original Image", image)
#     cv2.imshow("Warped Image", warped)
#     cv2.imshow("Preprocessed for OCR", preprocessed_warped)
#     cv2.imwrite("warped_license_plate.jpg", warped)
#     cv2.imwrite("preprocessed_warped_license_plate.jpg", preprocessed_warped)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#      main("D:/skripsi/skripsi/navalweb/navalweb/apps/assets/naval/video/002-Naval-24.mp4")

import cv2
import time
import random
import datetime
import numpy as np
import pytesseract

from modules.Image import Vision
from modules.yolo.Yolov5 import Yolov5
from sort.sort import *
from util import read_license_plate, insertPelanggaran, readLicensePlate

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

PATH = "../assets/naval"
DB_PATH = "apps/assets/naval/result"

def detect_license_plate(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 200)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    
    license_plate_contour = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            license_plate_contour = approx
            break
    return license_plate_contour

def four_point_transform(image, pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = np.sum(pts, axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

def preprocess_for_ocr(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    return processed

if __name__ == "__main__":
    cam = Vision(isUsingCam=False, addr=f"{PATH}/video/002-Naval-11.mp4", index=1, device="windows")
    motTracker = Sort()

    model = Yolov5()
    model.load(f"{PATH}/name/coco.txt", f"{PATH}/model/yolov5n.pt")
    model.setConfidence(0.2)

    customModel = Yolov5()
    customModel.load(f"{PATH}/name/platemotor.txt", f"{PATH}/model/platemotor2v5s.pt")
    customModel.setConfidence(0.2)
    detectCount = 0
    while True:
        try:
            frame = cam.read(1080, show_fps=True, loop=False)
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
                        personImg = frame[pd["y"]:pd["y"] + pd["height"], pd["x"]:pd["x"] + pd["width"]]
                        frameNullPerson[pd["y"]:pd["y"] + pd["height"], pd["x"]:pd["x"] + pd["width"]] = personImg

                    frameNullPlate = np.zeros((height, width, 3), dtype=np.uint8)
                    for plate in lCustomPlate:
                        if model.isAreaOverlapping(plate, motor, option=True):
                            detectCount += 1
                            plateImg = frame[plate["y"]:plate["y2"], plate["x"]:plate["x2"]]
                            frameNullPlate[plate["y"]:plate["y2"], plate["x"]:plate["x2"]] = plateImg

                            framePlate = frame[plate["y"]:plate["y2"], plate["x"]:plate["x2"]]
                            framePlateGray = cv2.cvtColor(framePlate, cv2.COLOR_BGR2GRAY)
                            _, framePlateThresh = cv2.threshold(framePlateGray, 200, 255, cv2.THRESH_BINARY_INV)

                            # plateText, plateScore = readLicensePlate(framePlateThresh)
                            plateText, plateScore = read_license_plate(framePlate)
                            # print(f"plateText: {plateText}, plateScore: {plateScore}")

                            # waktu = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
                            # nama_file_pelanggaran = f'img_pelanggaran_{waktu}.png'
                            # nama_file_plat = f'img_plat_{waktu}.png'

                            # nama_file_pelanggaran_save = f'{PATH}/result/{nama_file_pelanggaran}'
                            # nama_file_plat_save = f'{PATH}/result/{nama_file_plat}'

                            # tgl_pelanggaran = datetime.datetime.now().strftime("%Y-%m-%d")
                            # jenis_pelanggaran = "penumpang lebih dari dua"
                            # nomor_plat = "N1234BA"
                            # gambar_pelanggaran = f"{DB_PATH}/{nama_file_pelanggaran}"
                            # gambar_plat_nomor = f"{DB_PATH}/{nama_file_plat}"

                            cam.writeImage(framePlate, f'{PATH}/result/img_{detectCount}_framePlate.png')
                            cam.writeImage(framePlateGray, f'{PATH}/result/img_{detectCount}_framePlateGray.png')
                            cam.writeImage(framePlateThresh, f'{PATH}/result/img_{detectCount}_framePlateThresh.png')

                    frameDrawCopy = frame.copy()
                    model.draw(frameDrawCopy, lPerson)
                    model.draw(frameDrawCopy, lCustom)
                    topRow = np.hstack((frame, frameDrawCopy))
                    bottomRow = np.hstack((frameNullPerson, frameNullPlate))
                    frameFinal = np.vstack((topRow, bottomRow))
                    frameFinal = cam.resize(frameFinal, 400)

                    cam.show(frameFinal, 'frameFinal')

            model.draw(frame, lMotor)
            model.draw(frame, lPerson)
            if cam.wait(1) == ord('q'):
                break
        except Exception as e:
            print(e)
    cam.release()
    cam.destroy()

# if __name__ == "__main__":
    # main("D:/skripsi/skripsi/navalweb/navalweb/apps/assets/naval/video/002-Naval-24.mp4")
