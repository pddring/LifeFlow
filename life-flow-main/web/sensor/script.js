function temperature() {
  async function run() {
    let n = await eel.sensor_temp()();
    
    let sval = "-- " + n.substring(0, n.length - 1) + " --";
    
    console.log(sval);
    document.getElementById("sensordata").innerText = sval;
    }
   run();
}