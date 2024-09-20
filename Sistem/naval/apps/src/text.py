import datetime

# Mendapatkan tanggal dan waktu saat ini
sekarang = datetime.datetime.now()

# Memformat tanggal dan waktu tanpa fraksi detik
hasil_format = sekarang.strftime("%Y-%m-%d %H:%M:%S")

# Mencetak hasil format
print("Tanggal dan waktu saat ini tanpa fraksi detik:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
