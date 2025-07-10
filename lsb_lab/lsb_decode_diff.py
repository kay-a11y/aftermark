from aftermark.utils.path import project_path
from PIL import Image
import numpy as np

img = Image.open(project_path("artifacts", "lsb_lab", "demo_wm.png")).convert("RGB")
arr = np.array(img)

def bits_to_char(bits):
    return chr(int(''.join(bits), 2))

bits_r = [str(arr[0, x, 0] & 1) for x in range(8)]
bits_g = [str(arr[0, x, 1] & 1) for x in range(8)]
bits_b = [str(arr[0, x, 2] & 1) for x in range(8)]

secret = bits_to_char(bits_r) + bits_to_char(bits_g) + bits_to_char(bits_b)
print("Hidden message:", secret)            # → CAT
