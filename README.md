# <img src="https://github.com/pddring/LifeFlow/assets/152720783/899cfe60-e323-4a9e-888c-b15697a5152e" width="25%">

> PA Consulting Raspberry Pi competition entry 2023-2025

- [About](#about)
- [Build Guide](#build-guide)
- [Business Models](#our-business-models)

## About
![image]()


LifeFlow is an integrated health care management system designed to give detailed insights to carers and to give residence the most high-quality care possible. LifeFlow is made with HTML, PHP, CSS, JS & Python. In total the whole system contains around 10,000 lines of code. 

The LifeFlow system is comprised of three parts: The Hub, Staff Portal, and the ID Badges. The hub uses a Raspberry Pi to log sensor readings which can be used to inform treatment plans and monitor the health of patients. It has medication reminders which prompt users to take their medication at the right time. This allows the elderly to be more independent, reducing their reliance on others such as carers and family members. The hub can monitor vitals by using modular sensors that attach to the main device. These modules currently include heart rate, blood oxygen and body temperature. The device has a simple user interface and accessibility features making it easy to use.  Our working prototype is enclosed in a custom-designed 3D-printed case giving it a stylish and easy to use appearance. 

The Badges can be worn by the residents so that they can be easily identified. They are also fitted with an accelerometer which can detect sudden movement e.g. if the user falls. An alert is then sent to the staff via the staff portal allowing help to reach the resident. In the future we would like to add GPS location tracking to the lanyards allowing an even easier and more advanced experience. Both the badge and the hub have an emergency button. 

Finally, the Staff Portal is a web app that allows care homes to get advanced insights into their residents. It also notifies carers when a fall is detected, or an emergency button is pressed. The staff portal links the badges and hubs to one location with an easy-to-use user interface for staff. The staff portal shows a resident’s sensor logs, age, and other information allowing carers and family members to get an idea of how a resident or loved one is doing. 

## Build Guide
### Parts
- [Raspberry Pi 3 Model B](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/)
- [Elegoo Raspberry Pi Touchscreen Display](https://www.amazon.co.uk/gp/product/B01MRQTMTD/ref=ppx_yo_dt_b_asin_title_o00_s01?ie=UTF8&psc=1 )
- [MAX30102 Heart Rate and Pulse Oximetry Sensor](https://www.amazon.co.uk/dp/B09M87934Q?psc=1&smid=AY8YTBRZSL2Q4&ref_=chk_typ_imgToDp)
- [MLX90614 Non Contact Thermometer](https://www.amazon.co.uk/dp/B07YKNQQ7P?psc=1&smid=A1A7E5ILEFA1R3&ref_=chk_typ_imgToDp)

### Build

- Firstly we formatted an SD card with Raspberry Pi OS then we inserted the SD card and connected the toushcreen via the GPIO pins. We added a [Nano Hat Hacker](https://shop.pimoroni.com/products/pico-hat-hacker?variant=44144542154) to gain access to the used GPIO.
- We installed the necessary [tools and drivers](https://www.elegoo.com/pages/download) for the [Touchscreen Display](https://www.amazon.co.uk/gp/product/B01MRQTMTD/ref=ppx_yo_dt_b_asin_title_o00_s01?ie=UTF8&psc=1 ) following the instructions [here](https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(A))
- We progammed the User Interface with python, html, css and javascript using the [eel library](https://pypi.org/project/Eel/). We then transferred this code to the Pi using GitHub.
- We soldered some wires onto the emergency button and then connected it to the GPIO pins as shown below
- ![image](https://github.com/pddring/LifeFlow/assets/760604/e4cf8fa8-178e-49b6-8a24-e1caf0372b75)
- For our prototype we have got the infrared temperature working so far:
- Connect each pin as shown below:
 >-  Vin on the temperature sensor to 3v on the Pi (physical pin 1) 
 >- Gnd on the temperature sensor to Gnd on the Pi (physical pin 9)
 >- SCL (I2C clock) on the temperature sensor to SCL on the Pi (Physical pin 5 / GPIO3)
 >- SDA (I2C data) on the temperature sensor to SDA on the Pi (Physical pin 3 / GPIO2)

Our next iteration involved using some PCB prototyping board rather than a bread board as shown below:
Inside:
![image](https://github.com/pddring/LifeFlow/assets/760604/9b8d493d-6cd4-455f-b5e2-27a0d5aae650)
With 3d printed casing:
![image](https://github.com/pddring/LifeFlow/assets/760604/9667c055-2894-4e57-a513-08f49787380c)

During prototyping we designed our cases using Sketchup. We designed our initial prototype cases to have as thin walls as possible to reduce the amount of plastic and limit the environmental impact of the development cycle but our final design would have a thicker case in order to be more durable.

In order to test the device you need to copy the files from the [github repository](https://github.com/pddring/LifeFlow/tree/main/life-flow-main) and run it using the command `python3 main.py`

The first time you run this it will require a number of python libraries which can be installed by running:
```
sudo apt update
sudo apt upgrade
sudo apt install pip3
pip3 install eel pyautogui pyautogui pyautogui pyautogui pyautogui gpiod Adafruit-Blinka adafruit-circuitpython-mlx90614 
```

To power the device we are using a solar powered USB battery pack:
![image](https://github.com/pddring/LifeFlow/assets/760604/c1827d16-28cf-4134-bfef-46110e08a708)


## Our Business Models
The cost of medical technology can sometimes be prohibitive but our business plan maps out how LifeFlow can not only improve the health, independence and quality of life for patients but also reduce private health insurance premiums, save money for care homes and reduce the strain on NHS primary healthcare.
<img src="https://raw.githubusercontent.com/megacooki/LifeFlow/main/Readme%20Files/Business%20model.png" width="25%">
