from aftermark.utils.path import project_path
from PIL import Image
import numpy as np

arr = np.array(Image.open(project_path("artifacts", "lsb_lab", "hidden_demo.png")))
flat = arr[:, :, 0].flatten()
payload_bits = ''.join(f"{ord(c):08b}" for c in '{"uid": "123456789", "tid": "260239564", "ts": "2025-07-01T12:32:57"}') + '00000000'

for i, bit in enumerate(payload_bits):
    if i >= flat.size: break
    y, x = divmod(i, arr.shape[1])
    if bit == '1':
        arr[y, x] = [255,0,0]  # red for 1
    else:
        arr[y, x] = [0,0,255]  # blue for 0

img3 = Image.fromarray(arr)
img3.save("artifacts", "lsb_lab", "hidden_demo_colored.png")
