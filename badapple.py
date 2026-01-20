import RPi.GPIO as GPIO
import time
import json

# --- CONFIGURATION ---
# Adjust these pin mappings to match CrowPi 2’s block display wiring
ROW_PINS = [5, 6, 13, 19, 26, 12, 16, 20]   # Example row pins
COL_PINS = [21, 22, 23, 24, 25, 27, 17, 4]  # Example column pins

FPS = 15   # Frames per second

# --- SETUP ---
GPIO.setmode(GPIO.BCM)

for pin in ROW_PINS + COL_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def clear_display():
    for r in ROW_PINS:
        GPIO.output(r, GPIO.LOW)
    for c in COL_PINS:
        GPIO.output(c, GPIO.LOW)

def show_frame(frame):
    """
    frame: 8x8 list of 0/1 values
    """
    for y in range(8):
        for x in range(8):
            GPIO.output(ROW_PINS[y], GPIO.HIGH)
            if frame[y][x] == 1:
                GPIO.output(COL_PINS[x], GPIO.HIGH)
            else:
                GPIO.output(COL_PINS[x], GPIO.LOW)
        # small delay to stabilize row
        time.sleep(0.001)
        GPIO.output(ROW_PINS[y], GPIO.LOW)

# --- LOAD FRAMES ---
# You need to preprocess Bad Apple!! frames into JSON or .npy format
# Example: frames.json contains a list of 8x8 arrays
with open("frames.json", "r") as f:
    frames = json.load(f)

# --- PLAYBACK LOOP ---
try:
    for frame in frames:
        show_frame(frame)
        time.sleep(1/FPS)
finally:
    clear_display()
    GPIO.cleanup()
