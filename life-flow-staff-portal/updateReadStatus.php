<?php
// Database connection settings
$host = "localhost";
$username = "root";
$password = "";
$dbname = "lifeflow_data";

// Read the incoming JSON data (optional for checking status)
$data = json_decode(file_get_contents('php://input'), true);

// Create a PDO connection to the database
try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // SQL query to update read_status to 1
    $stmt = $pdo->prepare("UPDATE lifeflow_incidents SET read_status = 1 WHERE read_status = 0");
    $stmt->execute();

    // Return a JSON response confirming the update
    echo json_encode(['success' => true]);
} catch (PDOException $e) {
    echo json_encode(['error' => 'Database connection failed: ' . $e->getMessage()]);
}
?>
