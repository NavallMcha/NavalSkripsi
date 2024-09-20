import cv2
import os
import time

def extract_frames(video_path, output_directory, interval):
    # Membaca video
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    frame_count = 262

    # Membuat direktori output jika belum ada
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    while success:
        # Mengambil frame pada interval yang ditentukan
        if count % interval == 0:
            # Menyimpan frame sebagai gambar JPG
            frame_path = os.path.join(output_directory, f"frame_{frame_count:05d}.jpg")
            cv2.imwrite(frame_path, image)
            print(f"[INFO] {time.time()}.{count}.{frame_count} Image Write at frame_{frame_count:05d}.jpg")
            frame_count += 1

        success, image = vidcap.read()
        count += 1
    vidcap.release()
    print(f"[INFO] {count}.{frame_count} Convert Done")

# Memanggil fungsi untuk mengubah video menjadi urutan gambar JPG
video_path = 'D:/User/source/caktin_ws/YoloDatasets/2315 - Training/py/cat-video-3.mp4'
output_directory = 'D:/User/source/caktin_ws/YoloDatasets/2315 - Training/py/cat1'
interval = 120  # Ambil setiap interval detik
extract_frames(video_path, output_directory, interval)
