from aftermark.utils.path import project_path
from PIL import Image
import numpy as np

arr2 = np.array(Image.open(project_path("artifacts", "lsb_lab", "demo2_all_wm.png")))
flat2 = arr2.reshape(-1, 3)

bits_r = ''.join(str(px[0] & 1) for px in flat2[:24])
# Or for G/B: px[1], px[2]

chars = []
for i in range(0, len(bits_r), 8):
    byte = bits_r[i:i+8]
    val = int(byte, 2)
    if val == 0:
        break
    chars.append(chr(val))
msg = ''.join(chars)
print("Extracted message:", msg)
