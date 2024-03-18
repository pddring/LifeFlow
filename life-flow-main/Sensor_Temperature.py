import board
import busio as io
import adafruit_mlx90614 

from time import sleep

def check():
    i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
    adress = [hex(x) for x in i2c.scan()]
    return(adress)

def take():
    i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
    mlx = adafruit_mlx90614.MLX90614(i2c)

    ambientTemp = "{:.2f}".format(mlx.ambient_temperature)
    targetTemp = "{:.2f}".format(mlx.object_temperature)

    sleep(1)

    print("Ambient Temperature:", ambientTemp, "C")
    print("Target Temperature", targetTemp, "C")
    
    return(targetTemp)