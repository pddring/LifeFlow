function loadReminders() {
    var update_id = ["reminder_slot_1", "reminder_slot_2"]
    
    update_id.forEach((id) => {
    
      async function run() {
        let n = await eel.readData(id)();
        if (n != "") {
            document.getElementById(id).innerHTML = n;
        }
      }
    
      run();
    });
    }

function del(key) {
  eel.writeData(key, "");
  eel.writeData(key + "_time", "");
  window.location.href = window.location.href;
}