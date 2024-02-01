import RPi.GPIO as GPIO
import time
import subprocess

emailCode = "emailsystem.py"

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
button1_pin = 17    # Change this to the actual GPIO pin you've connected the first button to
button2_pin = 20    # Change this to the actual GPIO pin you've connected the second button to
button3_pin = 26    # Change this to the actual GPIO pin you've connected the third button to
led1_pin = 18       # Change this to the actual GPIO pin you've connected the first LED to
led2_pin = 21       # Change this to the actual GPIO pin you've connected the second LED to
led3_pin = 16       # Change this to the actual GPIO pin you've connected the third LED to
buzzer_pin = 12     # Change this to the actual GPIO pin you've connected the buzzer to

# Set up GPIO pins
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led1_pin, GPIO.OUT)
GPIO.setup(led2_pin, GPIO.OUT)
GPIO.setup(led3_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)

buzzer_pwm = GPIO.PWM(buzzer_pin, 1000)  # 1000 Hz initial frequency

def turn_on_led(led_pin):
    GPIO.output(led_pin, GPIO.HIGH)

def turn_off_led(led_pin):
    GPIO.output(led_pin, GPIO.LOW)

def activate_buzzer(pitch=1000, duration=0.1):
    # Activate the buzzer with the specified pitch for the specified duration
    buzzer_pwm.ChangeFrequency(pitch)
    buzzer_pwm.start(50)  # Duty cycle set to 50%
    time.sleep(duration)
    deactivate_buzzer()

def deactivate_buzzer():
    # Turn off the buzzer
    buzzer_pwm.stop()

def rightbutton():
    print("Button 1 clicked!")

def middlebutton():
    subprocess.run(["python", emailCode])

def leftbutton():
    print("Button 3 clicked!")

def handle_button_press(button_pin, led_pin, pitch, duration, button_function):
    if GPIO.input(button_pin) == GPIO.LOW:
        print(f"Button Pressed on Pin {button_pin}!")
        # Turn on the corresponding LED
        turn_on_led(led_pin)
        # Activate the buzzer for one beep (you can change the pitch and duration as needed)
        activate_buzzer(pitch, duration)
        # Run the empty function
        button_function()
        # Wait for the button to be released
        while GPIO.input(button_pin) == GPIO.LOW:
            time.sleep(0.1)
        # Turn off the corresponding LED
        turn_off_led(led_pin)

try:
    while True:
        # Pass the appropriate empty function for each button
        handle_button_press(button1_pin, led1_pin, 1500, 0.1, rightbutton)
        handle_button_press(button2_pin, led2_pin, 2000, 0.1, middlebutton)
        handle_button_press(button3_pin, led3_pin, 2500, 0.1, leftbutton)
        time.sleep(0.1)  # Add a small delay to avoid button bouncing

except KeyboardInterrupt:
    pass

finally:
    # Turn off all LEDs and the buzzer
    turn_off_led(led1_pin)
    turn_off_led(led2_pin)
    turn_off_led(led3_pin)
    deactivate_buzzer()

    # Clean up GPIO
    GPIO.cleanup()
