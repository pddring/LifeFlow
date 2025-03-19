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
    $first_name = trim($_POST['first_name']);
    $last_name = trim($_POST['last_name']);
    $gender = $_POST['gender'];
    $age = $_POST['age'];
    $room = $_POST['room'];

    // Validate the input
    if (empty($first_name) || empty($last_name) || empty($gender) || empty($age) || empty($room)) {
        header('Location: index.php?error=2');
        exit;
    }

    // Prepare the SQL query with first_name and last_name
    $sql = "INSERT INTO lifeflow_residents (first_name, last_name, gender, age, room) VALUES (?, ?, ?, ?, ?)";

    // Initialize prepared statement
    if ($stmt = $conn->prepare($sql)) {
        // Bind parameters to the SQL query
        $stmt->bind_param("sssii", $first_name, $last_name, $gender, $age, $room);

        // Execute the query
        if ($stmt->execute()) {
            echo "New resident added successfully!";
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
