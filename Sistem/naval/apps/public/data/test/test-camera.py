import cv2

# Buka video
video_path = 'data/hands/hands-video.mp4'
cap = cv2.VideoCapture(video_path)

# Cek apakah video berhasil dibuka
if not cap.isOpened():
    print("Video tidak dapat dibuka")
    exit()

# Loop untuk membaca dan memutar video
while True:
    ret, frame = cap.read()

    # Cek apakah frame berhasil dibaca
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Mengatur posisi frame kembali ke awal
        continue

    cv2.imshow('Video', frame)

    # Hentikan loop jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bebaskan sumber daya
cap.release()
cv2.destroyAllWindows()
