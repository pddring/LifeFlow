
    async function run1() {
      let n = await eel.readData("reminder_slot_1_time")();
      if (n != "") {
        localStorage.setItem('alert1', n);
      }
    }
  
    run1();


  async function run2() {
    let n = await eel.readData("reminder_slot_2_time")();
    if (n != "") {
      localStorage.setItem('alert2', n);
    }
  }

  run2();


// Function to update the time display
function updateTime() {
    const timeDisplay = document.getElementById('clock');
    const currentTime = new Date();
    const date = currentTime.getDate().toString();
    const hours = currentTime.getHours().toString().padStart(2, '0');
    const minutes = currentTime.getMinutes().toString().padStart(2, '0');
    const formattedTime = `${hours}:${minutes}`;

    timeDisplay.textContent = formattedTime;

    if (localStorage.getItem("alert1").includes(formattedTime.toString()) && localStorage.getItem("alert1_shown") != date) {
      document.getElementById("popup-name").innerHTML = localStorage.getItem("alert1");
      localStorage.setItem("alert1", "")
      localStorage.setItem("alert1_shown", date)
      document.getElementById("popup").showModal();
    }
    if (localStorage.getItem("alert2").includes(formattedTime.toString()) && localStorage.getItem("alert2_shown") != date) {
      document.getElementById("popup-name").innerHTML = localStorage.getItem("alert2");
      localStorage.setItem("alert2", "")
      localStorage.setItem("alert2_shown", date)
      document.getElementById("popup").showModal();
    }
  }

  // Update time every minute (60000 milliseconds)
  setInterval(updateTime, 5000);

  // Initial time update
  updateTime();