//Settings To JSON

function save(key, page) {
  eel.writeData(key, document.querySelector(".use-keyboard-input").value);
  transitionToPage(page);
}
function skip(page) {
  transitionToPage(page);
}