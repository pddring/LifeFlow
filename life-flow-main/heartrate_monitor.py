import threading
import time
import numpy as np
from max30102 import MAX30102
import hrcalc

class HeartRateMonitor:
    """
    Heart Rate Monitor class using MAX30102 sensor with smoothing,
    validation, and automatic noise rejection.
    """

    LOOP_TIME = 0.01
    PRINT_INTERVAL = 2
    BPM_THRESHOLD = 5
    SPO2_THRESHOLD = 1
    STABILIZATION_TIME = 3  # Grace period to ignore early readings (in seconds)
    MAX_VALID_BPM = 180
    MIN_VALID_BPM = 40

    def __init__(self, print_raw=False, print_result=False):
        self.bpm = 0
        self.spo2 = 0
        self._stop_event = threading.Event()
        self.bpms = []
        self.last_print_time = time.time()
        self.start_time = None
        self.print_raw = print_raw
        self.print_result = print_result
        self.lock = threading.Lock()  # For thread-safe access to bpm and spo2

    def run_sensor(self):
        try:
            sensor = MAX30102()
        except Exception as e:
            print(f"Error initializing sensor: {e}")
            return

        ir_data = []
        red_data = []
        self.start_time = time.time()

        while not self._stop_event.is_set():
            num_bytes = sensor.get_data_present()
            if num_bytes > 0:
                while num_bytes > 0:
                    red, ir = sensor.read_fifo()
                    num_bytes -= 1
                    ir_data.append(ir)
                    red_data.append(red)

                while len(ir_data) > 100:
                    ir_data.pop(0)
                    red_data.pop(0)

                if len(ir_data) == 100:
                    bpm, valid_bpm, spo2, valid_spo2 = hrcalc.calc_hr_and_spo2(ir_data, red_data)

                    # Check signal strength for finger presence
                    if np.mean(ir_data) < 50000 and np.mean(red_data) < 50000:
                        self.bpm = 0
                        self.spo2 = 0
                        continue  # Skip until finger is detected

                    # Grace period to let sensor settle
                    if time.time() - self.start_time < self.STABILIZATION_TIME:
                        continue

                    # Filter out nonsense BPM readings
                    if valid_bpm and self.MIN_VALID_BPM <= bpm <= self.MAX_VALID_BPM:
                        self.bpms.append(bpm)

                        if len(self.bpms) > 4:
                            self.bpms.pop(0)

                        new_bpm = np.mean(self.bpms)
                        new_spo2 = spo2 if valid_spo2 else self.spo2

                        current_time = time.time()
                        if (abs(new_bpm - self.bpm) >= self.BPM_THRESHOLD or
                            abs(new_spo2 - self.spo2) >= self.SPO2_THRESHOLD or
                            current_time - self.last_print_time >= self.PRINT_INTERVAL):

                            self.lock.acquire()
                            self.bpm = new_bpm
                            self.spo2 = new_spo2
                            self.last_print_time = current_time
                            self.lock.release()

                            if self.print_result:
                                print(f"\n--- Heart Rate & SpO2 Update ---")
                                print(f"BPM: {self.bpm:.2f}")
                                print(f"SpO2: {self.spo2:.2f}%")
                                print(f"----------------------------------")

            time.sleep(self.LOOP_TIME)

        sensor.shutdown()

    def start_sensor(self):
        self._stop_event.clear()
        self._thread = threading.Thread(target=self.run_sensor)
        self._thread.start()

    def stop_sensor(self, timeout=2.0):
        self._stop_event.set()
        self._thread.join(timeout)
        self.bpm = 0
        self.spo2 = 0

    def get_data(self):
        print("get_data (heartrate_monitor) dunrcion called")
        """
        Returns the latest smoothed and validated BPM and SpO2 values.
        """
        self.lock.acquire()
        result = {
            "heart_rate": int(round(self.bpm)) if self.bpm > 0 else 0,
            "spo2": int(round(self.spo2)) if self.spo2 > 0 else 0
        }
        self.lock.release()
        return result
