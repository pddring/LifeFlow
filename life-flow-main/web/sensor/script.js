function temperature() {
  async function run() {
    let n = await eel.sensor_temp()();
    
    let sval = "-- " + n.substring(0, n.length - 1) + " --";
    
    console.log(sval);
    document.getElementById("sensordata").innerText = sval;
    }
   run();
}

function heart() {
  async function run() {
    let n = await eel.sensor_temp()();
    
    let sval = "-- " + n.substring(0, n.length - 1) + " --";
    
    console.log(sval);
    document.getElementById("sensordata").innerText = sval;
    }
   run();
}

function check() {
  async function run() {
    let n = await eel.check_I2C()();
    console.log(n);

    if (n === "0x5A") {
      transitionToPage('module/s-temp.html');
    } else if (n === "0x57") {
      transitionToPage('module/s-heart.html');
    }
  }

  run();
}
