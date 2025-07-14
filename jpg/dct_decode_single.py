from aftermark.utils.path import project_path
from PIL import Image
from scipy.fftpack import dct
import numpy as np
import os

def decode_uid(img, Q, channel=0, hid_a=4, hid_b=3, try_bit=200):
    stego_img = Image.open(img).convert("YCbCr")

    target_channel = np.array(stego_img)[:, :, channel]

    h, w  = target_channel.shape
    h_pad = (8 - h % 8) % 8
    w_pad = (8 - w % 8) % 8
    target_padded = np.pad(target_channel, ((0, h_pad), (0, w_pad)), mode="constant")

    bits = ""
    for i in range(0, target_padded.shape[0], 8):
        for j in range(0, target_padded.shape[1], 8):
            block     = target_padded[i:i+8, j:j+8].astype(np.float32) - 128
            dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
            quant     = np.round(dct_block / Q)
            bit       = int(quant[hid_a][hid_b]) & 1
            bits      += str(bit)

            if len(bits) >= try_bit:
                break
        if len(bits) >= try_bit:
            break        

    def bits_to_text(bitstring):
        chars = [bitstring[i:i+8] for i in range(0, len(bitstring), 8)]
        text  = ""
        for b in chars:
            try:
                text += chr(int(b, 2))
            except:
                break
        return text
    
    decoded_text = bits_to_text(bits[:try_bit])  # Try first 200 bits for now

    print("first 64 bits:", bits[:64])
    print("ascii preview:",
        "".join(chr(int(bits[i:i+8],2)) for i in range(0,64,8)))
    print(f"decoded_text = {decoded_text}")

    return decoded_text


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
    
    # === single image decoding ===
    # img = project_path("artifacts", "jpg", "cat_dct_y.jpg") # or channel=1, channel=2

    # decode_uid(img, Q, channel=0, hid_a=4, hid_b=3, try_bit=200)  # or channel=1, channel=2

    # === mass decoding ===
    imgs_folder =project_path("artifacts", "jpg", "dct_y")  # or dct_cb, dct_cr, dct, etc.
    imgs = os.listdir(imgs_folder)

    print(f"folder: {imgs_folder}")

    for _ in range(3):
        print(f"{'-'*45}\nchannel: {_}\n{'-'*45}")
        for img in imgs:
            print(f"[{img}]:")
            img = os.path.join(imgs_folder, img)
            decode_uid(img, Q, channel=_, hid_a=4, hid_b=3, try_bit=200)