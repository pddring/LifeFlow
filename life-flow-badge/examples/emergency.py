import badger2040
import badger_os  # ✅ Import badger_os for proper app exit
from badger2040 import WIDTH
import urequests
import WIFI_CONFIG
import time

print("Emergency app is open")

ID = WIFI_CONFIG.BADGE_ID  # Determines time zone from lat/long

URL = "http://lifeflow.local/api/fall_detected.php?badge_id=" + str(ID)

# Display Setup
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(2)


def draw_page(body_text):
    display.set_pen(15)
    display.clear()
    display.set_pen(0)

    # Draw header
    display.set_font("bitmap6")
    display.set_pen(0)
    display.rectangle(0, 0, WIDTH, 20)
    display.set_pen(15)
    display.text("LifeFlow Emergency System", 3, 4)
    display.set_pen(0)

    # Draw body text
    display.set_font("bitmap8")
    display.text(body_text, 3, 28, WIDTH, 3)

    display.update()


def send_request():
    try:
        print(f"Requesting URL: {URL}")
        r = urequests.get(URL)
        j = r.json()
        r.close()
        return j.get('status') == 'success'
    except Exception as e:
        print(f"Error: {e}")
        return False  # Handle network errors


def connect_to_network():
    display.update()
    display.connect()


def check_for_button_press():
    """Checks if any button is pressed and returns to the launcher."""
    while True:
        display.keepalive()  # Keeps the display active

        if display.pressed_any():  # Detects any button press
            print("Button pressed! Exiting to launcher.")
            badger_os.launch("launcher")  # Launch the main launcher
            return  # Exit the loop and script to prevent further execution

        time.sleep(0.1)  # Avoid excessive CPU usage


def main():
    connect_to_network()
    draw_page("LifeFlow emergency system is sending assistance...")
    time.sleep(2)

    success = send_request()

    if success:
        draw_page("LifeFlow has been notified that you need assistance.")
    else:
        draw_page("Failed to notify LifeFlow.\nPlease reload to try again.")
        time.sleep(2)

    print("🚨 Emergency app is open and running.")

    # Start button listener
    check_for_button_press()


# ✅ Run the app
main()
