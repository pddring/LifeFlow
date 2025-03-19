//Settings To JSON

update();

function update() {
  async function run() {
    let n = await eel.readData("language")();
    document.getElementById("language").value = n;
    console.log(n);
  }
  run();

}

function save() {
  eel.writeData("language", document.getElementById("language").value);
  transitionToPage('setup/1.html');
}

function complete() {
  eel.writeData("completed_setup", "true");
}