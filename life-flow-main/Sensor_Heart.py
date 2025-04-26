import time
import sys
import gevent
from heartrate_monitor import HeartRateMonitor

def sensor_heart():
        print("Collecting pulse for 10 seconds...")

        monitor = HeartRateMonitor(print_raw=True, print_result=True)
        monitor.start_sensor()

        try:
            time.sleep(10)  # Wait to collect data

            data = monitor.get_data()

            if data and data['heart_rate'] > 0:
                heart_rate = data['heart_rate']
                print(f"Heart Rate: {heart_rate} BPM, SpO2: {data['spo2']}")
                return str(heart_rate)
            else:
                print("No valid heart rate detected.")
                return None
        except KeyboardInterrupt:
            print("Interrupted.")
            return None
        finally:
            monitor.stop_sensor()

sensor_heart()