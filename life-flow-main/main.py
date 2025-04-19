import eel
import json
import requests
import subprocess
import time
import pyautogui
import multiprocessing
import sys
import socket

# Function to update settings in the JSON file
def update_settings(file_path, updated_data):
    try:
        with open(file_path, 'r') as file:
            settings = json.load(file)
        settings.update(updated_data)
        with open(file_path, 'w') as file:
            json.dump(settings, file, indent=4)
        print("Settings updated successfully.")
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except json.JSONDecodeError:
        print("Error decoding the JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to fetch and update settings from an API
def fetch_and_update_settings(file_path):
    try:
        with open(file_path, 'r') as file:
            settings = json.load(file)
        hub_id = settings.get("hub", None)
        if hub_id is None:
            print("Error: No 'hub' field found in the settings file.")
            return
        api_url = f"http://localhost/api/hub_info.php?id={hub_id}"
        response = requests.get(api_url)
        if response.status_code == 200:
            hub_data = response.json()
            if all(key in hub_data for key in ["first_name", "last_name", "age", "gender", "room"]):
                updated_data = {
                    "first_name": hub_data["first_name"],
                    "last_name": hub_data["last_name"],
                    "age": hub_data["age"],
                    "gender": hub_data["gender"],
                    "room": hub_data["room"]
                }
                update_settings(file_path, updated_data)
            else:
                print("Error: Missing data in API response.")
        else:
            print(f"Error: Failed to fetch data from API. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Get a free port from the OS
def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

# Eel UI setup
def UI():
    # Try importing sensors safely
    try:
        import Sensor_Temperature as s1
    except Exception as e:
        print(f"Failed to import Sensor_Temperature: {e}")
        s1 = None

    try:
        import Sensor_Heart as s2
    except Exception as e:
        print(f"Failed to import Sensor_Heart: {e}")
        s2 = None

    @eel.expose
    def readData(key):
        print("Reading from json...")
        with open("settings.json", "r") as jsonFile:
            data = json.load(jsonFile)
        return str(data.get(key, ""))

    @eel.expose
    def writeData(key, value):
        print("Writing to json...")
        with open("settings.json", "r") as jsonFile:
            data = json.load(jsonFile)
        data[key] = value
        with open("settings.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)
        print("JSON write complete")

    @eel.expose
    def sensor_temp():
        print("Fetching temperature...")
        if s1:
            return s1.take()
        return "Temperature sensor unavailable"

    @eel.expose
    def sensor_heart():
        print("Fetching pulse...")
        if s2:
            return s2.take()
        return "Heart rate sensor unavailable"

    @eel.expose
    def check_I2C():
        print("Checking I2C bus...")
        if s1:
            return s1.check()
        return "Temperature sensor unavailable"

    @eel.expose
    def git_pull():
        try:
            print("Performing git pull...")
            result = subprocess.run(["git", "pull"], capture_output=True, text=True)
            print(result.stdout)
            eel.quit()
        except Exception as e:
            print(f"Error during git pull: {e}")

    @eel.expose
    def emergency():
        print('Sending emergency alerts...')
        try:
            with open('settings.json', 'r') as file:
                data = json.load(file)
            hub_id = data.get('hub', '')
            url = f"http://localhost/api/hub_alert.php?hub_id={hub_id}"
            response = requests.get(url)
            if response.status_code == 200:
                print("Request successful")
            else:
                print(f"Request failed with status: {response.status_code}")
        except Exception as e:
            print(f"Error with the request: {e}")

    @eel.expose
    def fullscreen():
        print('Entering fullscreen...')
        time.sleep(0.5)
        pyautogui.hotkey("fn", "f11")

    @eel.expose
    def ping_server():
        print("Ping received - server is alive")
        return "Server is up and running!"

    # Sync with API before launching UI
    fetch_and_update_settings("settings.json")

    # Start Eel server with an automatically free port
    eel.init("web")
    port = get_free_port()
    print(f"Starting Eel on port {port}...")
    time.sleep(2)

    try:
        eel.start("load-redirect.html", port=port, cmdline_args=['--disable-http-cache'], mode=None)

    except Exception as e:
        print(f"Error starting Eel: {e}")

# GPIO Setup for emergency and home buttons
def GPIO():
    def home():
        print("Home Button Pressed")
    def emergency():
        print("Emergency Button Pressed")
        pyautogui.hotkey("ctrl", "e")
    def select():
        print("Select Button Pressed")
    while True:
        time.sleep(1)

if __name__ == '__main__':
    multiprocessing.set_start_method('fork')  # Safe for Pi/Linux

    # Start GPIO process
    gpio_process = multiprocessing.Process(target=GPIO)
    gpio_process.start()

    # Start the UI
    UI()
