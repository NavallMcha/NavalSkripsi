import cv2
import numpy as np
import pytesseract
from flask import Flask, request, jsonify
import threading
from ultralytics import YOLO
import uuid
import os

pytesseract.pytesseract.tesseract_cmd = r'D:\xampp\htdocs\navalweb\apps\public\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

# Load models
coco_model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('license_plate_detector.pt')


def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Rescale image to enhance OCR accuracy
    scale_percent = 150  # Percent of original size
    width = int(gray.shape[1] * scale_percent / 100)
    height = int(gray.shape[0] * scale_percent / 100)
    dim = (width, height)
    gray = cv2.resize(gray, dim, interpolation=cv2.INTER_CUBIC)

    # Apply bilateral filter to remove noise
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # Apply adaptive thresholding
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply dilation and erosion to enhance features
    kernel = np.ones((1, 1), np.uint8)
    processed_image = cv2.dilate(binary, kernel, iterations=1)
    processed_image = cv2.erode(processed_image, kernel, iterations=1)

    return processed_image


def read_license_plate(image):
    # Preprocess image for better OCR accuracy
    processed_image = preprocess_image(image)

    # Optimized Tesseract OCR configuration
    config = '--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(processed_image, config=config)
    text_score = 1.0  # Dummy score, since Tesseract does not provide a confidence score

    return text.strip(), text_score


def detect_and_process(frame):
    vehicles = [2, 3]  # Car and motorbike class IDs in COCO dataset

    # Detect vehicles
    detections = coco_model(frame)[0]
    detections_ = []
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = detection
        if int(class_id) in vehicles:
            detections_.append([x1, y1, x2, y2, score])

            # Detect license plates
            license_plates = license_plate_detector(frame)[0]
            plate_texts = []
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate

                # Crop license plate
                license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]

                # Read license plate number
                license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop)
                if license_plate_text:
                    plate_texts.append(license_plate_text)

                    # Draw bounding box around the vehicle
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

                    # Draw bounding box around the license plate
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

                    # Put the license plate text on the image
                    cv2.putText(frame, license_plate_text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (36, 255, 12), 2)

                    # Generate a random filename for the output image
                    output_filename = f'output_image_{uuid.uuid4().hex}.jpg'
                    output_path = os.path.join('platregister', output_filename)
                    cv2.imwrite(output_path, frame)

                    return plate_texts, output_path


@app.route('/detect_plate_yolo', methods=['POST'])
def detect_plate_service():
    file = request.files['image']
    # Read image from the uploaded file
    image_bytes = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

    # Resize the image to maintain aspect ratio with a max dimension of 640x480
    original_height, original_width = frame.shape[:2]
    max_dim = max(original_width, original_height)
    scale_factor = min(640 / max_dim, 480 / max_dim)
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)
    frame = cv2.resize(frame, (new_width, new_height))

    plate_texts, result_image_path = detect_and_process(frame)

    return jsonify({
        'plate_texts': plate_texts,
        'result_image_path': result_image_path
    })


def run_app():
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    threading.Thread(target=run_app).start()
