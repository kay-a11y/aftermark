from aftermark.utils.path import project_path
from PIL import Image
import numpy as np

img = Image.open(project_path("demo", "demo.jpg")).convert("RGB")
arr = np.array(img)

watermark_r = format(ord("C"), "08b")
watermark_g = format(ord("A"), "08b")
watermark_b = format(ord("T"), "08b")

for i, bit in enumerate(watermark_r):
    arr[0, i, 0] = (arr[0, i, 0] & 0b11111110) | int(bit)  # Red
for i, bit in enumerate(watermark_g):
    arr[0, i, 1] = (arr[0, i, 1] & 0b11111110) | int(bit)  # Green
for i, bit in enumerate(watermark_b):
    arr[0, i, 2] = (arr[0, i, 2] & 0b11111110) | int(bit)  # Blue

Image.fromarray(arr).save(project_path("artifacts", "lsb_lab", "demo_wm.png")) # must use a loss-less format, instead of .jpg 
