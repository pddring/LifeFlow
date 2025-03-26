import eel
import multiprocessing
import pyautogui
import time
import json
import requests

def UI():
    @eel.expose
    def readData(key):
        print("reading from json...")
        with open("settings.json", "r") as jsonFile:
            data = json.load(jsonFile)
        print("JSON read complete")
        return str(data.get(key, ""))

    @eel.expose
    def writeData(key, value):
        print("writing to json...")
        with open("settings.json", "r") as jsonFile:
            data = json.load(jsonFile)
        data[key] = value
        with open("settings.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)
        print("JSON write complete")

    @eel.expose
    def sensor_temp():
        import Sensor_Temperature as s1
        print("fetching temperature...")
        return s1.take()

    @eel.expose
    def sensor_heart():
        import Sensor_Heart as s2
        print("fetching pulse...")
        return s2.take()

    @eel.expose
    def check_I2C():
        import Sensor_Temperature as s1
        print("I2C checking...")
        return s1.check()

    @eel.expose
    def emergency():
        print('Sending emergency alerts...')

        with open('settings.json', 'r') as file:
            data = json.load(file)
        hub_id = data.get('hub', '')

        url = f"http://localhost/api/hub_alert.php?hub_id={hub_id}"

        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                print("Request successful")
            else:
                print(f"Request failed with status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error with the request: {e}")

    @eel.expose
    def fullscreen():
        print('Entering fullscreen...')
        time.sleep(0.5)
        pyautogui.hotkey("fn", "f11")

    @eel.expose
    def bingR():
        return 'No wallpaper found'

    # Initialize Eel
    eel.init("web")
    print("Starting Eel...")
    eel.start("load-redirect.html", port=8000, cmdline_args=['--disable-http-cache'], block=True)


def GPIO():
    def home():
        print("Home Button Pressed")

    def emergency():
        print("Emergency Button Pressed")
        pyautogui.hotkey("ctrl", "e")

    def select():
        print("Select Button Pressed")

    while True:
        time.sleep(1)  # Simulate GPIO loop

if __name__ == '__main__':
    # Run Eel in the main process
    ui_process = multiprocessing.Process(target=GPIO)
    ui_process.start()

    # Run Eel in the main thread
    UI()
