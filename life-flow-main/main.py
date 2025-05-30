import eel
import json
import requests
import subprocess
import time
from smbus2 import SMBus
import multiprocessing
import sys
import gevent
from heartrate_monitor import HeartRateMonitor

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
                    "room": hub_data["room"],
                    "emergency_contact_1": hub_data["emergency_contact_1"],
                    "emergency_contact_2": hub_data["emergency_contact_2"],
                    "emergency_contact_3": hub_data["emergency_contact_3"]
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
        print("Collecting pulse for 10 seconds...", flush=True)
        monitor = HeartRateMonitor(print_raw=True, print_result=True)
        monitor.start_sensor()

        try:
            time.sleep(10)

            data = monitor.get_data()
            if data and data['heart_rate'] > 0:
                heart_rate = data['heart_rate']
                print(f"Heart Rate: {heart_rate} BPM, SpO2: {data['spo2']}", flush=True)
                return str(heart_rate)
            else:
                print("No valid heart rate detected.", flush=True)
                return None
        except KeyboardInterrupt:
            print("Interrupted.", flush=True)
            return None
        finally:
            monitor.stop_sensor()


    @eel.expose
    def sensor_spo2():
        print("Collecting SpO₂ for 10 seconds...", flush=True)
        monitor = HeartRateMonitor(print_raw=True, print_result=True)
        monitor.start_sensor()

        try:
            time.sleep(10)

            data = monitor.get_data()
            if data and data['spo2'] > 0:
                spo2 = data['spo2']
                print(f"SpO₂: {spo2}%", flush=True)
                return str(spo2)
            else:
                print("No valid SpO₂ detected.", flush=True)
                return None
        except KeyboardInterrupt:
            print("Interrupted.", flush=True)
            return None
        finally:
            monitor.stop_sensor()



    @eel.expose
    def check_I2C():
        bus = SMBus(0)  # Use I2C bus 0 (/dev/i2c-0)
        addresses = []
        for addr in range(0x03, 0x77):
            try:
                bus.write_quick(addr)
                addresses.append(hex(addr))
            except:
                continue
        bus.close()
        print("ADDRESSES:", addresses)  # Using the comma will automatically format the list as a string
        return addresses

    @eel.expose
    def git_pull():
        try:
            print("Performing git pull...")
            result = subprocess.run(["git", "pull"], capture_output=True, text=True)
            print(result.stdout)  # Print the output of the git pull command
            eel.quit()  # Close the app gracefully after the pull
        except Exception as e:
            print(f"Error during git pull: {e}")

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
        #=======++++++============================++++++++++++++++++++++================= MAYBE IT ISNT BEING REFERENCED IN THE CODE BECAUSE IT STARTS ON IDEX.HTML NOW NOT LOAD REDIRECT

    # Perform server sync before starting UI
    fetch_and_update_settings("settings.json")

    # Initialize and start Eel
    eel.init("web")
    print("Waiting for Eel server to be fully ready...")
    time.sleep(3)  # Give the server a little time to initialize before starting the UI
    try:
        eel.start("home/index.html", port=8123, cmdline_args=['--disable-http-cache'], block=False)
        print("Eel server started and running...")
    except Exception as e:
        print(f"Error starting Eel: {e}")

    # Run the gevent event loop to prevent the script from exiting
    gevent.get_hub().join()

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
