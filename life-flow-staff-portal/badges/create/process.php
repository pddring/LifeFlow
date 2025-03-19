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

    // Validate the input
    if (empty($patient_id) || !is_numeric($patient_id)) {
        header('Location: index.php?error=2');
        exit;
    }

    $sql = "INSERT INTO lifeflow_badges (patient_id) VALUES (?)";

    // Initialize prepared statement
    if ($stmt = $conn->prepare($sql)) {
        // Bind parameters to the SQL query
        $stmt->bind_param("i", $patient_id); // Bind as integer

        // Execute the query
        if ($stmt->execute()) {
            // Redirect after successful insertion
            header('Location: ../'); // No further output after this
            exit;
        } else {
            // Handle error
            header('Location: index.php?error=1');
            exit;
        }

        // Close the prepared statement
        $stmt->close();
    } else {
        // Handle preparation error
        header('Location: index.php?error=0');
        exit;
    }
}

// Close connection
$conn->close();
?>
