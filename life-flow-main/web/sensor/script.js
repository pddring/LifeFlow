function temperature() {
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
    if (n="0x5A") {
      transitionToPage('module/s-temp.html');
    }
  }

  run();
}

setTimeout(()=> {
  setInterval(check(), 3000);
}, 3000);
