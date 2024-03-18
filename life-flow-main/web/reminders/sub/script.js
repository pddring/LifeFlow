function addReminder() {
    var title = document.getElementById('title').value;
    var time = document.getElementById('time').value;
    var key = document.getElementById('key').value;

    var txt = "<div><strong>" + title + "</strong><br>Alert - " + time + "</div><button id='deleteb' onclick='del(" + "\"" + key + "\"" + ")'>Delete</button>";

    localStorage.setItem("alert1_shown", "")
    localStorage.setItem("alert2_shown", "")

    eel.writeData(key, txt.toString());
    eel.writeData(key + "_time", time + " - " + title);

    transitionToPage("/reminders/index.html");
}
