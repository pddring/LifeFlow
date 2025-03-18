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

# Initialize I2C and accelerometer
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
ADXL343_ADDR = 0x53
i2c.writeto(ADXL343_ADDR, bytearray([0x2D, 0x08]))  # Power on
i2c.writeto(ADXL343_ADDR, bytearray([0x31, 0x00]))  # Set ±2g mode

# Thresholds
FREE_FALL_THRESHOLD = 0.4  # g (Below this = free fall)

# Initialize display
display = badger2040.Badger2040()
display.set_font("bitmap8")
display.led(128)

# Initialize image decoders
png = pngdec.PNG(display.display)
jpeg = jpegdec.JPEG(display.display)

APP_DIR = "/examples"
FONT_SIZE = 2
changed = False
fall_detected = False  # Prevent multiple fall triggers
emergency_triggered = False  # Defer emergency launch

# State management for persistence
state = {"fall_detected": False, "page": 0, "running": "launcher"}
badger_os.state_load("fall_detection", state)

# Reset mechanism
if badger2040.pressed_to_wake(badger2040.BUTTON_A) and badger2040.pressed_to_wake(badger2040.BUTTON_C):
    print("Resetting fall detection state.")
    # Reinitialize the state dictionary
    state = {"fall_detected": False, "page": 0, "running": "launcher"}
    # Save the new state to persistent storage
    badger_os.state_save("fall_detection", state)
    print("Fall detection state has been reset.")


# Populate examples
examples = [x[:-3] for x in os.listdir(APP_DIR) if x.endswith(".py")]
centers = (41, 147, 253)
MAX_PAGE = math.ceil(len(examples) / 3)
WIDTH = 296


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


def check_fall():
    """Monitors the accelerometer for a free-fall event."""
    global fall_detected, emergency_triggered

    while not fall_detected:
        x, y, z, total_acc = get_acceleration()
        print(f"X: {x:.2f}g, Y: {y:.2f}g, Z: {z:.2f}g, Total: {total_acc:.2f}g")

        if total_acc < FREE_FALL_THRESHOLD:
            print("🚨 Free Fall Detected! Deferring emergency app launch.")
            fall_detected = True
            emergency_triggered = True  # Signal for deferred app launch
            return  # Exit the function to stop further fall detection

        time.sleep(0.1)


if not state["fall_detected"]:
    # Start fall detection thread
    _thread.start_new_thread(check_fall, ())


def render():
    """Renders the app launcher UI."""
    display.set_pen(15)
    display.clear()
    display.set_pen(0)

    max_icons = min(3, len(examples[(state["page"] * 3):]))  # Update max icons for the current page

    for i in range(max_icons):
        x = centers[i]
        label = examples[i + (state["page"] * 3)]
        icon_label = label.replace("_", "-")
        icon = f"{APP_DIR}/icon-{icon_label}"
        label = label.replace("_", " ")
        for lib, ext in [(png, "png"), (jpeg, "jpg")]:
            try:
                lib.open_file(f"{icon}.{ext}")
                lib.decode(x - 26, 30)
                break
            except (OSError, RuntimeError):
                continue
        display.set_pen(0)
        w = display.measure_text(label, FONT_SIZE)
        display.text(label, int(x - (w / 2)), 16 + 80, WIDTH, FONT_SIZE)

    # Draw page indicators
    for i in range(MAX_PAGE):
        x = 286
        y = int((128 / 2) - (MAX_PAGE * 10 / 2) + (i * 10))
        display.set_pen(0)
        display.rectangle(x, y, 8, 8)
        if state["page"] != i:
            display.set_pen(15)
            display.rectangle(x + 1, y + 1, 6, 6)

    display.set_pen(0)
    display.rectangle(0, 0, WIDTH, 16)
    display.set_pen(15)
    display.text("badgerOS", 4, 4, WIDTH, 1.0)

    display.update()


def wait_for_user_to_release_buttons():
    while display.pressed_any():
        time.sleep(0.01)


def launch_example(index):
    wait_for_user_to_release_buttons()
    file = examples[(state["page"] * 3) + index]
    badger_os.launch(f"{APP_DIR}/{file}")


def button(pin):
    global changed
    changed = True

    if pin == badger2040.BUTTON_A:
        launch_example(0)
    if pin == badger2040.BUTTON_B:
        launch_example(1)
    if pin == badger2040.BUTTON_C:
        launch_example(2)
    if pin == badger2040.BUTTON_UP:
        state["page"] = (state["page"] - 1) % MAX_PAGE
        render()
    if pin == badger2040.BUTTON_DOWN:
        state["page"] = (state["page"] + 1) % MAX_PAGE
        render()


# Initial rendering
if not state["fall_detected"]:
    render()

while True:
    # Handle button presses and UI updates
    display.keepalive()

    if emergency_triggered:
        print("🚨 Launching emergency app outside callback context.")
        emergency_triggered = False
        badger_os.launch("/examples/emergency.py")
    
    # Check for A + C combination to exit to launcher
    if display.pressed(badger2040.BUTTON_A) and display.pressed(badger2040.BUTTON_C):
        print("Exiting to launcher via A + C.")
        wait_for_user_to_release_buttons()  # Ensure buttons are released
        badger_os.launch("launcher")  # Exit to launcher
        break  # Exit loop to prevent additional actions

    # Check individual button presses
    if display.pressed(badger2040.BUTTON_A):
        button(badger2040.BUTTON_A)
    elif display.pressed(badger2040.BUTTON_B):
        button(badger2040.BUTTON_B)
    elif display.pressed(badger2040.BUTTON_C):
        button(badger2040.BUTTON_C)
    elif display.pressed(badger2040.BUTTON_UP):
        button(badger2040.BUTTON_UP)
    elif display.pressed(badger2040.BUTTON_DOWN):
        button(badger2040.BUTTON_DOWN)

    if changed:
        badger_os.state_save("launcher", state)
        changed = False

    time.sleep(0.1)  # Add delay to debounce button checks

