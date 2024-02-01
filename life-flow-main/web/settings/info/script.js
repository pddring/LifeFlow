//Settings To JSON

update();

function update() {
var update_id = ["first_name", "last_name", "age"]

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