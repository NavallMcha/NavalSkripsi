<?php
// Koneksi ke database
$koneksi = mysqli_connect("localhost", "root", "", "navalweb");

// Periksa koneksi
if (mysqli_connect_errno()) {
    die("Koneksi database gagal: " . mysqli_connect_error());
}

// Query untuk mengambil data dari database
$query = "SELECT * FROM pelanggaran";
$result = mysqli_query($koneksi, $query);

// Buat array untuk menyimpan hasil query
$data = array();

// Iterasi hasil query dan simpan ke dalam array
while ($row = mysqli_fetch_assoc($result)) {
    $data[] = $row;
}

// Mengembalikan data dalam format JSON
echo json_encode($data);

// Tutup koneksi database
mysqli_close($koneksi);
?>

