from aftermark.utils.path import project_path
from PIL import Image
from scipy.fftpack import dct
import numpy as np
import os

def _extract_bit(block, Q, a, b):
    """Return LSB of quantised coefficient [a,b] in this 8*8 block."""
    blk = block.astype(np.float32) - 128
    coeff = np.round(dct(dct(blk.T, norm="ortho").T, norm="ortho") / Q)[a, b]
    return int(coeff) & 1

def decode_uid_majority(img_path, Q, a=4, b=3, try_bits=200):
    """
    Read bits from Y, Cb, Cr •vote per block• and turn into ASCII.
    """
    y, cb, cr = Image.open(img_path).convert("YCbCr").split()
    planes = [np.array(ch) for ch in (y, cb, cr)]

    # pad all channels the same
    h, w = planes[0].shape
    hp, wp = (8 - h % 8) % 8, (8 - w % 8) % 8
    planes = [np.pad(p, ((0, hp), (0, wp)), "constant") for p in planes]
    H, W   = planes[0].shape

    bits = ""
    for i in range(0, H, 8):
        for j in range(0, W, 8):
            votes = [
                _extract_bit(p[i:i+8, j:j+8], Q, a, b)
                for p in planes
            ]
            bit = 1 if sum(votes) >= 2 else 0   # majority of 3
            bits += str(bit)
            if len(bits) >= try_bits:           # enough for preview
                break
        if len(bits) >= try_bits:
            break

    # convert to text
    chars = [bits[k:k+8] for k in range(0, len(bits), 8)]
    msg   = "".join(chr(int(c, 2)) for c in chars if len(c) == 8)
    print("bits[0:64] :", bits[:64])
    print("ascii preview:", msg[:8])
    return msg

if __name__ == "__main__":
    Q = np.array([
        [16,11,10,16,24,40,51,61],
        [12,12,14,19,26,58,60,55],
        [14,13,16,24,40,57,69,56],
        [14,17,22,29,51,87,80,62],
        [18,22,37,56,68,109,103,77],
        [24,35,55,64,81,104,113,92],
        [49,64,78,87,103,121,120,101],
        [72,92,95,98,112,100,103,99]
    ])

    # === single img decode ===
    # img = project_path("artifacts", "jpg", "dct", "cat_stego_all.jpg")
    # msg = decode_uid_majority(img, Q, try_bits=256)
    # print("\nDecoded (Majority):", msg)

    # === mass decode ===
    imgs_folder = project_path("artifacts", "jpg", "dct")
    imgs = os.listdir(imgs_folder)
    print(f"folder: {imgs_folder}")

    for img in imgs:
        print(f"[{img}]:")
        img = os.path.join(imgs_folder, img)
        print(decode_uid_majority(img, Q, try_bits=256))