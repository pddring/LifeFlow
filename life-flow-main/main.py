import eel
import json
import requests
import subprocess
import time
import pyautogui
import multiprocessing

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

# Eel UI setup
def UI():
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
        import Sensor_Temperature as s1
        print("Fetching temperature...")
        return s1.take()

    @eel.expose
    def sensor_heart():
        import Sensor_Heart as s2
        print("Fetching pulse...")
        return s2.take()

    @eel.expose
    def check_I2C():
        import Sensor_Temperature as s1
        print("I2C checking...")
        return s1.check()

    @eel.expose
    def git_pull():
        try:
            result = subprocess.run(["git", "pull"], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return str(e)

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
    def ping_server():
        # Dummy function to ensure server is active
        print("Ping received - server is alive")
        return "Server is up and running!"

    # Perform server sync before starting UI
    fetch_and_update_settings("settings.json")

    # Initialize and start Eel
    eel.init("web")
    print("Waiting for Eel server to be fully ready...")
    time.sleep(2)  # Give the server a little time to initialize before starting the UI
    try:
        eel.start("load-redirect.html", port=8000, cmdline_args=['--disable-http-cache'], block=True)
        print("Eel server started and running...")
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
    # Start GPIO process
    gpio_process = multiprocessing.Process(target=GPIO)
    gpio_process.start()

    # Start the UI
    UI()
