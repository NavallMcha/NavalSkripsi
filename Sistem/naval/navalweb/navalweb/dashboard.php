<?php
    session_start();
    error_reporting(0);
    include 'koneksi.php';

    if($_SESSION['status'] == 'login') {

?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="ie=edge">
<meta name="Description" content="Enter your description here"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.6.0/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
<link rel="stylesheet" href="assets/css/style.css">
<title>Dashboard</title>
<style>
    body {
        background: #2f8eed; /* Warna biru muda */
        background: linear-gradient(to bottom, #2f8eed 50%, #b9c0c7 50%);
        background-size: 100% 150%; /* Ukuran latar belakang 100% lebar dan 200% tinggi */
    }
</style>
</head>
<body>
<?php
if($_SESSION['status'!="login"]){
    header("location:index.php?pesan=belum_login");
}
?>

    <nav class="navbar navbar-expand-sm navbar-dark bg-primary">
        <a class="navbar-brand" href="dashboard.php"><h1 class="text-dark font-weight-bold ml-5"><span class="text-white">POS</span> PANTAU</h1></a>
        <button class="navbar-toggler d-lg-none" type="button" data-toggle="collapse" data-target="#collapsibleNavId" aria-controls="collapsibleNavId"
            aria-expanded="false" aria-label="Toggle navigation"></button>
        <div class="collapse navbar-collapse" id="collapsibleNavId">
            <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
                
            </ul>
            <div class="form-inline my-lg-0 mr-5 text-white">
                <i class="fas fa-user fa-lg mr-3 mb-2"></i>
                <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle text-white h5" href="#" id="dropdownId" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            <?= $_SESSION['nama']; ?>
                        </a>
                        <div class="dropdown-menu" aria-labelledby="dropdownId">
                            <a class="dropdown-item" href="logout.php">Log out</a>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container" style="margin-top: 70px;">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card bg-primary" style="border-radius: 20px;">
                <h3 class="font-weight-bold text-center text-white py-3">Total Pelanggaran</h3>
                <div class="text-center py-2 mb-2">
                    <svg xmlns="http://www.w3.org/2000/svg" height="80" width="80" viewBox="0 0 640 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="#ffffff" d="M400 96a48 48 0 1 0 -48-48 48 48 0 0 0 48 48zm-4 121a31.9 31.9 0 0 0 20 7h64a32 32 0 0 0 0-64h-52.8L356 103a31.9 31.9 0 0 0 -40.8 .7l-112 96a32 32 0 0 0 3.1 50.9L288 305.1V416a32 32 0 0 0 64 0V288a32 32 0 0 0 -14.3-26.6l-41.4-27.6 58.3-49.9zm116 39a128 128 0 1 0 128 128 128 128 0 0 0 -128-128zm0 192a64 64 0 1 1 64-64 64 64 0 0 1 -64 64zM128 256a128 128 0 1 0 128 128 128 128 0 0 0 -128-128zm0 192a64 64 0 1 1 64-64 64 64 0 0 1 -64 64z"/></svg>
                </div>
            </div>
        </div>
    </div>
    </div>

    <div class="container" style="margin-top: 70px;">
    <div class="row justify-content-center">
        <div class="col-lg-10">
            <div class="card bg-white" style="border-radius: 10px;">
                <div class="card-body">
                    <h5 class="card-title text-center mb-4">Data Pelanggaran</h5>
                    <div class="table-responsive">
                    <table id="data-table" class="table table-bordered table-striped">
                        <thead>
                            <tr>
                                <th>No.</th>
                                <th>Tanggal</th>
                                <th>Jenis Pelanggaran</th>
                                <th>Nomor Plat</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <?php
                            // $no = 1;
                            // $data = mysqli_query($koneksi, "SELECT * FROM pelanggaran");
                            // while ($d = mysqli_fetch_array($data)) {
                        ?>
                        <tbody>
                            
                        </tbody>
                        <?php //} ?>
                    </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
function loadTableData() {
    $.ajax({
        url: 'getData.php',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            $('#data-table tbody').empty();

            console.log(data);

            $.each(data, function(index, item) {
                var row =   '<tr>' +
                                '<td>' + (index + 1) + '</td>' +
                                '<td>' + item.tgl_pelanggaran + '</td>' +
                                '<td>' + item.jenis_pelanggaran + '</td>' +
                                '<td>' + item.nomor_plat + '</td>' +
                                '<td><a href="detailPelanggaran.php?id_pelanggaran=' + item.id + '" class="btn btn-success">Detail</a></td>' +
                            '</tr>';
                $('#data-table tbody').append(row);
            
            });
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText);
        }
    });
}

setInterval(loadTableData, 1000);

$(document).ready(function() {
    loadTableData();
});
</script>


<!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.slim.min.js"></script> -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.1/umd/popper.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.6.0/js/bootstrap.min.js"></script>
</body>
</html>
<?php 
    }

    else {
        header("location:index.php?login=false");
        $_SESSION['login'] = "false";
    }
?>