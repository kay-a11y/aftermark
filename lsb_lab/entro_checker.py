from aftermark.utils.path import project_path
from PIL import Image
import collections, math
import numpy as np
import os
import string

def shannon_entropy(data):
    if not data: return 0
    freq = collections.Counter(data)
    return -sum((c/len(data))*math.log2(c/len(data)) for c in freq.values())

def printable_ratio(msg):
    if not msg: return 0
    return sum(1 for c in msg if c in string.printable) / len(msg)

IMG_DIR = project_path("artifacts", "nuke")
LOG = project_path("artifacts", "logs", IMG_DIR.name)

with open(LOG, "w", encoding="utf-8") as f:
    for fn in sorted(os.listdir(IMG_DIR)):
        if not fn.lower().endswith(('.PNG', '.png', '.jpg', '.jpeg', '.bmp', '.webp')):
            continue
        img_path = os.path.join(IMG_DIR, fn)
        arr = np.array(Image.open(img_path))
        nchan = 1 if arr.ndim == 2 else arr.shape[2]
        for ch in range(nchan):
            if nchan == 1:
                flat = arr.flatten()
                label = 'Gray'
            else:
                flat = arr[:, :, ch].flatten()
                label = "RGB"[ch]
            bits = ''.join(str(px & 1) for px in flat)
            chars = []
            for i in range(0, len(bits), 8):
                byte = bits[i:i+8]
                if len(byte) < 8: break
                val = int(''.join(byte), 2)
                if val == 0: break
                chars.append(chr(val))
            msg = ''.join(chars)
            raw = msg.encode('latin-1', errors='replace')
            ent = shannon_entropy(raw)
            pratio = printable_ratio(msg)
            has_uid = b"uid" in raw.lower()
            if len(msg) > 0 or ent > 0.5 or pratio > 0.5 or has_uid:
                f.write(f"{fn:>20s} [{label}]  len:{len(msg):4d}  ent:{ent:5.2f}  printable:{100*pratio:4.1f}%  uid:{has_uid}\n")
            if len(msg) > 0 and ent > 0.5 and pratio > 0.5:
                f.write(f"*msg*:{msg}\n")
                print(f"*msg*:{msg}\n")
            if ent > 0.5 or pratio > 0.3 or has_uid:
                print(f"[{fn:>16s}] Channel {label}  len:{len(msg)}  ent:{ent:.2f}  printable:{100*pratio:.1f}%  uid:{has_uid}")
print(f"\nChannel sweep complete! See {LOG} for details.")
