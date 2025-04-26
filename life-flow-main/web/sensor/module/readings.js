// eel error, modules were working but for now generate random values for the sensor data
//
//
//
// =============================











//THIS SCRIPT IS NOT REFERENCED OR USED

/*

let hub_id; // Declare a variable for hub_id

// Fetch the hub_id from eel asynchronously
eel.readData("hub")(function (data) {
    hub_id = data; // Set the hub_id once the data is fetched
    console.log('Hub ID:', hub_id); // Optional: log it to make sure it's correct
});


// Function to generate random values within a range
function getRandomValue(min, max, decimals = 0) {
    let value = Math.random() * (max - min) + min;
    return parseFloat(value.toFixed(decimals)); // Return as a float value for sending in request
}

// Function to send data to the API
function sendSensorData(type, value) {
    const url = `http://localhost/api/vitals.php?hub_id=${hub_id}&type=${type}&value=${value}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(`${type} data sent successfully:`, data);
        })
        .catch(error => {
            console.error(`Error sending ${type} data:`, error);
        });
}

// Get the current page name
const page = window.location.pathname.split("/").pop();

// Object to store different fake reading ranges
const readingRanges = {
    "s-heart.html": { min: 70, max: 75, decimals: 0, autoUpdate: true, type: "pulse" },  // Heart Rate (BPM)
    "s-oxygen.html": { min: 96, max: 99, decimals: 0, autoUpdate: true, type: "oxygen" }, // Oxygen Level (%)
    "s-temp.html": { min: 36.5, max: 37.5, decimals: 1, autoUpdate: false, type: "temperature" } // Temperature (°C)
};

// Function to update the reading and send the dynamic data
function updateReading() {
    if (readingRanges[page]) {
        const dataContainer = document.getElementById("reading-container");
        if (dataContainer) {
            const { min, max, decimals, type } = readingRanges[page];
            const newValue = getRandomValue(min, max, decimals);
            dataContainer.textContent = newValue;

            // Send the dynamic data based on the sensor type (pulse, oxygen, temperature)
            sendSensorData(type, newValue); // type and value are dynamic
        }
    }
}

// If autoUpdate is enabled, start updating after 2 seconds, then continue updating every 30 seconds
if (readingRanges[page]?.autoUpdate) {
    if (page !== "s-temp.html") {
        setTimeout(() => {
            updateReading(); // First update after 2 seconds
            setInterval(updateReading, 30000); // Then update every 30 seconds
        }, 2000);
    }
}

// For temperature: Start updating only after button is clicked
document.addEventListener("DOMContentLoaded", () => {
    if (page === "s-temp.html") {
        const button = document.getElementById("take-reading-btn");
        if (button) {
            button.addEventListener("click", () => {
                // Call updateReading on button click to generate and send the temperature
                updateReading(); // Update once when button is clicked
            });
        }
    }
});


*/