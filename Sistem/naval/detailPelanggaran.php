<?php
    session_start();
    error_reporting(0);
    include 'koneksi.php';

    if($_SESSION['status'] == 'login') {

    // get data id dari get
    $id_pelanggaran = $_GET['id_pelanggaran'];

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
<title>Detail Pelanggaran</title>
<style>
    body {
        background: #2f8eed; /* Warna biru muda */
        background: linear-gradient(to bottom, #2f8eed 50%, #b9c0c7 50%);
        background-size: 100% 125%; /* Ukuran latar belakang 100% lebar dan 200% tinggi */
    }
</style>
</head>
<body>

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
        <div class="col-lg-12">

            <?php
                
                $data = mysqli_query($koneksi,"SELECT * from pelanggaran WHERE id='$id_pelanggaran'");
                while($d = mysqli_fetch_array($data)){
            ?>
            <div class="card bg-white" style="border-radius: 10px;">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-1 mb-3">
                            <button type="button" class="btn btn-secondary rounded-circle" onclick="history.back()">
                                <i class="fas fa-arrow-left"></i>
                            </button>
                        </div>
                        <div class="col-md-11">
                            <h5 class="bg-secondary text-white card-title text-center py-1" style="border-radius: 10px;">Detail Data > <?= $id_pelanggaran; ?></h5>
                            <!-- Your table or content here -->
                        </div>
                    </div>

                    <div class="row justify-content-center">
                        <div class="card bg-primary col-md-3 py-2 mx-4 text-center" style="border-radius: 20px;">
                            <Label class="text-white font-weight-bold h5">Tanggal</Label>
                            <p class="text-white h6"><?= $d['tgl_pelanggaran']; ?></p>
                        </div>

                        <div class="card bg-primary col-md-3 py-3 mx-4 text-center" style="border-radius: 20px;">
                            <label class="text-white font-weight-bold h5">Jenis Pelanggaran</label>
                            <p class="text-white h6"><?= $d['jenis_pelanggaran']; ?></p>
                        </div>

                        <div class="card bg-primary col-md-3 py-3 mx-4 text-center" style="border-radius: 20px;">
                            <label class="text-white font-weight-bold h5">Nomor Plat</label>
                            <p class="text-white h6"><?= $d['nomor_plat']; ?></p>
                        </div>
                    </div>

                    <div class="row justify-content-center py-5">
                        <div class="card bg-primary col-md-5 py-2 mx-4 text-center" style="border-radius: 20px;">
                            <Label class="text-white font-weight-bold h5">Gambar Pelanggaran</Label>
                            <img src="<?= $d['gambar_pelanggaran']; ?>">
                        </div>

                        <div class="card bg-primary col-md-5 py-3 mx-4 text-center" style="border-radius: 20px;">
                            <label class="text-white font-weight-bold h5">Gambar Plat Nomor</label>
                            <img src="<?= $d['gambar_plat_nomor']; ?>">
                        </div>

                    </div>

                </div>
            </div>

            <?php
                }
            ?>

        </div>
    </div>
    </div>



<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.slim.min.js"></script>
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