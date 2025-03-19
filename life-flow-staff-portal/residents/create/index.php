<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../../global.css">
    <link rel="stylesheet" href="../../form.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <link rel="shortcut icon" href="../../images/favicon.png" type="image/x-icon">
    <title>Residents</title>
</head>
<body>
<?php include '../../nav.php'; ?>
    <div class="content">
        <p>Add Resident</p>
        <form  action="process.php" method="post">
        <form action="process.php" method="POST">
    <!-- Name input -->
    <label for="first_name">First Name</label>
    <input class="form-item" type="text" id="first_name" name="first_name" required>

    <label for="last_name">Last Name</label>
    <input class="form-item" type="text" id="last_name" name="last_name" required>

    <!-- Gender selection -->
    <label for="gender">Gender</label>
    <select class="form-item" id="gender" name="gender" required>
        <option value="male">Male</option>
        <option value="female">Female</option>
        <option value="other">Other</option>
    </select>

    <!-- Age input -->
    <label for="age">Age</label>
    <input class="form-item" value="50" type="number" id="age" name="age" required>

    <!-- Room input -->
    <label for="room">Room</label>
    <input class="form-item" type="number" id="room" name="room" required>

    <input id="confirm" type="submit" value="Confirm">
    <input id="cancel" type="button" onclick="window.location.href='../'" value="Cancel">
</form>

    </div>
    <?php
// Check if the 'error' parameter is set and is an integer
if (isset($_GET['error'])) {
    $error = (int)$_GET['error']; // Cast to integer for safe comparison

    if ($error === 0) {
        echo "<script>alert('Connection error'); window.location.href='index.php';</script>";
        exit; // Stop script execution after the alert
    } elseif ($error === 1) {
        echo "<script>alert('Stmt error'); window.location.href='index.php';</script>";
        exit; // Stop script execution after the alert
    }
    elseif ($error === 2) {
        echo "<script>alert('Please fill all fields'); window.location.href='index.php';</script>";
        exit; // Stop script execution after the alert
    }
}
?>


?>
</body>
</html>