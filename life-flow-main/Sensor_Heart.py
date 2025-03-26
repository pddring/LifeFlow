import max30102
import time

def take(raw=False):
    """Take one valid reading from the MAX30102 sensor."""
    hrm = max30102(print_raw=raw, print_result=(not raw))
    hrm.start_sensor()
    
    print("Waiting for a valid reading...")
    
    try:
        while True:
            reading = hrm.get_data()
            
            # Check if the reading is valid (based on the sensor's logic)
            if reading and reading['heart_rate'] > 0:  # Adjust condition based on valid data
                hrm.stop_sensor()
                return reading
            
            time.sleep(0.5)  # Wait briefly before checking again
    
    except KeyboardInterrupt:
        print("Interrupted. Stopping sensor.")
        hrm.stop_sensor()
        return None

# Example usage:
if __name__ == "__main__":
    result = take(raw=False)
    if result:
        print("Valid Reading:", result)
    else:
        print("No valid reading detected.")
