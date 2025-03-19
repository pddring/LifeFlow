<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../../global.css">
    <link rel="stylesheet" href="../../form.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <link rel="shortcut icon" href="../../images/favicon.png" type="image/x-icon">
    <title>Hubs</title>
</head>
<body>
<?php include '../../nav.php'; ?>
    <div class="content">




        <?php
            // Retrieve the 'id' parameter from the query string
            if (isset($_GET['id'])) {
                $id = $_GET['id'];
                echo "<p> Edit Hub " . htmlspecialchars(str_pad($id, 3, '0', STR_PAD_LEFT)) . "</p>";
            } else {
                echo "ID parameter is missing.";
            }
        ?>


<?php
// Database connection (Replace with your actual credentials)
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "lifeflow_data";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Retrieve the 'id' parameter from the query string
$id = isset($_GET['id']) ? (int) $_GET['id'] : null;

// Fetch data for the specific ID
$details = [];
if ($id) {
    $sqlDetails = "SELECT patient_id, room FROM lifeflow_hubs WHERE id = ?";
    $stmt = $conn->prepare($sqlDetails);
    $stmt->bind_param("i", $id);
    $stmt->execute();
    $details = $stmt->get_result()->fetch_assoc();
}

// Query to fetch all residents
$sqlResidents = "SELECT id, first_name, last_name FROM lifeflow_residents";
$resultResidents = $conn->query($sqlResidents);
?>

<form action="process.php" method="POST">
    <label for="patient">Assigned Resident</label>
    <select class="form-item" id="patient" name="patient_id" required>
        <option value="" disabled>Select a resident</option>
        <?php
        if ($resultResidents->num_rows > 0) {
            while ($row = $resultResidents->fetch_assoc()) {
                $selected = (isset($details['patient_id']) && $details['patient_id'] == $row['id']) ? 'selected' : '';
                echo '<option value="' . htmlspecialchars($row['id']) . '" ' . $selected . '>'
                    . htmlspecialchars(trim($row['first_name'] . ' ' . $row['last_name'])) . '</option>';
            }
        } else {
            echo '<option value="">No residents found</option>';
        }
        ?>
    </select>

    <label for="room">Room</label>
    <input class="form-item" type="number" id="room" name="room"
        value="<?php echo isset($details['room']) ? htmlspecialchars($details['room']) : ''; ?>" required>

    <?php
    // Output the id as a hidden input field (if present)
    if ($id) {
        echo '<input type="hidden" name="id" value="' . htmlspecialchars($id) . '" />';
    }
    ?>

    <input id="confirm" type="submit" value="Confirm">
    <input id="cancel" type="button" onclick="window.location.href='../'" value="Cancel">
</form>

<?php
// Close the database connection
$conn->close();
?>



        
      

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
</body>
</html>