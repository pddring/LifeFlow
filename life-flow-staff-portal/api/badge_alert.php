<?php
// Set response header for content type
header('Content-Type: application/json');

// MySQL database connection credentials
$servername = "localhost"; // Database server
$username = "root"; // Database username
$password = ""; // Database password (empty password in this case)
$dbname = "lifeflow_data"; // Database name

// Get the badge_id from the URL parameter
if (isset($_GET['badge_id'])) {
    $badge_id = $_GET['badge_id'];
} else {
    echo json_encode(["status" => "error", "message" => "badge_id parameter missing"]);
    exit;
}

// Create a new mysqli connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check if the connection was successful
if ($conn->connect_error) {
    die(json_encode(["status" => "error", "message" => "Connection failed: " . $conn->connect_error]));
}

// Prepare the SQL query to select the patient_id based on badge_id
$sql = "SELECT patient_id FROM lifeflow_badges WHERE id = ?";
$stmt = $conn->prepare($sql);

if ($stmt === false) {
    die(json_encode(["status" => "error", "message" => "SQL error: " . $conn->error]));
}

// Bind the badge_id to the SQL statement
$stmt->bind_param("i", $badge_id);

// Execute the query
$stmt->execute();

// Bind the result to a variable
$stmt->bind_result($patient_id);

// Fetch the result
if ($stmt->fetch()) {
    // If the patient_id is found, insert a new row into the lifeflow_incidents table
    $stmt->close(); // Close the first statement

    // Prepare the SQL query to insert a new incident into lifeflow_incidents
    $incident_type = "Badge Alert"; // Set the incident_type to "Fall"
    $sql2 = "INSERT INTO lifeflow_incidents (resident_id, incident_type) VALUES (?, ?)";
    $stmt2 = $conn->prepare($sql2);

    if ($stmt2 === false) {
        die(json_encode(["status" => "error", "message" => "SQL error: " . $conn->error]));
    }

    // Bind the patient_id (resident_id) and incident_type to the SQL statement
    $stmt2->bind_param("is", $patient_id, $incident_type);

    // Execute the insert query
    if ($stmt2->execute()) {
        // If the insertion is successful, return a success message
        echo json_encode([
            "status" => "success",
            "message" => "Incident recorded successfully",
            "badge_id" => $badge_id,
            "patient_id" => $patient_id,
            "incident_type" => $incident_type
        ]);
    } else {
        // If there is an error during insertion
        echo json_encode(["status" => "error", "message" => "Failed to insert incident"]);
    }

    // Close the second statement
    $stmt2->close();
} else {
    // If no matching record is found in the lifeflow_badges table
    echo json_encode(["status" => "error", "message" => "No record found for badge_id: $badge_id"]);
}

// Close the connection
$conn->close();
?>
