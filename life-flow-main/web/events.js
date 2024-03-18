function KeyPress(e) {
      var evtobj = window.event? event : e
      if (evtobj.keyCode == 69 && evtobj.ctrlKey) {
      window.location.href = "../../../../../emergency/index.html";
        }
}

document.onkeydown = KeyPress;