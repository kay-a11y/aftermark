from aftermark.utils.path import project_path
from PIL import Image
import numpy as np

msg = "CAT"
img = Image.open(project_path("demo", "demo2.jpg")).convert("RGB")
arr = np.array(img)

bits = ''.join(f"{ord(c):08b}" for c in msg)
N = len(bits)

h, w, _ = arr.shape
flat = arr.reshape(-1, 3)

for i, bit in enumerate(bits):
    for chan in range(3):  # R, G, B
        flat[i, chan] = (flat[i, chan] & 0b11111110) | int(bit)

# Optionally
for j in range(3):
    flat[N, j] = flat[N, j] & 0b11111110

arr2 = flat.reshape(h, w, 3)
Image.fromarray(arr2).save(project_path("artifacts", "lsb_lab", "demo2_all_wm.png"))
print("Watermark embedded in all channels!")
