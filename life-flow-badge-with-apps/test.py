import gc
import os
import time
import machine
import struct
import badger2040
import badger_os
import _thread

# Initialize I2C and accelerometer
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
ADXL343_ADDR = 0x53
i2c.writeto(ADXL343_ADDR, bytearray([0x2D, 0x08]))  # Power on
i2c.writeto(ADXL343_ADDR, bytearray([0x31, 0x00]))  # Set ±2g mode

# Thresholds
FREE_FALL_THRESHOLD_SQ = 0.4 ** 2  # squared g

# Initialize display
display = badger2040.Badger2040()
display.set_font("bitmap8")
display.led(128)

APP_DIR = "/examples"
centers = (41, 147, 253)
WIDTH = 296

# State management
state = {"fall_detected": False, "page": 0, "running": "launcher"}
badger_os.state_load("fall_detection", state)

changed = False
fall_detected = False
emergency_triggered = False

# Reset mechanism
if badger2040.pressed_to_wake(badger2040.BUTTON_A) and badger2040.pressed_to_wake(badger2040.BUTTON_C):
    print("Resetting fall detection state.")
    state = {"fall_detected": False, "page": 0, "running": "launcher"}
    badger_os.state_save("fall_detection", state)
    print("Fall detection state has been reset.")

def get_examples():
    return [x[:-3] for x in os.listdir(APP_DIR) if x.endswith(".py")]

examples = get_examples()
MAX_PAGE = -(-len(examples) // 3)  # ceiling division

def get_acceleration():
    raw = i2c.readfrom_mem(ADXL343_ADDR, 0x32, 6)
    x, y, z = struct.unpack('<hhh', raw)
    x_g, y_g, z_g = x / 256.0, y / 256.0, z / 256.0
    total_sq = x_g**2 + y_g**2 + z_g**2
    return x_g, y_g, z_g, total_sq

def check_fall():
    global fall_detected, emergency_triggered
    while not fall_detected:
        _, _, _, total_sq = get_acceleration()
        if total_sq < FREE_FALL_THRESHOLD_SQ:
            print("🚨 Free Fall Detected!")
            fall_detected = True
            emergency_triggered = True
            return
        time.sleep(0.1)

if not state["fall_detected"]:
    _thread.start_new_thread(check_fall, ())

def render():
    import pngdec, jpegdec
    png = pngdec.PNG(display.display)
    jpeg = jpegdec.JPEG(display.display)

    display.set_pen(15)
    display.clear()
    display.set_pen(0)

    page_start = state["page"] * 3
    page_examples = examples[page_start:page_start + 3]

    for i, label in enumerate(page_examples):
        x = centers[i]
        icon_label = label.replace("_", "-")
        icon_path = f"{APP_DIR}/icon-{icon_label}"
        label_display = label.replace("_", " ")
        for decoder, ext in [(png, "png"), (jpeg, "jpg")]:
            try:
                decoder.open_file(f"{icon_path}.{ext}")
                decoder.decode(x - 26, 30)
                break
            except (OSError, RuntimeError):
                continue
        display.set_pen(0)
        w = display.measure_text(label_display, 2)
        display.text(label_display, int(x - w / 2), 96, WIDTH, 2)

    for i in range(MAX_PAGE):
        x, y = 286, int((128 / 2) - (MAX_PAGE * 10 / 2) + (i * 10))
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
    gc.collect()

def wait_for_user_to_release_buttons():
    while display.pressed_any():
        time.sleep(0.01)

def launch_example(index):
    wait_for_user_to_release_buttons()
    file = examples[(state["page"] * 3) + index]
    badger_os.launch(f"{APP_DIR}/{file}")
    gc.collect()

def button(pin):
    global changed
    changed = True
    if pin == badger2040.BUTTON_A:
        launch_example(0)
    elif pin == badger2040.BUTTON_B:
        launch_example(1)
    elif pin == badger2040.BUTTON_C:
        launch_example(2)
    elif pin == badger2040.BUTTON_UP:
        state["page"] = (state["page"] - 1) % MAX_PAGE
        render()
    elif pin == badger2040.BUTTON_DOWN:
        state["page"] = (state["page"] + 1) % MAX_PAGE
        render()

if not state["fall_detected"]:
    render()

while True:
    display.keepalive()

    if emergency_triggered:
        emergency_triggered = False
        badger_os.launch("/examples/emergency.py")
        break

    if display.pressed(badger2040.BUTTON_A) and display.pressed(badger2040.BUTTON_C):
        print("Exiting to launcher via A + C")
        wait_for_user_to_release_buttons()
        badger_os.launch("launcher")
        break

    for btn in [badger2040.BUTTON_A, badger2040.BUTTON_B, badger2040.BUTTON_C,
                badger2040.BUTTON_UP, badger2040.BUTTON_DOWN]:
        if display.pressed(btn):
            button(btn)
            break

    if changed:
        badger_os.state_save("launcher", state)
        changed = False

    time.sleep(0.1)