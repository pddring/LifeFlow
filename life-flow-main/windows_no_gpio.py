import eel 
import multiprocessing
import pyautogui
import lflowalerts
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
        return str(data[key])

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
    def emergency():
        print('Sending emergency alerts...')
        #lflowalerts.send(readData("first_name") + " " + readData("last_name"))

        # Send Request to Incidents API
        # Load the JSON file to retrieve the ID
        with open('settings.json', 'r') as file:
            data = json.load(file)

        # Retrieve the 'hub' value from the JSON
        hub_id = data['hub']  # Assuming 'hub' contains the hub ID value

        # Construct the URL with the retrieved hub_id
        url = f"http://lifeflow.local/api/hub_alert.php?hub_id={hub_id}"

        # Send a GET request to the constructed URL
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
        print("Failed to enter fullscreen. Run 'main.py' to enable fullscreen. This script doesn't use fullscreen as it is for development only.")

    @eel.expose
    def bingR():
        return 'No wallpaper found'
    #writeData("key_name", "new_value")
    #readData("key_name"")   

    eel.init("web")   
    print("yes")
    eel.start("load-redirect.html" , size=[320,480])

# Define the function to update the settings.json file
def update_settings(file_path, updated_data):
    try:
        # Open the settings.json file for reading
        with open(file_path, 'r') as file:
            settings = json.load(file)
        
        # Update the settings with the data provided
        settings.update(updated_data)
        
        # Write the updated settings back to the file
        with open(file_path, 'w') as file:
            json.dump(settings, file, indent=4)
        
        print("Settings updated successfully.")
    
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except json.JSONDecodeError:
        print("Error decoding the JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to fetch data from the API and update the settings
def fetch_and_update_settings(file_path):
    try:
        # Open the settings.json file and read the hub ID
        with open(file_path, 'r') as file:
            settings = json.load(file)
        
        # Retrieve the hub ID from the settings file
        hub_id = settings.get("hub", None)
        
        if hub_id is None:
            print("Error: No 'hub' field found in the settings file.")
            return
        
        # API URL to fetch hub information
        api_url = f"http://lifeflow.local/api/hub_info.php?id={hub_id}"
        
        # Fetch the data from the API
        response = requests.get(api_url)
        
        if response.status_code == 200:
            # Parse the response JSON data
            hub_data = response.json()

            # Check if the expected data exists in the response
            if "first_name" in hub_data and "last_name" in hub_data and "age" in hub_data and "gender" in hub_data:
                updated_data = {
                    "first_name": hub_data["first_name"],
                    "last_name": hub_data["last_name"],
                    "age": hub_data["age"],
                    "gender": hub_data["gender"]
                }
                
                # Update settings.json with the fetched data
                update_settings(file_path, updated_data)
            else:
                print("Error: Missing data in API response.")
        else:
            print(f"Error: Failed to fetch data from API. Status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while requesting the API: {e}")
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except json.JSONDecodeError:
        print("Error decoding the JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example of how to use the function
file_path = 'settings.json'

# Fetch data from the API and update the settings based on the hub_id in settings.json
fetch_and_update_settings(file_path)

UI()