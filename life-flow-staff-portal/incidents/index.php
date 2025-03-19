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
                <div class="pic pink"><span class="material-symbols-rounded">bedroom_child</span></div>
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

            <div class="card-title">
                <p>Incidents</p><a class="material-symbols-rounded action" href="create">add</a>
            </div>

            <?php
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Default limit is 10 if not set in the URL
$limit = isset($_GET['limit']) ? (int)$_GET['limit'] : 10;

// Query to fetch incidents with first and last names and a dynamic limit
$sql = "
    SELECT r.first_name, r.last_name, i.incident_type, i.timestamp, i.read_status 
    FROM lifeflow_incidents i
    JOIN lifeflow_residents r ON i.resident_id = r.id
    ORDER BY i.timestamp DESC 
    LIMIT $limit";

$result = $conn->query($sql);

// Check if there are results
if ($result->num_rows > 0) {
    // Loop through the results and generate cards
    while ($row = $result->fetch_assoc()) {
        $first_name = htmlspecialchars($row["first_name"]);
        $last_name = htmlspecialchars($row["last_name"]);
        $full_name = trim("$first_name $last_name");  // Combine first and last names
        $incident_type = htmlspecialchars($row["incident_type"]);
        $timestamp = htmlspecialchars($row["timestamp"]);
        $read_status = $row["read_status"];

        // Determine the class based on read_status
        $pic_class = $read_status == 0 ? 'white' : 'red'; // 'white' if unread, 'red' if read

        echo '
        <div class="card" id="card_' . $row["timestamp"] . '">
            <div class="pic ' . $pic_class . '"><span class="material-symbols-rounded">report</span></div>
            <div class="text">
                <div class="sub">' . $full_name . ' | ' . $timestamp . '</div>
                <div class="main">' . $incident_type . '</div>
            </div>
        </div>';
    }

    // Check if there are more incidents to load (more than the current limit)
    $totalIncidentsQuery = "SELECT COUNT(*) as total FROM lifeflow_incidents";
    $totalIncidentsResult = $conn->query($totalIncidentsQuery);
    $totalIncidentsRow = $totalIncidentsResult->fetch_assoc();
    $totalIncidents = $totalIncidentsRow['total'];

    // Only show the "Load More" button if there are more incidents
    if ($limit < $totalIncidents) {
        $newLimit = $limit + 10;
        echo '<a href="?limit=' . $newLimit . '" class="load-more-button" id="loadMoreButton">Load More</a>';
    }

    // Display the "Load All" button
    if ($limit < $totalIncidents) {
        echo '<a href="javascript:void(0);" class="load-all-button" id="loadAllButton">Load All</a>';
    }

} else {
    echo "No incidents found.";
}
?>


<script>
// JavaScript to handle the buttons and confirmation for "Load All"
document.addEventListener("DOMContentLoaded", function() {
    const loadMoreButton = document.getElementById("loadMoreButton");
    const loadAllButton = document.getElementById("loadAllButton");

    // Store the current limit so we can revert if necessary
    let previousLimit = <?php echo $limit; ?>;

    // If "Load More" button is clicked, it loads more incidents
    if (loadMoreButton) {
        loadMoreButton.addEventListener("click", function(e) {
            // Additional actions can be added here if necessary
        });
    }

    // If "Load All" button is clicked, ask for confirmation
    if (loadAllButton) {
        loadAllButton.addEventListener("click", function(e) {
            // Show a confirmation dialog to the user
            const confirmLoadAll = confirm("Are you sure you want to load all incidents?");

            if (!confirmLoadAll) {
                // If canceled, reset the limit to the previous value
            } else {
                // If confirmed, change the limit to load all incidents
                window.location.href = `?limit=<?php echo $totalIncidents; ?>`;
            }
        });
    }
});
</script>




        </div>




        <div class="rightcont">


            

            <div class="card-title">
                <p></p>
            </div>


            <div class="card">
                <div class="pic pink"><span class="material-symbols-rounded">bedroom_child</span></div>
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


            
            
        </div>
    </div>

</body>
<script>
    
        console.log("URL contains 'incidents'. Marking all as read after 3 seconds...");

        // Delay the execution by 3 seconds (3000 milliseconds)
        setTimeout(() => {
            document.querySelectorAll(".circle").forEach(circle => {
                        // Only add "circle-active" if it hasn't been added already
                        if (!circle.classList.contains("circle-active")) {
                            circle.classList.remove("circle-active");
                        }
                    });
            fetch("../updateReadStatus.php", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ read_status: 1 })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Update read status response:", data);
            })
            .catch(error => console.error("Error updating read status:", error));
        }, 500); // 3-second delay
</script>
</html>