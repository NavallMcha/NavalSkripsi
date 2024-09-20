import os

# Ganti direktori sesuai dengan direktori tempat gambar dan label berada
direktori = "D:/User/source/caktin_ws/YoloDatasets/236 B - Training/new dataset/grapes-datasets/grape-papaya"

# Loop melalui setiap file di direktori
for filename in os.listdir(direktori):
    # Periksa apakah file adalah gambar (dengan ekstensi .jpg)
    if filename.endswith(".jpg"):
        # Mendapatkan nomor urut dari nama file gambar
        nomor_urut = filename.split("_")[1].split(".")[0]
        
        # Konstruksi nama baru untuk gambar
        nama_baru_gambar = f"frame_papaya_{nomor_urut}.jpg"
        
        # Mendapatkan nama file label dengan ekstensi .txt
        nama_label = f"frame_{nomor_urut}.txt"

        # Periksa apakah file label ada di direktori
        if os.path.exists(os.path.join(direktori, nama_label)):
            # Konstruksi nama baru untuk file label
            nama_baru_label = f"frame_papaya_{nomor_urut}.txt"
            
            # Rename file gambar
            os.rename(os.path.join(direktori, filename), os.path.join(direktori, nama_baru_gambar))
            
            # Rename file label
            os.rename(os.path.join(direktori, nama_label), os.path.join(direktori, nama_baru_label))
        else:
            print(f"File label tidak ditemukan untuk {filename}.")
