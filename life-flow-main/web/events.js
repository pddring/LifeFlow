function KeyPress(e) {
      var evtobj = window.event? event : e
      if (evtobj.keyCode == 69 && evtobj.ctrlKey) {
      window.location.href = "../../../../../emergency/index.html";
        }
}

document.onkeydown = KeyPress;

window.addEventListener("DOMContentLoaded", () => {
  // Select all elements that have a data-json attribute
  const elements = document.querySelectorAll("[data-json]");

  elements.forEach(el => {
      const key = el.getAttribute("data-json");

      if (key) {
          eel.readData(key)((value) => {
              if (value && value.trim() !== "") {
                  //el.innerText = value + " ✅";
                  el.innerText = value;
              } else {
                  el.innerText = "❌";
              }
          });
      }
  });
});
