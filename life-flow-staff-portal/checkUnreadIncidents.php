<?php
// Database connection settings
$host = "localhost";
$username = "root";
$password = "";
$dbname = "lifeflow_data";

// Create a PDO connection to the database
try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // SQL query to check for unread incidents
    $stmt = $pdo->query("SELECT * FROM lifeflow_incidents WHERE read_status = 0");
    $unreadIncidents = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Return a JSON response with whether there are unread incidents
    echo json_encode(['hasUnread' => count($unreadIncidents) > 0]);
} catch (PDOException $e) {
    echo json_encode(['error' => 'Database connection failed: ' . $e->getMessage()]);
}
?>
