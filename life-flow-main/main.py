import eel 
import multiprocessing
import pyautogui
import lflowalerts
import gpiod
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
    eel.start("load-redirect.html")

def GPIO():

        # Define GPIO pin numbers for the buttons
    button_pins = [17, 27, 22]  # You can change these to the desired GPIO pins for the buttons

    # Define messages for each button
    button_functions = {
        17: "home()",
        27: "emergency()",
        22: "select()"
    }

    # Create a GPIO chip and lines for the buttons
    chip = gpiod.Chip('gpiochip4')
    button_lines = {pin: chip.get_line(pin) for pin in button_pins}

    def home():
        print("Home Button Pressed")

    def emergency():
        print("Emergency Button Pressed")
        pyautogui.hotkey("ctrl", "e" )

    def select():
        print("Select Button Pressed")

    # Request the lines for input
    for line in button_lines.values():
        line.request(consumer='button', type=gpiod.LINE_REQ_EV_BOTH_EDGES)

    while True:
        for pin, line in button_lines.items():
            value = line.get_value()
            if value == 1:
                exec(button_functions[pin])
                time.sleep(0.3)

multi_UI = multiprocessing.Process(target=UI)
multi_GPIO = multiprocessing.Process(target=GPIO)

if __name__ == '__main__':
    multi_UI.start()
    multi_GPIO.start()