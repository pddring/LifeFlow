import eel 
import multiprocessing
import pyautogui
import lflowalerts
import time
import json


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
        lflowalerts.send(readData("first_name") + " " + readData("last_name"))

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

UI()