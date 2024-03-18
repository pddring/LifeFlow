import eel 
import multiprocessing
import pyautogui
import lflowalerts
import time
import json

#gpio

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
    def sensor_temp():
        import Sensor_Temperature as s1
        print("fetching temperature...")
        return(s1.take())
    
    @eel.expose
    def check_I2C():
        import Sensor_Temperature as s1
        print("I2C checking...")
        return(s1.check())

    @eel.expose
    def emergency():
        print('Sending emergency alerts...')
        lflowalerts.send(readData("first_name") + " " + readData("last_name"))

    @eel.expose
    def fullscreen():
        print('entering fullscreen...')
        time.sleep(0.5)
        pyautogui.hotkey("fn", "f11")

    @eel.expose
    def bingR():
        return 'No wallpaper found'
    #writeData("key_name", "new_value")
    #readData("key_name"")   

    eel.init("web")   
    print("yes")
    eel.start("load-redirect.html", port=8000)

def GPIO():

    def home():
        print("Home Button Pressed")

    def emergency():
        print("Emergency Button Pressed")
        pyautogui.hotkey("ctrl", "e" )

    def select():
        print("Select Button Pressed")

multi_UI = multiprocessing.Process(target=UI)
multi_GPIO = multiprocessing.Process(target=GPIO)

if __name__ == '__main__':
    multi_UI.start()
    multi_GPIO.start()   