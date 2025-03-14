<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../../global.css">
    <link rel="stylesheet" href="../../form.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <link rel="shortcut icon" href="../../images/favicon.png" type="image/x-icon">
    <title>Log Incident</title>
</head>
<body>
<?php include '../../nav.php'; ?>

    <div class="content">
        <p>Add Incident</p>
        <form  action="process.php" method="post">
        <label for="name">Resident Name</label>
        <input class="form-item" type="text" id="name" name="name" required>
        <br><br>

        <label for="email">Incident Type</label>
        <input class="form-item" type="email" id="email" name="email" required>
        <br><br>

        <!--<label for="message">Message:</label>
        <textarea class="form-item" id="message" name="message" required></textarea>
        <br><br>-->

        <input id="confirm" type="submit" value="Confirm">
        <input id="cancel"type="button" onclick="window.location.href='../'" value="Cancel">
    </form>
    </div>
    
</body>
</html>