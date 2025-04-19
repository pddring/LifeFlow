import machine
import struct
import time
import math
import badger2040
import badger_os

# Initialize I2C
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
ADXL343_ADDR = 0x53

# Initialize ADXL343
i2c.writeto(ADXL343_ADDR, bytearray([0x2D, 0x08]))  # Power on
i2c.writeto(ADXL343_ADDR, bytearray([0x31, 0x00]))  # Set ±2g mode

# Threshold
FREE_FALL_THRESHOLD = 0.4  # g (Below this = free fall)

def get_acceleration():
    """Reads X, Y, Z acceleration and calculates total acceleration."""
    raw_data = i2c.readfrom_mem(ADXL343_ADDR, 0x32, 6)
    x, y, z = struct.unpack('<hhh', raw_data)

    # Convert to g-force
    x_g = x / 256.0
    y_g = y / 256.0
    z_g = z / 256.0

    # Calculate total acceleration magnitude
    total_acc = math.sqrt(x_g**2 + y_g**2 + z_g**2)
    
    return x_g, y_g, z_g, total_acc

def detect_fall():
    """Monitors acceleration and triggers emergency app on free fall."""
    while True:
        x, y, z, total_acc = get_acceleration()
        print(f"📊 Accel -> X: {x:.2f}g, Y: {y:.2f}g, Z: {z:.2f}g, Total: {total_acc:.2f}g")

        # Trigger emergency mode immediately on free fall detection
        if total_acc < FREE_FALL_THRESHOLD:
            print("🚨 Free Fall Detected! Switching to emergency app.")
            #badger_os.load("emergency")
            break  # Exit loop after triggering emergency mode

        time.sleep(0.1)  # Polling delay

# Start fall detection
detect_fall()
