import os

# Tentukan direktori file gambar
direktori = 'D:/User/source/caktin_ws/YoloDatasets/2315 - Training/cat-video-2-compressed'

# Loop melalui file gambar
for i in range(1, 501):
    # Bentuk nama file lama dan baru
    nama_lama = f'{direktori}/{"{:04d}".format(i)}.jpg'
    nama_baru = f'{direktori}/{"{:04d}".format(i+500)}.jpg'

    # Ubah nama file
    os.rename(nama_lama, nama_baru)

print("Pengubahan nama file selesai.")
