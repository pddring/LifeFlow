let hub_id;  // Variable to store the hub_id

// Function to fetch the hub_id
eel.readData("hub")(function (data) {
    hub_id = data;  // Set the hub_id once the data is fetched
    console.log('Hub ID:', hub_id);  // Optional: log it to make sure it's correct
});

// Function to fetch the temperature and send it to the API
function temperature() {
  async function run() {
    try {
      // Call the Python function exposed through Eel
      let n = await eel.sensor_temp()(); // Calls sensor_temp() and waits for the result

      // Format the temperature data as needed
      let sval = "-- " + n.substring(0, n.length - 1) + " --";
      console.log(sval);

      // Send the fetched temperature data to the API
      sendSensorData('temperature', sval);  // Send the temperature data to the API

      // Update the HTML element with id "sensordata" to display the result
      document.getElementById("sensordata").innerText = sval;

    } catch (error) {
      console.error("Error fetching temperature:", error);
      document.getElementById("sensordata").innerText = "Error fetching data.";
    }
  }
  run(); // Invoke the function
}

// Function to send data to the API
function sendSensorData(type, value) {
  // Check if hub_id is available before making the API call
  if (!hub_id) {
    console.error("Hub ID not yet set");
    return;
  }

  // Construct the API URL with the hub_id, type, and value
  const url = `http://localhost/api/vitals.php?hub_id=${hub_id}&type=${type}&value=${value}`;

  // Use fetch API to send the data to the API endpoint
  fetch(url)
    .then(response => response.json())  // Parse JSON response from the API
    .then(data => {
      console.log(`${type} data sent successfully:`, data);  // Log the response for debugging
    })
    .catch(error => {
      console.error(`Error sending ${type} data:`, error);  // Log any errors
    });
}


/*
function heart() {
  async function run() {
    while (true) {  // Keep fetching every 2 seconds
      let n = await eel.sensor_heart()();  // Fetch heart rate data

      // Display the result in the sensor data element
      let sval = "-- " + n + " --";

      console.log(sval);
      document.getElementById("sensordata").innerText = sval;

      // Wait 2 seconds before the next reading
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }
  run();
}
*/


function check() {
  async function run() {
    let n = await eel.check_I2C()();
    console.log("I2C devices found:", n);

    
    if (n.includes("0x5a")) {
      transitionToPage('module/s-temp.html');
    }
    if (n.includes("0x57")) {
      transitionToPage('module/MAX30102.html');
    }
  }
0x5a
  run();
}
