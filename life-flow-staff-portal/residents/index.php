<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../global.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <link rel="shortcut icon" href="../images/favicon.png" type="image/x-icon">
    <title>Residents</title>
</head>
<body>
    <?php include '../nav.php'; ?>

    <div class="content">
        <div class="leftcont">


        

            <div class="card-title">
                <p>Residents</p>
            </div>


            <?php
                            // Check connection
                if ($conn->connect_error) {
                    die("Connection failed: " . $conn->connect_error);
                }

                // Query to fetch resident data
                $sql = "SELECT name, age FROM lifeflow_residents";  // Change 'residents' to your actual table name
                $result = $conn->query($sql);

                // Check if there are results
                if ($result->num_rows > 0) {
                    // Loop through the results and generate cards
                    while($row = $result->fetch_assoc()) {
                        $name = $row["name"];
                        $age = $row["age"];
                        // You can modify the name variable to format it as you want (e.g., Midred B. to Midred B)
                        echo '
                        <div class="card">
                            <div class="pic blue"><span class="material-symbols-rounded">person</span></div>
                            <div class="text">
                                <div class="sub">Age ' . htmlspecialchars($age) . '</div>
                                <div class="main">' . htmlspecialchars($name) . '</div>
                            </div>
                        </div>';
                    }
                } else {
                    echo "No residents found.";
                }

            ?>



        </div>




        <div class="rightcont">


        <div class="card-title">
                <p>Occupancy</p>
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

                        $conn->close();
                        ?>
                </div>
            </div>
    


            
            
        </div>
    </div>

        </div>
    </div>

</body>
</html>