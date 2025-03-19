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
    $id = $_POST['id']; // The ID passed from the query string (which identifies the row in lifeflow_hubs)

    // Validate the input
    if (empty($patient_id) || empty($id)) {
        header('Location: index.php?error=2');
        exit;
    }

    // Prepare the SQL query to update the 'lifeflow_badges' table
    $sql = "UPDATE lifeflow_badges SET patient_id = ? WHERE id = ?";

    // Initialize prepared statement
    if ($stmt = $conn->prepare($sql)) {
        // Bind parameters to the SQL query
        // Ensure that the types of the parameters match the column types in the database
        $stmt->bind_param("ii", $patient_id, $id);  // assuming both are integers

        // Execute the query
        if ($stmt->execute()) {
            // Redirect to the homepage on success
            header('Location: ../');
            exit;
        } else {
            // Error during execution
            header('Location: index.php?error=1');
            exit;
        }

        // Close the prepared statement
        $stmt->close();
    } else {
        // Error preparing the SQL query
        header('Location: index.php?error=0');
        exit;
    }
}

// Close connection
$conn->close();
?>
