import cv2

from lib import *
import sys
import signal
from vidgear.gears import CamGear

from flask import Flask, render_template, Response, redirect


app = Flask(__name__)

## PARAMETER
TRESHOLD_ASAP = 30
TRESHOLD_SUHU = 50

PORT_COM = 'COM6'
PORT_BAUD = 115200

TELEGRAM_TOKEN = "6322020435:AAELvBH9XaWxsG5hFZ4vn-FTm70B69wsB20"
CHAT_ID = ["678809573", "5071997349"]
WA_ID = ["Notifikasi - API"]

STREAM_URL = 1
STREAM_MODE = False
FRAME_WIDTH = 640
FRAME_HEIGHT = 640
FRAME_SLEEP = 1 # 15

## VARIABLE
DataSensor = []
DeteksiClass = []
DeteksiFrame = []
DeteksiConfidence = []

# Fungsi untuk menghentikan program secara aman saat Ctrl+C atau terminal ditutup
def signal_handler(signal, frame):
    print("Program dihentikan")
    sys.exit(0)


# Pengaturan sinyal untuk mengatasi Ctrl+C atau terminal ditutup
signal.signal(signal.SIGINT, signal_handler)

def arduino_handler():
    global DataSensor, PORT_COM, PORT_BAUD

    sensor_reader = SensorDataReader(port=PORT_COM, baud_rate=PORT_BAUD)
    sensor_reader.open_serial_connection()
    last_time_read = 0
    read_timer = 1
    while True:
        if time.time() - last_time_read > read_timer :
            last_time_read = time.time()

            sensor_reader.read_data()
            Data = sensor_reader.get_data()

            # Data = [-6, 140, 20, 40, 12]
            # print(Data)
            DataSensor = Data

            if Data:
                sensor = SensorData(data_list=Data)
                message = "[INFO] New data received: " \
                        "Latitude={}, " \
                        "Longitude={}, " \
                        "Temperature={}," \
                        " Humidity={}, " \
                        "Smoke Sensor={}".format(
                    sensor.latitude,
                    sensor.longitude,
                    sensor.temperature,
                    sensor.humidity,
                    sensor.smoke_sensor
                )

                print(message)



def telegram_handler():

    global DeteksiClass, DeteksiConfidence, DeteksiFrame, DataSensor, \
        CHAT_ID, TRESHOLD_ASAP, TRESHOLD_SUHU, TELEGRAM_TOKEN, STREAM_URL

    time.sleep(2)

    print('TELEGRAM INIT')
    telegram_token = TELEGRAM_TOKEN


    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%Y-%m-%d")

    telegram_client = TelegramClient(telegram_token)

    sensor = ''
    last_print_time = [0, 0, 0]
    print_time = 60 # detik
    # DataSensor = [-6, 140, 29,30,11]
    # DeteksiClass = ['api', 'person']
    # DeteksiConfidence = [0.1, 0.2, 0.34]
    while True:
        print(DataSensor, DeteksiClass, DeteksiConfidence)
        if DataSensor is not None and len(DataSensor) > 3:
            sensor = SensorData(data_list=DataSensor)
            if "api" in DeteksiClass and any(conf >= 0.33 for conf in DeteksiConfidence):
                current_time = time.time()
                # print('OTW KIRIM ', current_time, last_print_time ,current_time - last_print_time[0], current_time - last_print_time[0] >= print_time)
                if current_time - last_print_time[0] >= print_time:
                    for chat_id in CHAT_ID:
                        print("SEND NOTIF")
                        telegram_client.send_imagecv2(chat_id, DeteksiFrame)
                        telegram_client.send_message(chat_id, f"[INFO] Ada Api pada {current_date} {current_time}")
                        telegram_client.send_message(
                            chat_id,
                            "[INFO] Status Sensor Temperature={}, Humidity={}, Smoke Sensor={}".format(sensor.temperature,sensor.humidity,sensor.smoke_sensor)
                                                    )
                        telegram_client.send_message(
                            chat_id,
                            "[INFO] Lokasi :  https://www.google.com/maps/search/?api=1&query={},{}" .format(sensor.latitude, sensor.longitude)
                        )
                    last_print_time[0] = current_time

            else:
                # pass
                if float(sensor.temperature) > 50 and float(sensor.smoke_sensor) > 30:
                    current_time = time.time()

                    if current_time - last_print_time[1] >= print_time:
                        for chat_id in CHAT_ID:
                            if DeteksiFrame is not None and len(DeteksiFrame) > 0 :  telegram_client.send_imagecv2(chat_id, DeteksiFrame)
                            telegram_client.send_message(chat_id, f"[INFO] Ada Api pada {current_date} {current_time}")
                            telegram_client.send_message(
                                chat_id,
                                "[INFO] Status Sensor Temperature={}, Humidity={}, Smoke Sensor={}"
                                .format(sensor.temperature, sensor.humidity, sensor.smoke_sensor)
                            )
                            telegram_client.send_message(
                                chat_id,
                                "[INFO] Lokasi :  https://www.google.com/maps/search/?api=1&query={},{}"
                                .format(sensor.latitude, sensor.longitude)
                            )
                        last_print_time[1] = current_time

                else: # Tidak Ada Api
                    current_time = time.time()
                    if current_time - last_print_time[2] >= print_time:
                        print("tidak ada api", sensor.temperature, sensor.humidity)
                        last_print_time[2] = current_time


def whatsapp_handler():
    global DeteksiClass,DeteksiConfidence, DeteksiFrame, DataSensor, \
        WA_ID, TRESHOLD_ASAP, TRESHOLD_SUHU, STREAM_URL

    messenger = WhatsappClient()
    for wa_id in WA_ID:
        messenger.find_by_username(wa_id)
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%Y-%m-%d")


    sensor = ''
    last_print_time = 0
    print_time = 2  # detik
    while True:
        while True:

            print(DeteksiClass, DataSensor)
            if DataSensor is not None and len(DataSensor) > 3:
                sensor = SensorData(data_list=DataSensor)
                if "api" in DeteksiClass and any(conf > 33 for conf in DeteksiConfidence):
                    current_time = time.time()
                    if current_time - last_print_time >= print_time:
                        for wa_id in WA_ID:
                            messenger.find_by_username(wa_id)

                            messenger.kirimText(f"[INFO] Ada Api pada {current_date} {current_time}")
                            messenger.kirimText(
                                "[INFO] Status Sensor Temperature={}, Humidity={}, Smoke Sensor={}".format(
                                    sensor.temperature, sensor.humidity, sensor.smoke_sensor)
                            )
                            messenger.kirimText(
                                "[INFO] Lokasi :  https://www.google.com/maps/search/?api=1&query={},{}".format(
                                    sensor.latitude, sensor.longitude)
                            )

                        last_print_time = current_time

                else:
                    if float(sensor.temperature) > 50 and float(sensor.smoke_sensor) > 30:
                        current_time = time.time()
                        if current_time - last_print_time >= print_time:
                            for wa_id in WA_ID:
                                messenger.find_by_username(wa_id)

                                messenger.kirimText(f"[INFO] Ada Api pada {current_date} {current_time}")
                                messenger.kirimText(
                                    "[INFO] Status Sensor Temperature={}, Humidity={}, Smoke Sensor={}"
                                    .format(sensor.temperature, sensor.humidity, sensor.smoke_sensor)
                                )
                                messenger.kirimText(
                                    "[INFO] Lokasi :  https://www.google.com/maps/search/?api=1&query={},{}"
                                    .format(sensor.latitude, sensor.longitude)
                                )

                            last_print_time = current_time
                    else:  # Tidak Ada Api
                        current_time = time.time()
                        if current_time - last_print_time >= print_time:
                            print("tidak ada api", sensor.temperature, sensor.humidity)
                            last_print_time = current_time

def image_handler():
    global DeteksiClass, DeteksiConfidence, DeteksiFrame, STREAM_URL, STREAM_MODE, FRAME_HEIGHT, FRAME_WIDTH, FRAME_SLEEP

    print('DETEKSI INIT')
    time.sleep(FRAME_SLEEP)  # 15 saat program utama
    stream = cv2.imread(STREAM_URL)
    yolo = ImgRex()
    n = 0
    yolo.load("yolov3-tiny_training_baru.weights", "tiny.cfg", "obj.names")  ## INI GET DATA HASIL TRAINING
    while True:
        frame = stream
        # frame = cv2.imread('api_1.jpg')
        frame = resize(frame, FRAME_WIDTH, FRAME_HEIGHT)  ## RESIZE
        ksize = (3, 3)  # GANJIL
        frame = cv2.blur(frame, ksize)  ## BLUR untuk Kurang Noise

        detect = yolo.predict(frame)

        buffClass = []
        buffConf = []
        for data in detect:
            buffClass.append(data['class'])
            buffConf.append(data['confidence'])

        DeteksiClass = buffClass
        DeteksiConfidence = buffConf


        DeteksiFrame = frame  # Ambil HASIL DETEKSI YOLO JIKA ADA
        yolo.draw(frame, detect)  # GAMBAR Bouning BOX
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1) & 0xFF

        # check for 'q' key-press
        if key == ord("q"):
            # if 'q' key-pressed break out
            break

    cv2.destroyAllWindows()


def deteksi_handler():
    global DeteksiClass, DeteksiConfidence, DeteksiFrame, STREAM_URL, STREAM_MODE, FRAME_HEIGHT, FRAME_WIDTH, FRAME_SLEEP

    print('DETEKSI INIT : deteksi_handler')
    time.sleep(FRAME_SLEEP) # 15 saat program utama

    cam = cv2.VideoCapture(STREAM_URL, cv2.CAP_DSHOW)
    yolo = ImgRex()
    n = 0

    yolo.load("yolov3-tiny_training_baru.weights", "tiny.cfg", "obj.names") ## INI GET DATA HASIL TRAINING
    while True:
            _, frame = cam.read()
            frame = resize(frame, FRAME_WIDTH, FRAME_HEIGHT)  ## RESIZE
            ksize = (3, 3) # GANJIL
            frame = cv2.blur(frame, ksize)  ## BLUR untuk Kurang Noise

            detect = yolo.predict(frame)

            buffClass = []
            buffConf = []
            for data in detect:
                buffClass.append(data['class'])
                buffConf.append(data['confidence'])

            DeteksiClass = buffClass
            DeteksiConfidence = buffConf

            DeteksiFrame = frame                                 # Ambil HASIL DETEKSI YOLO JIKA ADA
            yolo.draw(frame, detect)                # GAMBAR Bouning BOX
            cv2.imshow('frame', frame)
            key = cv2.waitKey(1) & 0xFF

            # check for 'q' key-press
            if key == ord("q"):
                # if 'q' key-pressed break out
                break

    cv2.destroyAllWindows()
    cam.release()


def video_handler():
    global DeteksiClass, DeteksiConfidence, DeteksiFrame, STREAM_URL, STREAM_MODE, FRAME_SLEEP, FRAME_HEIGHT, FRAME_WIDTH

    print('DETEKSI INIT: video_handler()')
    time.sleep(FRAME_SLEEP) # 15 saat program utama

    cam = cv2.VideoCapture(STREAM_URL, cv2.CAP_DSHOW)
    yolo = ImgRex()
    n = 0
    yolo.load("yolov3-tiny_training_baru.weights", "tiny.cfg", "obj.names") ## INI GET DATA HASIL TRAINING
    while True:
            _, frame = cam.read()
            frame = resize(frame, FRAME_WIDTH, FRAME_HEIGHT)  ## RESIZE

            ksize = (3, 3) # GANJIL
            frame = cv2.blur(frame, ksize)  ## BLUR untuk Kurang Noise

            detect = yolo.predict(frame)

            buffClass = []
            buffConf = []
            # for data in detect: l9d
            # ,buffClass.append(data['class'])
            #     buffConf.append(data['confidence'])

            DeteksiClass = buffClass
            DeteksiConfidence = buffConf

            yolo.draw(frame, detect)                # GAMBAR Bouning BOX
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            tresh = cv2.inRange(frame, (10, 100, 20), (25, 255, 255))
            cv2.imshow('frame', frame)
            cv2.imshow('tresh', tresh)

            key = cv2.waitKey(1) & 0xFF
            # check for 'q' key-press
            if key == ord("q"):
                # if 'q' key-pressed break out
                break

    cv2.destroyAllWindows()
    cam.release()

IsStreamHandler = False
camera = ''
telegram_client = ''
sensor_reader = ''

INIT_FLAG = False
def stream_handler():
    global camera, STREAM_URL
    app.run(debug=True)

def stream_camera_frame():
    global INIT_FLAG, DeteksiClass, DataSensor,  DeteksiConfidence,\
        DeteksiFrame, STREAM_URL, STREAM_MODE, FRAME_SLEEP, FRAME_HEIGHT, FRAME_WIDTH,\
        PORT_COM, PORT_BAUD, camera, telegram_client, sensor_reader

    last_print_time = [0, 0, 0]
    print_time = 60  # detik


    if INIT_FLAG is False:
       INIT_FLAG = True
       print('CAMWERA INIT')
       camera = cv2.VideoCapture(STREAM_URL, cv2.CAP_DSHOW)

       print('TELEGRAM INIT')
       telegram_token = TELEGRAM_TOKEN
       telegram_client = TelegramClient(telegram_token)

       print('SERIAL INIT')
       sensor_reader = SensorDataReader(port=PORT_COM, baud_rate=PORT_BAUD)
       sensor_reader.open_serial_connection()


    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%Y-%m-%d")

    yolo = ImgRex()
    n = 0
    yolo.load("yolov3-tiny_training_baru.weights", "tiny.cfg", "obj.names")  ## INI GET DATA HASIL TRAINING


    while True:
        success, frame = camera.read()

        sensor_reader.read_data()
        Data = sensor_reader.get_data()
        DataSensor = Data

        if not success:
            break

        frame = resize(frame, FRAME_WIDTH, FRAME_HEIGHT)  ## RESIZE
        # print('e')
        ksize = (3, 3)  # GANJIL
        frame = cv2.blur(frame, ksize)  ## BLUR untuk Kurang Noise
        detect = yolo.predict(frame)

        buffClass = []
        buffConf = []
        for data in detect:
            buffClass.append(data['class'])
            buffConf.append(data['confidence'])

        DeteksiClass = buffClass
        DeteksiConfidence = buffConf

        DeteksiFrame = frame  # Ambil HASIL DETEKSI YOLO JIKA ADA
        yolo.draw(frame, detect)  # GAMBAR Bouning BOX
        #
        print(DataSensor, DeteksiClass, DeteksiConfidence)

        if DataSensor is not None and len(DataSensor) > 3:
            sensor = SensorData(data_list=DataSensor)
            if "api" in DeteksiClass and any(conf >= 0.33 for conf in DeteksiConfidence):
                current_time = time.time()
                # print('OTW KIRIM ', current_time, last_print_time ,current_time - last_print_time[0], current_time - last_print_time[0] >= print_time)
                if current_time - last_print_time[0] >= print_time:
                    for chat_id in CHAT_ID:
                        print("SEND NOTIF")
                        telegram_client.send_imagecv2(chat_id, DeteksiFrame)
                        telegram_client.send_message(chat_id, f"[INFO] Ada Api pada {current_date} {current_time}")
                        telegram_client.send_message(
                            chat_id,
                            "[INFO] Status Sensor Temperature={}, Humidity={}, Smoke Sensor={}".format(
                                sensor.temperature, sensor.humidity, sensor.smoke_sensor)
                        )
                        telegram_client.send_message(
                            chat_id,
                            "[INFO] Lokasi :  https://www.google.com/maps/search/?api=1&query={},{}".format(
                                sensor.latitude, sensor.longitude)
                        )
                    last_print_time[0] = current_time

            else:
                # pass
                if float(sensor.temperature) > 50 and float(sensor.smoke_sensor) > 30:
                    current_time = time.time()

                    if current_time - last_print_time[1] >= print_time:
                        for chat_id in CHAT_ID:
                            if DeteksiFrame is not None and len(DeteksiFrame) > 0:  telegram_client.send_imagecv2(
                                chat_id, DeteksiFrame)
                            telegram_client.send_message(chat_id, f"[INFO] Ada Api pada {current_date} {current_time}")
                            telegram_client.send_message(
                                chat_id,
                                "[INFO] Status Sensor Temperature={}, Humidity={}, Smoke Sensor={}"
                                .format(sensor.temperature, sensor.humidity, sensor.smoke_sensor)
                            )
                            telegram_client.send_message(
                                chat_id,
                                "[INFO] Lokasi :  https://www.google.com/maps/search/?api=1&query={},{}"
                                .format(sensor.latitude, sensor.longitude)
                            )
                        last_print_time[1] = current_time

                else:  # Tidak Ada Api
                    current_time = time.time()
                    if current_time - last_print_time[2] >= print_time:
                        print("tidak ada api", sensor.temperature, sensor.humidity)
                        last_print_time[2] = current_time


        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return redirect('/video_feed')

@app.route('/video_feed')
def video_feed():
    return Response(stream_camera_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


