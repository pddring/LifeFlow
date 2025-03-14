<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../global.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <link rel="shortcut icon" href="../images/favicon.png" type="image/x-icon">
    <title>Hubs</title>
</head>
<body>
<?php include '../nav.php'; ?>

    <div class="content">
        <div class="leftcont">


            

            <div class="card-title">
                <p>Stats</p>
            </div>


            <div class="card">
                <div class="pic green"><span class="material-symbols-rounded">check_box_outline_blank</span></div>
                <div class="text">
                    <div class="sub">Devices</div>
                    <div class="main"><?php

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT COUNT(*) AS total FROM lifeflow_hubs";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    echo '<div class="main">' . $row["total"] . '</div>';
} else {
    echo "No records found";
}
?></div>
                </div>
            </div>

            <div class="card-title">
                <p>LifeFlow Hubs</p>
            </div>

            <?php
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Query to fetch resident data with a join
$sql = "SELECT h.id, h.room, h.patient_id, r.name 
        FROM lifeflow_hubs h
        LEFT JOIN lifeflow_residents r ON h.patient_id = r.id"; 

$result = $conn->query($sql);

// Check if there are results
if ($result->num_rows > 0) {
    // Loop through the results and generate cards
    while($row = $result->fetch_assoc()) {
        $name = isset($row["name"]) ? $row["name"] : "Unknown"; // Handle missing names
        $id = $row["id"];
        
        echo '
        <div class="card">
            <div class="pic blue"><span class="material-symbols-rounded">person</span></div>
            <div class="text">
                <div class="sub">User  -  ' . htmlspecialchars($name) . '</div>
                <div class="main">' . htmlspecialchars(str_pad($id, 3, '0', STR_PAD_LEFT)) . '</div>
            </div>
        </div>';
    }
} else {
    echo "No hubs found.";
}
?>



        </div>




        <div class="rightcont">




            
            
        </div>
    </div>
    
</body>
</html>