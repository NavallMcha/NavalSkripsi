import cv2
import string
import easyocr
import mysql.connector
import numpy as np
import pytesseract

reader = easyocr.Reader(['en'], gpu=False)
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}
dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}


def writeCSV(results, output_path):
    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{}\n'.format('frame_nmr', 'car_id', 'car_bbox',
                                                'license_plate_bbox', 'license_plate_bbox_score', 'license_number',
                                                'license_number_score'))

        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                print(results[frame_nmr][car_id])
                if 'car' in results[frame_nmr][car_id].keys() and \
                        'license_plate' in results[frame_nmr][car_id].keys() and \
                        'text' in results[frame_nmr][car_id]['license_plate'].keys():
                    f.write('{},{},{},{},{},{},{}\n'
                            .format(frame_nmr,
                                    car_id,
                                    '[{} {} {} {}]'.format(
                                        results[frame_nmr][car_id]['car']['bbox'][0],
                                        results[frame_nmr][car_id]['car']['bbox'][1],
                                        results[frame_nmr][car_id]['car']['bbox'][2],
                                        results[frame_nmr][car_id]['car']['bbox'][3]),
                                    '[{} {} {} {}]'.format(
                                        results[frame_nmr][car_id]['license_plate']['bbox'][0],
                                        results[frame_nmr][car_id]['license_plate']['bbox'][1],
                                        results[frame_nmr][car_id]['license_plate']['bbox'][2],
                                        results[frame_nmr][car_id]['license_plate']['bbox'][3]),
                                    results[frame_nmr][car_id]['license_plate']['bbox_score'],
                                    results[frame_nmr][car_id]['license_plate']['text'],
                                    results[frame_nmr][car_id]['license_plate']['text_score']))
        f.close()


def licenseCompliesFormat(text):
    if len(text) != 7:
        return False
    if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
            (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
            (text[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
            (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
            (text[4] in string.ascii_uppercase or text[4] in dict_int_to_char.keys()) and \
            (text[5] in string.ascii_uppercase or text[5] in dict_int_to_char.keys()) and \
            (text[6] in string.ascii_uppercase or text[6] in dict_int_to_char.keys()):
        return True
    else:
        return False


def formatLicense(text):
    license_plate_ = ''
    mapping = {0: dict_int_to_char, 1: dict_int_to_char, 4: dict_int_to_char, 5: dict_int_to_char, 6: dict_int_to_char,
               2: dict_char_to_int, 3: dict_char_to_int}
    for j in [0, 1, 2, 3, 4, 5, 6]:
        if text[j] in mapping[j].keys():
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]

    return license_plate_


def readLicensePlate(license_plate_crop):
    detections = reader.readtext(license_plate_crop)
    for detection in detections:
        bbox, text, score = detection
        text = text.upper().replace(' ', '')
        # print(text)
        # if licenseCompliesFormat(text):
            # return formatLicense(text), score
        # return formatLicense(text), score
        return text, score
    return None, None


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

    thresh_min = cv2.getTrackbarPos('Threshold Min', 'Threshold Adjuster')
    thresh_max = cv2.getTrackbarPos('Threshold Max', 'Threshold Adjuster')

    # Apply adaptive thresholding
    _, binary = cv2.threshold(gray, thresh_min, thresh_max, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


    # print("thresh_min:" + str(thresh_min ))
    # print("thresh_max:" + str(thresh_max))

    cv2.imshow("binary", binary)

    # Apply dilation and erosion to enhance features
    kernel = np.ones((1, 1), np.uint8)
    processed_image = cv2.dilate(binary, kernel, iterations=1)
    processed_image = cv2.erode(processed_image, kernel, iterations=1)

    # topRow = np.hstack((image, image))
    # bottomRow = np.hstack((image, image))
    # frameFinal = np.vstack((topRow, bottomRow))
    #
    # cv2.imshow("frameFinal", frameFinal)

    # cv2.imshow("image", image)
    # cv2.imshow("gray", gray)
    # cv2.imshow("binary", binary)
    # cv2.imshow("processed_image", processed_image)

    return processed_image


def read_license_plate(image):
    # Preprocess image for better OCR accuracy
    processed_image = preprocess_image(image)

    # Optimized Tesseract OCR configuration
    config = '--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(processed_image, config=config)
    text_score = 1.0  # Dummy score, since Tesseract does not provide a confidence score

    return text.strip(), text_score


def insertPelanggaran(tgl_pelanggaran, jenis_pelanggaran, nomor_plat, gambar_pelanggaran, gambar_plat_nomor):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Ganti dengan username MySQL Anda
            password="",  # Ganti dengan password MySQL Anda
            database="navalweb"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            # Query SQL untuk menyisipkan data ke dalam tabel pelanggaran
            insert_query = "INSERT INTO pelanggaran (tgl_pelanggaran, jenis_pelanggaran, nomor_plat, gambar_pelanggaran, gambar_plat_nomor) VALUES (%s, %s, %s, %s, %s)"
            # Data yang akan dimasukkan ke dalam tabel
            data = (tgl_pelanggaran, jenis_pelanggaran, nomor_plat, gambar_pelanggaran, gambar_plat_nomor)
            cursor.execute(insert_query, data)
            connection.commit()
            print("Data berhasil dimasukkan ke dalam tabel pelanggaran")
    except mysql.connector.Error as err:
        print("Gagal memasukkan data ke dalam tabel pelanggaran:", err)
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
