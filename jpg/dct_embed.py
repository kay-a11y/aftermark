from aftermark.utils.path import project_path
from scipy.fftpack import dct, idct
from PIL import Image
import numpy as np

def _embed_bit_in_block(block, Q, bit, a=4, b=3):
    block   = block.astype(np.float32) - 128
    dct_blk = dct(dct(block.T, norm="ortho").T, norm="ortho")
    quant   = np.round(dct_blk / Q)

    coeff       = int(quant[a][b])
    quant[a][b] = (coeff & ~1) | bit 
    dequant     = quant * Q
    idct_blk    = idct(idct(dequant.T, norm="ortho").T, norm="ortho") + 128
    return np.clip(idct_blk, 0, 255)

def embed_uid_all(img_path, save_path, msg, Q, a=4, b=3):
    img     = Image.open(img_path).convert("YCbCr")
    ycbcr   = np.array(img)    
    bits    = "".join(f"{ord(c):08b}" for c in msg)
    h, w, _ = ycbcr.shape
    hp, wp  = (8 - h % 8) % 8, (8 - w % 8) % 8
    padded  = np.pad(ycbcr, ((0,hp),(0,wp),(0,0)), "constant")

    H, W  = padded.shape[:2]
    bit_i = 0
    for ch in range(3):  
        for i in range(0, H, 8):
            for j in range(0, W, 8):
                if bit_i >= len(bits): break
                blk   = padded[i:i+8, j:j+8, ch]
                bit   = int(bits[bit_i])
                padded[i:i+8, j:j+8, ch] = _embed_bit_in_block(blk, Q, bit, a, b)
                bit_i += 1
        bit_i = 0   

    stego = Image.fromarray(padded[:h,:w,:]).convert("YCbCr")
    stego.save(save_path, format="JPEG", quality=95, subsampling=0)

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

    embed_uid_all(
        img_path = project_path("demo", "cat.jpg"),
        save_path= project_path("artifacts", "jpg", "cat_dct.jpg"),
        msg      = "uid:123456789",
        Q        = Q,
        a=4, b=3
    )
