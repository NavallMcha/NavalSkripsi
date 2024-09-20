<?php
//aktifkan session
session_start();

//menghubungkan koneksi
include 'koneksi.php';

//menagkap data yang dikirim dari form
$email = $_POST['email'];
$password = $_POST['password'];

//menyeleksi data admin
$data = mysqli_query($koneksi,"select * from user where email='$email' and password='$password'");

//menghitung jumlah data
$cek = mysqli_num_rows($data);

if($cek > 0){
    // Mengambil baris pertama dari hasil kueri
    $row = mysqli_fetch_assoc($data);

    // Mendapatkan nilai kolom 'nama'
    $nama = $row['nama'];

    $_SESSION['nama'] = $nama;
    $_SESSION['status'] = "login";
    header("location:dashboard.php");
}
else{
    header("location:index.php?pesan=gagal");
    $_SESSION['pesan'] = "gagal";
}
?>