<?php
// Start output buffering
ob_start();

include '../../nav.php';
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get the patient ID and incident type directly from the form
    $resident_id = isset($_POST["patient_id"]) ? intval($_POST["patient_id"]) : 0;
    $type = trim(htmlspecialchars($_POST["type"]));

    // Validate input
    if ($resident_id <= 0 || empty($type)) {
        echo "Resident and incident type are required!";
        header('Location: index.php?error=1');
        exit;
    }

    // Insert the incident record using the resident ID
    $insert_sql = "INSERT INTO lifeflow_incidents (resident_id, incident_type) VALUES (?, ?)";
    $insert_stmt = $conn->prepare($insert_sql);

    if (!$insert_stmt) {
        echo "Error preparing insert statement: " . $conn->error;
        header('Location: index.php?error=1');
        exit;
    }

    $insert_stmt->bind_param("is", $resident_id, $type);

    if ($insert_stmt->execute()) {
        echo "Incident record inserted successfully for resident ID: $resident_id with type $type.";
        header('Location: ../../');
        exit;
    } else {
        echo "Error inserting incident record: " . $conn->error;
        header('Location: index.php?error=1');
        exit;
    }

    $insert_stmt->close();
}

$conn->close();
ob_end_flush(); // Send the buffered output
?>
