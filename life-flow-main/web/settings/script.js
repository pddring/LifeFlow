//Settings To JSON
function update() {
var update_id = ["narrator", "high_contrast"]

update_id.forEach((id) => {

  async function run() {
    let n = await eel.readData(id)();
    let current = document.getElementById(id).value;
    document.getElementById(id).value = current.replace("LOADING", n);
    
  }

  run();
});
}

function save(key) {
  if (document.getElementById(key).value.includes("ON")) {
    eel.writeData(key, "OFF");
    let current = document.getElementById(key).value;
    document.getElementById(key).value = current.replace("ON", "OFF");
    return
  } else {
    eel.writeData(key, "ON");
    let current = document.getElementById(key).value;
    document.getElementById(key).value = current.replace("OFF", "ON");
    return
  }
}

// loading

setTimeout(function() {
  document.getElementById("loading").remove();
}, 1000);