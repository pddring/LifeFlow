//eel error, modules were working but for now generate random values for the sensor data
//
//
//
//
//
//
// =============================

// Function to generate random values within a range
function getRandomValue(min, max, decimals = 0) {
    let value = Math.random() * (max - min) + min;
    return `-- ${value.toFixed(decimals)} --`;
}

// Get the current page name
const page = window.location.pathname.split("/").pop();

// Object to store different fake reading ranges
const readingRanges = {
    "s-heart.html": { min: 70, max: 75, decimals: 0, autoUpdate: true },  // Heart Rate (BPM) - No decimals
    "s-oxygen.html": { min: 96, max: 99, decimals: 0, autoUpdate: true }, // Oxygen Level (%) - No decimals
    "s-temp.html": { min: 36.5, max: 37.5, decimals: 1, autoUpdate: false } // Temperature (°C) - 1 decimal, manual start
};

// Function to update the reading
function updateReading() {
    if (readingRanges[page]) {
        const dataContainer = document.getElementById("reading-container");
        if (dataContainer) {
            const { min, max, decimals } = readingRanges[page];
            dataContainer.textContent = getRandomValue(min, max, decimals);
        }
    }
}

// Auto-update every 0.5 seconds for heart rate and oxygen
if (readingRanges[page]?.autoUpdate) {
    setInterval(updateReading, 2000);
}

// For temperature: Start updating only after button is clicked
document.addEventListener("DOMContentLoaded", () => {
    if (page === "s-temp.html") {
        const button = document.getElementById("take-reading-btn");
        if (button) {
            button.addEventListener("click", () => {
                updateReading(); // First update immediately
                updateReading();
            });
        }
    }
});