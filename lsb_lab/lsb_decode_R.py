from aftermark.utils.path import project_path
from PIL import Image
import numpy as np

arr = np.array(Image.open(project_path("artifacts", "lsb_lab", "hidden_demo.png")))
flat = arr[:, :, 0].flatten()
bits = ''.join(str(px & 1) for px in flat) 

chars = []
for i in range(0, len(bits), 8):
    byte = bits[i:i+8]
    if len(byte) < 8:
        break
    val = int(''.join(byte), 2)
    if val == 0:
        break
    chars.append(chr(val))
msg = ''.join(chars)
print("Decoded hidden message:", msg)
