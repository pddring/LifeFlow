<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "lifeflow_data";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form input values
    $patient_id = $_POST['patient_id']; // ID of the selected patient
    $room = trim($_POST['room']); // Room input

    // Validate the input
    if (empty($patient_id) || empty($room)) {
        header('Location: index.php?error=2');
        exit;
    }

    // Prepare the SQL query to insert a new row into 'lifeflow_hubs'
    $sql = "INSERT INTO lifeflow_hubs (patient_id, room) VALUES (?, ?)";

    // Initialize prepared statement
    if ($stmt = $conn->prepare($sql)) {
        // Bind parameters to the SQL query
        $stmt->bind_param("is", $patient_id, $room);

        // Execute the query
        if ($stmt->execute()) {
            echo "New row created successfully!";
            header('Location: ../');
        } else {
            echo "Error: " . $stmt->error;
            header('Location: index.php?error=1');
        }

        // Close the prepared statement
        $stmt->close();
    } else {
        echo "Error: " . $conn->error;
        header('Location: index.php?error=0');
    }
}

// Close connection
$conn->close();
?>
