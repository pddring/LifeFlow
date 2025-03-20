# <img src="https://github.com/pddring/LifeFlow/assets/152720783/899cfe60-e323-4a9e-888c-b15697a5152e" width="25%">

> PA Consulting Raspberry Pi competition entry 2025

- [About](#about)
- [Build Guide](#build-guide)
- [Business Models](#our-business-models)

## About

![image](https://github.com/user-attachments/assets/ee4331ec-a89a-46ab-bad1-bfc7be4c5275)


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
- [Pimoroni Badger 2040 W](https://shop.pimoroni.com/products/badger-2040-w?variant=40514062188627)
- [ADXL343 Triple-Axis Accelerometer](https://shop.pimoroni.com/products/adxl343-triple-axis-accelerometer-2g-4g-8g-16g-w-i2c-spi?variant=21768703541331)
- [4 Pin JST-SH Cable](https://shop.pimoroni.com/products/jst-sh-cable-qwiic-stemma-qt-compatible?variant=31910609813587)
- [400mAh Hard Case LiPo Battery](https://shop.pimoroni.com/products/galleon-400mah-battery?variant=40061068673107)

### LifeFlow Hub

- Firstly we formatted an SD card with Raspberry Pi OS then we inserted the SD card and connected the toushcreen via the GPIO pins. We added a [Nano Hat Hacker](https://shop.pimoroni.com/products/pico-hat-hacker?variant=44144542154) to gain access to the used GPIO.
- We installed the necessary [tools and drivers](https://www.elegoo.com/pages/download) for the [Touchscreen Display](https://www.amazon.co.uk/gp/product/B01MRQTMTD/ref=ppx_yo_dt_b_asin_title_o00_s01?ie=UTF8&psc=1 ) following the instructions [here](https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(A))
- We progammed the User Interface with python, html, css and javascript using the [eel library](https://pypi.org/project/Eel/). We then transferred this code to the Pi using GitHub.
- For our prototype, we have got the MAX30102 heart rate and pulse oximitery sensor and the MLX90614 non - contact thermometer working.
- In order to test the device you need to copy the files from the [github repository](https://github.com/pddring/LifeFlow/tree/main/life-flow-main) and run it using the command `python3 main.py`

The first time you run this it will require a number of python libraries. Most of them can be installed can be installed by running:
```
sudo apt update
sudo apt upgrade
sudo apt install pip3
pip3 install eel pyautogui gpiod Adafruit-Blinka adafruit-circuitpython-mlx90614 
```
- We created a module system with PCB prototyping board that uses i2c communication with connections as shown below:
>- 3v on the Pi (physical pin 1) 
>-  Gnd on the Pi (physical pin 9)
>- SCL (I2C clock) on the Pi (Physical pin 5 / GPIO3)
>- SDA (I2C data) on the Pi (Physical pin 3 / GPIO2)
>  
> ![image](https://github.com/user-attachments/assets/7179de0a-c2ab-45e6-b9af-1ae4eaf80668)
> *Inside Of Modules*
> ![image](https://github.com/user-attachments/assets/afaefeb4-c874-42e3-be61-dd63bf027883)
> *Module Connectors*
> ![image](https://github.com/user-attachments/assets/193b7c00-2c31-45ac-9183-d0d92bb0209c)
> *Temperature & Pulse Modules*
> ![image](https://github.com/user-attachments/assets/ddf92536-104c-411a-858d-af01b1b57140)
> *Module Port*
>
- The hub itself uses a raspberry pi 3B with a solar powered batery:
> ![image](https://github.com/user-attachments/assets/44cad795-a4d1-4f9c-8c0e-ad3d8403d086)
> *LifeFlow Hub Inside View From Top*
> ![WhatsApp Image 2025-03-20 at 17 22 28_27c43e98](https://github.com/user-attachments/assets/9d8a8776-d171-423d-88c2-f82cf74d3672)
> *LifeFlow Hub*

### LifeFlow Badge
![image](https://github.com/user-attachments/assets/446600ad-1a29-4e7b-9c07-0be93e1ce38e)
- The LifeFlow Badge uses a hard-cased LiPo battery for power.
- It Also uses an accelerometer to accurately detect falls.
- The connections are as shown below:
![image](https://github.com/user-attachments/assets/1d75186b-1f63-479f-ae1e-48a069e03bb9)
- The device uses the following modules to operate:
```
import gc
import os
import time
import math
import machine
import struct
import badger2040
import badger_os
import pngdec
import jpegdec
import _thread
```
- The LifeFlow Badge needs an internet connection to send alerts to staff when a fall is detected. This needs to be set up in "WIFI_CONFIG.py"
```
SSID = "****"
PSK = "****"
COUNTRY = "GB"
BADGE_ID = "1"
```

### LifeFlow Staff Portal
The LifeFlow Staff Portal is a local web app that runs on an apache web server and uses a MariaDB or MySQL database. It is made with PHP, SQL, HTML, CSS and JS.
- To start using the lifeflow staff portal, you'll need to install it on a raspberry pi or other linux server/device.
- First, you'll need to install the following packages:
```
sudo apt update
sudo apt upgrade
sudo apt install apache2
sudo apt install mysql-server
sudo service mysql status
```
- Then, locate the hmtl folder on your device and get the web files from this repository.
- Also, you might want to install phpmyadmin to structure the database:
```
sudo apt install phpmyadmin
```
- Then you'll need to use phpmyadmin to create the following tables and databses:
![image](https://github.com/user-attachments/assets/c3b7d9dc-2e9e-4a34-99b3-ef2a6b2a2ce3)
- You can now visit the staff portal on your local network by visiting ```lifeflow.local``` in a web browser

### 3D Printing & CAD Design

![Untitled design (2)](https://github.com/user-attachments/assets/d9a63e25-e401-4fa5-b307-2c7a30d61767)

During prototyping we designed our cases using Sketchup. We designed our initial prototype cases to have as thin walls as possible to reduce the amount of plastic and limit the environmental impact of the development cycle but our final design would have a thicker case in order to be more durable.

Our deisign for the LifeFlow Hub Can be viewed [here](https://app.sketchup.com/share/tc/europe/aqrCFikvXgk?stoken=UQp0qggRx61hj7zEzaFMxSISR0IkfI2zEOqYd4P-_p8H29i8FynMl5u-Kpgof-Cb&source=web)



## Our Business Models

Our original marketing plan aimed the LifeFlow hub at individuals to reduce strain on the NHS. Since the addition of the LifeFlow Badge and Staff Portal, our new business model aims the LifeFLow System at retirement accomidation and care homes due to its ability to provide staff with advanced insights into residents health.
