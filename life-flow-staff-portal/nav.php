<div class="sidebar">
        <div class="title"><a href="../../"><img title="home" src="../../images/lifeflow.svg" alt="LifeFlow."></a></div>
        <div class="links">
            <a class="link" href="../../">
                <div class="icon"><span class="material-symbols-rounded">home</span></div> Home
            </a>
            <a class="link" href="../../residents/">
                <div class="icon"><span class="material-symbols-rounded">groups</span></div> Residents
            </a>
            <a class="link" href="../../incidents/">
                <div class="icon"><span class="material-symbols-rounded">warning</span></div> Incidents
            </a>
            <a class="link" href="../../hubs/">
                <div class="icon"><span class="material-symbols-rounded">hub</span></div> LifeFlow Hubs
            </a>
            <a class="link" href="../../badges/">
                <div class="icon"><span class="material-symbols-rounded">badge</span></div> LifeFlow Badges
            </a>
        </div>
    </div>
    
    <div class="top-bar">
        <div class="left">

        </div>
        <div class="right">
            <span class="topicon" title="help"><span class="material-symbols-rounded">help</span></span>
            <span id="notifications" class="topicon" title="notifications"><span class="material-symbols-rounded">notifications</span>
            <div class="circle" id="cirlce"></div>
        </span>
            <div class="profile" title="profile">
                <div class="profile-info">
                    <span class="name">John. S</span>
                    <span class="role">Admin</span>
                </div>
                <img src="../../images/pfp.jpg" alt="Profile">
            </div>
        </div>
    </div>

    <script>


document.addEventListener("DOMContentLoaded", function () {
    // Get the URL path and filter out empty segments
    let urlSegments = window.location.pathname.split("/").filter(seg => seg);
let firstSegment = urlSegments.length ? urlSegments[0] : null; // Get first segment or null

console.log("URL Segments:", urlSegments);
console.log("First Segment:", firstSegment);

// Select all <a> elements
document.querySelectorAll("a").forEach(a => {
    let href = a.getAttribute("href");
    console.log("Checking href:", href);

    // If there are subfolders, match the first segment
    if (firstSegment && href.includes(firstSegment)) {
        a.classList.add("active");
    } 
    // If no subfolders, apply "active" only to href="../"
    else if (!firstSegment && href === "../") {
        a.classList.add("active");
    }
});



    document.querySelector('.left').innerHTML = document.title;


    const notifications = document.getElementById("notifications");
    if (notifications) {
        console.log("Notifications element found");
    } else {
        console.error("Notifications element not found!");
    }

    // Function to check for unread incidents
    function checkUnreadIncidents() {
        console.log("Checking unread incidents...");

        fetch("../checkUnreadIncidents.php")
            .then(response => response.json())
            .then(data => {
                console.log("Unread incidents data:", data);
                // If there are unread incidents, show the circles by adding the "circle-active" class
                if (data.hasUnread) {
                    document.querySelectorAll(".circle").forEach(circle => {
                        // Only add "circle-active" if it hasn't been added already
                        if (!circle.classList.contains("circle-active")) {
                            circle.classList.add("circle-active");
                        }
                    });
                }
            })
            .catch(error => console.error("Error checking unread incidents:", error));
    }

    // Periodically check for unread incidents every 15 seconds (15000 milliseconds)
    setInterval(checkUnreadIncidents, 15000);
    checkUnreadIncidents();

    // If the URL contains "incidents", delay marking all as read by 3 seconds
    if (window.location.href.includes("incidents")) {
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
        }, 3000); // 3-second delay
    }

    // Handle the notification click event
    if (notifications) {
        notifications.addEventListener("click", () => {
            console.log("Notifications clicked!");

            // Only send the request if the URL does NOT contain "incidents"
                console.log("Not on incidents page. Sending request to mark as read...");
                        console.log("Redirecting to incidents...");
                        window.location.href = "../../incidents/";
        });
    }
});










    </script>

    <?php
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "lifeflow_data";
    
    $conn = new mysqli($servername, $username, $password, $dbname);
    ?>