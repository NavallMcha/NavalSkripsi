import folium

def create_map(latitude, longitude):
    # Buat objek peta dengan titik awal berdasarkan latitude dan longitude yang diberikan
    map_object = folium.Map(location=[latitude, longitude], zoom_start=10)

    # Tambahkan penanda (marker) pada posisi yang diberikan
    folium.Marker(location=[latitude, longitude], popup="Lokasi Anda").add_to(map_object)

    # Simpan peta ke file HTML
    map_object.save("map.html")

# Contoh input longitude dan latitude (ganti dengan nilai sesuai koordinat Anda)
latitude = -8.123614
longitude = 112.549310

# Buat peta dan simpan ke file HTML
create_map(latitude, longitude)
