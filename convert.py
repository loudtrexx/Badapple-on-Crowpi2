from PIL import Image
import glob, json

frames = []
for file in sorted(glob.glob("frame_*.png")):
    img = Image.open(file).convert("L")
    pixels = [[1 if img.getpixel((x,y)) < 128 else 0 for x in range(8)] for y in range(8)]
    frames.append(pixels)

with open("frames.json", "w") as f:
    json.dump(frames, f)
