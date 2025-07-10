from aftermark.utils.path import project_path
from PIL import Image
import json
import numpy as np

img = Image.new("RGB", (200, 200), "white")
arr = np.array(img)
img.save(project_path("artifacts", "lsb_lab", "clean_demo.png"))

payload = {"uid":"123456789",
           "tid":"260239564",
           "ts":"2025-07-01T12:32:57"}

payload_bits = ''.join(f"{ord(c):08b}" for c in json.dumps(payload)) + '00000000' 

flat = arr[:, :, 0].flatten()

for i, bit in enumerate(payload_bits):
    if i >= flat.size:
        break  
    flat[i] = (flat[i] & 0b11111110) | int(bit)

arr[:, :, 0] = flat.reshape(arr[:, :, 0].shape)
wm_img = Image.fromarray(arr)

wm_img.save(project_path("artifacts", "lsb_lab", "hidden_demo.png"))
print("Done. LSB-embedded file: hidden_demo.png")
