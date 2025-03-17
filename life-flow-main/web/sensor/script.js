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

setTimeout(() => {
  const randomNumber = Math.floor(Math.random() * 3) + 1;
  let redirectUrl = '';

  switch (randomNumber) {
      case 1:
          redirectUrl = 'module/s-heart.html';
          break;
      case 2:
          redirectUrl = 'module/s-oxygen.html';
          break;
      case 3:
          redirectUrl = 'module/s-temp.html';
          break;
  }

  window.location.href = redirectUrl;
}, 5000);



// the triger for check function is on the index.html file on the waiting page

