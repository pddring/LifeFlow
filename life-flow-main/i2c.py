from smbus2 import SMBus

bus = SMBus(0)  # Use I2C bus 0 (/dev/i2c-0)
addresses = []
for addr in range(0x03, 0x77):
    try:
        bus.write_quick(addr)
        addresses.append(hex(addr))
    except:
        continue
bus.close()
print("ADDRESSES:", addresses)  # Print the list of found addresses