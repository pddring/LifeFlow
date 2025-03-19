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
        <?php
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Query to fetch patient data
$sql = "SELECT id, first_name, last_name FROM lifeflow_residents";
$result = $conn->query($sql);
?>

<label for="patient">Resident</label>
<select class="form-item" id="patient" name="patient_id" required>
    <option value="" disabled selected>Select a resident</option>

    <?php
    // Loop through results to populate the select options
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $id = $row['id'];
            $first_name = $row['first_name'];
            $last_name = $row['last_name'];
            $full_name = htmlspecialchars(trim("$first_name $last_name"));

            echo '<option value="' . htmlspecialchars($id) . '">' . $full_name . '</option>';
        }
    } else {
        echo '<option value="">No residents found</option>';
    }
    ?>
</select>

        <label for="email">Incident Type</label>
        <input class="form-item" type="text" id="email" name="type" required>

        <!--<label for="message">Message:</label>
        <textarea class="form-item" id="message" name="message" required></textarea>
        <br><br>-->

        <input id="confirm" type="submit" value="Confirm">
        <input id="cancel"type="button" onclick="window.location.href='../'" value="Cancel">
    </form>
    </div>
    <?php
// Check if the 'error' parameter is set and is an integer
if (isset($_GET['error'])) {
    $error = (int)$_GET['error']; // Cast to integer for safe comparison

    if ($error === 0) {
        echo "<script>alert('Resident not found'); window.location.href='index.php';</script>";
        exit; // Stop script execution after the alert
    } elseif ($error === 1) {
        echo "<script>alert('Error inserting record'); window.location.href='index.php';</script>";
        exit; // Stop script execution after the alert
    }
}
?>


?>
</body>
</html>