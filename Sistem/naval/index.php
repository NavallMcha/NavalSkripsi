<?php
  session_start();
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
  <script src="https://cdnjs.cloudflare.com/ajax/libs/sweetalert/2.1.2/sweetalert.min.js"></script>
  <title>Login</title>
  <style>
    .card {
      border-radius: 20px;
    }
    .form-group input {
      border-radius: 10px;
      background-color: #e9ecef; /* warna background abu-abu */
      padding: 10px;
    }
  </style>
</head>
<body class="bg-primary">

  <?php
    if(isset($_SESSION['login'])){
        unset ($_SESSION['login']);
    ?>
    <script>
        swal("Silahkan Login!","","info");
    </script>
    <?php
      }
  ?>

  <?php
    if(isset($_SESSION['pesan'])){
        unset ($_SESSION['pesan']);
    ?>
    <script>
        swal("Email dan password salah!","","info");
    </script>
    <?php
      }
  ?>

  <div class="container" style="margin-top: 100px;">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="py-5 text-center">
            <img src="assets/logo.png" alt="Logo" class="img-fluid">
          </div>
          <div class="card-body">
            <h3 class="card-title text-center">Sign In To Dashboard</h3>
            <form action="cek_login.php" method="POST">
              <div class="form-group py-2">
                <label for="email"><i class="fas fa-envelope"></i> Email</label>
                <input type="email" name="email" class="form-control" id="email" placeholder="Type your email" required>
              </div>
              <div class="form-group py-2">
                <label for="password"><i class="fas fa-lock"></i> Password</label>
                <input type="password" name="password" class="form-control" id="password" placeholder="Type your password" required>
              </div>
              <div class="text-center py-3">
                <button type="submit" class="btn-lg btn-primary">Login</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.slim.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.1/umd/popper.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.6.0/js/bootstrap.min.js"></script>
</body>
</html>