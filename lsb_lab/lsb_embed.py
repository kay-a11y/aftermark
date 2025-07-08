from PIL import Image
import numpy as np
import json

img = Image.new("RGB", (200, 200), "white")
arr = np.array(img)

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

wm_img.save("hidden_demo.png")
print("Done. LSB-embedded file: hidden_demo.png")
