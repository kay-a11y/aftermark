from aftermark.utils.path import project_path
from PIL import Image
from scipy.fftpack import dct
import numpy as np
import os

def _bit(block, Q, a, b):
    blk = block.astype(np.float32) - 128
    coeff = np.round(dct(dct(blk.T, norm="ortho").T, norm="ortho") / Q)[a, b]
    return int(coeff) & 1

def decode_tri_or(img_path, Q, a=4, b=3, try_bits=128):
    y, cb, cr = Image.open(img_path).convert("YCbCr").split()
    planes = [np.array(p) for p in (y, cb, cr)]
    h, w = planes[0].shape
    hp, wp = (8-h%8)%8, (8-w%8)%8
    planes = [np.pad(p, ((0,hp),(0,wp)), "constant") for p in planes]
    H, W = planes[0].shape

    bits_y = bits_cb = bits_cr = ""
    for i in range(0, H, 8):
        for j in range(0, W, 8):
            bits_y  += str(_bit(planes[0][i:i+8, j:j+8], Q, a, b))
            bits_cb += str(_bit(planes[1][i:i+8, j:j+8], Q, a, b))
            bits_cr += str(_bit(planes[2][i:i+8, j:j+8], Q, a, b))
            if len(bits_y) >= try_bits:
                break
        if len(bits_y) >= try_bits:
            break

    bits_or = "".join("1" if (int(y) | int(u) | int(v)) else "0"
                      for y, u, v in zip(bits_y, bits_cb, bits_cr))

    def to_ascii(bitstr):
        chars = [bitstr[k:k+8] for k in range(0, len(bitstr), 8)]
        return "".join(chr(int(c,2)) for c in chars if len(c)==8)

    print("Y  :", bits_y[:64])
    print("Cb :", bits_cb[:64])
    print("Cr :", bits_cr[:64])
    print("OR :", bits_or[:64], "\n")
    print("ASCII-preview (OR):", to_ascii(bits_or)[:32])

    return to_ascii(bits_or)

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
    # msg = decode_tri_or(img_path, Q, try_bits=256)
    # print("\nDecoded (OR):", msg)

    # === mass decode ===
    imgs_folder = project_path("artifacts", "jpg", "dct")
    imgs = os.listdir(imgs_folder)
    print(f"folder: {imgs_folder}")

    for img in imgs:
        print(f"[{img}]:")
        img = os.path.join(imgs_folder, img)
        print(decode_tri_or(img, Q, try_bits=256))