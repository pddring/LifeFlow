from smbus2 import SMBus
from mlx90614 import MLX90614

def take():
    try:
        # Open I2C bus 0 (You can also use bus 1 if needed)
        bus = SMBus(0)

        # Initialize the MLX90614 sensor at address 0x5A
        sensor = MLX90614(bus, address=0x5A)

        # Get ambient temperature
        ambient_temp = sensor.get_amb_temp()
        print(f"Ambient Temperature: {ambient_temp:.2f} °C")

        # Get object temperature and return as a string
        object_temp = sensor.get_obj_temp()
        object_temp_str = f"{object_temp:.2f} °C"
        print(f"Object Temperature: {object_temp_str}")

        # Close the I2C bus when done
        bus.close()

        # Return object temperature as string
        return object_temp_str

    except Exception as e:
        print(f"Error: {e}")
        return None