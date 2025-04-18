//Settings To JSON


function update() {
var update_id = ["emergency_e_1", "emergency_e_2", "emergency_e_3"]

update_id.forEach((id) => {

  async function run() {
    let n = await eel.readData(id)();
    document.getElementById(id).value = n;
    console.log(n);
  }

  run();
});
}

function save(key) {
  eel.writeData(key, document.getElementById(key).value);
  transitionToPage('index.html');
}
