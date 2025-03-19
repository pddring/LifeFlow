<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../global.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <link rel="shortcut icon" href="images/favicon.png" type="image/x-icon">
    <title>Home</title>
</head>
<body>
    <?php include '../nav.php'; ?>

    <div class="content">
        <div class="leftcont">


            <div class="card-title">
                <p>Occupancy</p>
            </div>

            <div class="card">
                <div class="pic green"><span class="material-symbols-rounded">bedroom_parent</span></div>
                <div class="text">
                    <div class="sub">Occupancy</div>
                    <div class="main">
                    <?php

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get patient count (number of rows in lifeflow_residents)
$patient_sql = "SELECT COUNT(*) AS total FROM lifeflow_residents";
$patient_result = $conn->query($patient_sql);
$patient_count = 0;

if ($patient_result && $patient_result->num_rows > 0) {
    $row = $patient_result->fetch_assoc();
    $patient_count = $row["total"];
}

// Get room count from lifeflow_stats_int where stat = 'rooms'
$room_sql = "SELECT value FROM lifeflow_stats_int WHERE stat = 'rooms' LIMIT 1"; 
$room_result = $conn->query($room_sql);
$room_count = 0;

if ($room_result && $room_result->num_rows > 0) {
    $row = $room_result->fetch_assoc();
    $room_count = $row["value"]; // Fetch the correct value
}

// Check if room_count is not zero to avoid division by zero
if ($room_count > 0) {
    // Calculate the percentage of patients to rooms
    $percentage = ($patient_count / $room_count) * 100;
} else {
    $percentage = 0; // Avoid division by zero if room_count is 0
}

// Display the result as a percentage
echo '<div class="main">' . round($percentage, 2) . '%</div>';

?>


                    </div>
                </div>
            </div>

            <div class="card">
                <div class="pic green"><span class="material-symbols-rounded">scene</span></div>
                <div class="text">
                    <div class="sub">Rooms</div>
                    <div class="main">
                    <?php

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get room count from lifeflow_stats_int where stat = 'rooms'
$room_sql = "SELECT value FROM lifeflow_stats_int WHERE stat = 'rooms' LIMIT 1"; 
$room_result = $conn->query($room_sql);
$room_count = 0;

if ($room_result && $room_result->num_rows > 0) {
    $row = $room_result->fetch_assoc();
    $room_count = $row["value"]; // Fetch the correct value
}

// Display result as "patient_count / room_count"
echo '<div class="main">' . $room_count . '</div>';
?>

                    </div>
                </div>
            </div>

            <div class="card">
                <div class="pic green"><span class="material-symbols-rounded">bedroom_child</span></div>
                <div class="text">
                    <div class="sub">Current Occupancy</div>
                    <?php

                    if ($conn->connect_error) {
                        die("Connection failed: " . $conn->connect_error);
                    }

                    $sql = "SELECT COUNT(*) AS total FROM lifeflow_residents";
                    $result = $conn->query($sql);

                    if ($result->num_rows > 0) {
                        $row = $result->fetch_assoc();
                        echo '<div class="main">' . $row["total"] . '</div>';
                    } else {
                        echo "No records found";
                    }
                    ?>
                </div>
            </div>

         


            <div class="card-title">
                <p>Finance</p>
            </div>


            <div class="card">
                <div class="pic blue"><span class="material-symbols-rounded">bedroom_child</span></div>
                <div class="text">
                    <div class="sub">Average Weekly Fee</div>
                    <div class="main">-</div>
                </div>
            </div>


            <div class="card">
                <div class="pic blue"><span class="material-symbols-rounded">bedroom_parent</span></div>
                <div class="text">
                    <div class="sub">Weekly Earnings</div>
                    <div class="main">-</div>
                </div>
            </div>
        </div>




        <div class="rightcont">


            

            <div class="card-title">
                <p>Team</p>
            </div>


            <div class="card">
                <div class="pic pink"><span class="material-symbols-rounded">bedroom_child</span></div>
                <div class="text">
                    <div class="sub">Current Staff</div>
                    <div class="main">                    
                        
                    <?php
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT value FROM lifeflow_stats_int WHERE stat = 'staff' LIMIT 1";
$result = $conn->query($sql);

if ($result && $result->num_rows > 0) {
    $row = $result->fetch_assoc();
    echo '<div class="main">' . $row['value'] . '</div>';
} else {
    echo "No records found";
}
?>

            </div>
                </div>
            </div>


            <div class="card-title">
                <p>Incidents</p>
            </div>


            <div class="card">
                <div class="pic red"><span class="material-symbols-rounded">bedroom_child</span></div>
                <div class="text">
                    <div class="sub">Last 7 Days</div>
                    <div class="main">
                    <?php

                        if ($conn->connect_error) {
                            die("Connection failed: " . $conn->connect_error);
                        }

                        $sql = "SELECT COUNT(*) AS total FROM lifeflow_incidents WHERE timestamp >= NOW() - INTERVAL 7 DAY";
                        $result = $conn->query($sql);

                        if ($result->num_rows > 0) {
                            $row = $result->fetch_assoc();
                            echo '<div class="main">' . $row["total"] . '</div>';
                        } else {
                            echo "<div class='main'>0</div>";
                        }
                        ?>
                    </div>
                </div>
            </div>


            <div class="card">
                <div class="pic red"><span class="material-symbols-rounded">bedroom_child</span></div>
                <div class="text">
                    <div class="sub">Incidents Today</div>
                    <div class="main"><?php
                        if ($conn->connect_error) {
                            die("Connection failed: " . $conn->connect_error);
                        }

                        // SQL query to count incidents only from today
                        $sql = "SELECT COUNT(*) AS total FROM lifeflow_incidents WHERE DATE(timestamp) = CURDATE()";
                        $result = $conn->query($sql);

                        if ($result->num_rows > 0) {
                            $row = $result->fetch_assoc();
                            echo '<div class="main">' . $row["total"] . '</div>';
                        } else {
                            echo "<div class='main'>0</div>";
                        }

                    ?></div>
                </div>
            </div>

            
        </div>
    </div>
    
</body>
</html>