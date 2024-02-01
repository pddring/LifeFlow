// Function to update the time display
function updateTime() {
    const timeDisplay = document.getElementById('clock');
    const currentTime = new Date();
    const hours = currentTime.getHours().toString().padStart(2, '0');
    const minutes = currentTime.getMinutes().toString().padStart(2, '0');
    const formattedTime = `${hours}:${minutes}`;

    timeDisplay.textContent = formattedTime;
  }

  // Update time every minute (60000 milliseconds)
  setInterval(updateTime, 5000);

  // Initial time update
  updateTime();