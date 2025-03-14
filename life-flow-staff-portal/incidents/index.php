<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../global.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <link rel="shortcut icon" href="../images/favicon.png" type="image/x-icon">
    <title>Incidents</title>
</head>
<body>
<?php include '../nav.php'; ?>

    <div class="content">
        <div class="leftcont">


            

            <div class="card-title">
                <p>Stats</p>
            </div>


            <div class="card">
                <div class="pic pink"><span class="material-symbols-rounded">check_box_outline_blank</span></div>
                <div class="text">
                    <div class="sub">Weekly Incidents</div>
                    <div class="main">2</div>
                </div>
            </div>

            <div class="card-title">
                <p>Incidents</p>
            </div>

            <?php
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Query to fetch the latest 10 incidents with resident names and read_status
$sql = "
    SELECT r.name, i.incident_type, i.timestamp, i.read_status 
    FROM lifeflow_incidents i
    JOIN lifeflow_residents r ON i.resident_id = r.id
    ORDER BY i.timestamp DESC 
    LIMIT 10";

$result = $conn->query($sql);

// Check if there are results
if ($result->num_rows > 0) {
    // Loop through the results and generate cards
    while ($row = $result->fetch_assoc()) {
        $name = htmlspecialchars($row["name"]);
        $incident_type = htmlspecialchars($row["incident_type"]);
        $timestamp = htmlspecialchars($row["timestamp"]);
        $read_status = $row["read_status"];

        // Determine the class based on read_status
        $pic_class = $read_status == 0 ? 'white' : 'red'; // 'white' if unread, 'red' if read

        echo '
        <div class="card">
            <div class="pic ' . $pic_class . '"><span class="material-symbols-rounded">report</span></div>
            <div class="text">
                <div class="sub">' . $name . '    |    ' . $timestamp . '</div>
                <div class="main">' . $incident_type . '</div>
            </div>
        </div>';
    }
} else {
    echo "No incidents found.";
}
?>





        </div>




        <div class="rightcont">


            

            <div class="card-title">
                <p></p>
            </div>


            <div class="card">
                <div class="pic pink"><span class="material-symbols-rounded">check_box_outline_blank</span></div>
                <div class="text">
                    <div class="sub">Daily Incidents</div>
                    <div class="main">0</div>
                </div>
            </div>


            
            
        </div>
    </div>

</body>
</html>