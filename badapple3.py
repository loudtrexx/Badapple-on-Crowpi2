import os
import time
import pygame
from PIL import Image
from rpi_ws281x import PixelStrip, Color

# --- LED matrix config ---
LED_COUNT   = 64       # 8x8 matrix
LED_PIN     = 18       # GPIO pin connected to DIN
LED_FREQ_HZ = 800000
LED_DMA     = 10
LED_BRIGHT  = 50
LED_INVERT  = False
LED_CHANNEL = 0

# --- Frame config ---
FRAME_DIR = "./frames"   # folder with frame_*.png
FPS = 28 # frames per second

pygame.mixer.init()
pygame.mixer.music.load("badapple.mp3")
pygame.mixer.music.play()
            

def to_led_index(x, y):
    """Map (x,y) to LED index. Adjust if your matrix wiring differs."""
    if y % 2 == 0:
        return y*8 + x
    else:
        return y*8 + (7-x)

def load_frames():
    files = sorted([f for f in os.listdir(".") if f.startswith("frame_") and f.endswith(".png")])
    frames = []
    for fname in files:
        img = Image.open(fname).convert("RGB").resize((8,8))
        frames.append(img)
    return frames

def show_frame(strip, img):
    for y in range(8):
        for x in range(8):
            r,g,b = img.getpixel((x,y))
            strip.setPixelColor(to_led_index(x,y), Color(r,g,b))
    strip.show()

def main():
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHT, LED_CHANNEL)
    strip.begin()

    frames = load_frames()
    if not frames:
        print("No frames found in", FRAME_DIR)
        return
    

    delay = 1.0 / FPS
    try:
        while pygame.mixer.music.get_busy():
            pos_ms = pygame.mixer.music.get_pos()
            frame_index = int((pos_ms / 1000) * FPS) % len(frames)
            show_frame(strip, frames[frame_index])
            time.sleep(0.01)
    #    while True:
   #         for img in frames:
  #              show_frame(strip, img)
 #               time.sleep(delay)
    except KeyboardInterrupt:
        # Clear matrix on exit
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0,0,0))
        strip.show()

if __name__ == "__main__":
    main()

