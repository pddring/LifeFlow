import time
from heartrate_monitor import HeartRateMonitor

# Create an instance of the heart rate monitor
monitor = HeartRateMonitor(print_raw=True, print_result=True)

# Start the sensor in a background thread
monitor.start_sensor()

# Wait for the sensor to collect data for a specified time
print("Collecting data...")
time.sleep(10)  # Wait for 10 seconds to collect data

# Fetch the latest heart rate and SpO2 data
data = monitor.get_data()

# Print the results
print(f"SpO2: {data['spo2']}")

# Stop the sensor when done
monitor.stop_sensor()
