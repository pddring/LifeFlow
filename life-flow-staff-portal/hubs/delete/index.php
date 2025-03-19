<?php
// Set response header for content type
header('Content-Type: application/json');

// MySQL database connection credentials
$servername = "localhost"; // Database server
$username = "root"; // Database username
$password = ""; // Database password (empty password in this case)
$dbname = "lifeflow_data"; // Database name

// Get the 'id' from the URL parameter
if (isset($_GET['id'])) {
    $id = $_GET['id'];
} else {
    echo json_encode(["status" => "error", "message" => "'id' parameter missing"]);
    exit;
}

// Create a new mysqli connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check if the connection was successful
if ($conn->connect_error) {
    die(json_encode(["status" => "error", "message" => "Connection failed: " . $conn->connect_error]));
}

// Prepare the SQL query to delete the row with the given 'id' from the 'lifeflow_hubs' table
$sql = "DELETE FROM lifeflow_hubs WHERE id = ?";
$stmt = $conn->prepare($sql);

if ($stmt === false) {
    die(json_encode(["status" => "error", "message" => "SQL error: " . $conn->error]));
}

// Bind the 'id' parameter to the SQL statement
$stmt->bind_param("i", $id);

// Execute the delete query
if ($stmt->execute()) {
    // If the deletion is successful, redirect to ../
    header('Location: ../');
    exit;
} else {
    // If there is an error during deletion
    echo json_encode(["status" => "error", "message" => "Failed to delete the record"]);
}

// Close the statement and connection
$stmt->close();
$conn->close();
?>
