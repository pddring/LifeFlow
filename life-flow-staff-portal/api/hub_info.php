<?php
// Set the content type to JSON
header('Content-Type: application/json');

// MySQL database connection credentials
$servername = "localhost"; // Database server
$username = "root"; // Database username
$password = ""; // Database password (empty password in this case)
$dbname = "lifeflow_data"; // Database name

// Create connection to the database
$conn = new mysqli($servername, $username, $password, $dbname);

// Check the connection
if ($conn->connect_error) {
    die(json_encode(["error" => "Connection failed: " . $conn->connect_error]));
}

// Retrieve the 'id' parameter from the URL
if (isset($_GET['id'])) {
    $id = $_GET['id'];

    // Sanitize the input to prevent SQL injection
    $id = $conn->real_escape_string($id);

    // Query to fetch the row based on the 'id' from both lifeflow_hubs and lifeflow_residents, including age and gender
    $sql = "
        SELECT 
            h.room, 
            h.patient_id, 
            r.first_name, 
            r.last_name,
            r.age, 
            r.gender
        FROM 
            lifeflow_hubs h
        INNER JOIN 
            lifeflow_residents r ON h.patient_id = r.id
        WHERE 
            h.id = '$id'
    ";

    // Execute the query
    $result = $conn->query($sql);

    // Check if a result was found
    if ($result->num_rows > 0) {
        // Fetch the row and return it as JSON
        $row = $result->fetch_assoc();
        echo json_encode($row);
    } else {
        // If no result found, return an error
        echo json_encode(["error" => "No data found for the provided id."]);
    }

} else {
    // If 'id' parameter is not provided in the URL
    echo json_encode(["error" => "No 'id' parameter provided."]);
}

// Close the database connection
$conn->close();
?>
