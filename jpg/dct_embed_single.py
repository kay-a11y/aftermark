from aftermark.utils.path import project_path
from PIL import Image
from scipy.fftpack import dct, idct
import numpy as np

def _embed_bit_in_block(block: np.ndarray,
                        Q: np.ndarray,
                        bit: int,
                        a: int = 4,
                        b: int = 3) -> np.ndarray:
    block_f = block.astype(np.float32) - 128
    dct_blk = dct(dct(block_f.T, norm="ortho").T, norm="ortho")
    quant   = np.round(dct_blk / Q)

    quant[a, b] = (int(quant[a, b]) & ~1) | bit 
    dequant     = quant * Q
    idct_blk    = idct(idct(dequant.T, norm="ortho").T, norm="ortho") + 128
    return np.clip(idct_blk, 0, 255)


def embed_uid_single(img_path: str,
                     save_path: str,
                     msg: str,
                     Q: np.ndarray,
                     channel: int = 0,
                     a: int = 4,
                     b: int = 3,
                     quality: int = 95) -> None:
    img      = Image.open(img_path).convert("YCbCr")
    planes   = list(img.split()) 
    target   = np.array(planes[channel])
    h, w     = target.shape
    hp, wp   = (8 - h % 8) % 8, (8 - w % 8) % 8
    padded   = np.pad(target, ((0, hp), (0, wp)), "constant")
    H, W     = padded.shape

    bits     = "".join(f"{ord(c):08b}" for c in msg)
    bit_i    = 0
    for i in range(0, H, 8):
        for j in range(0, W, 8):
            if bit_i >= len(bits):
                break
            blk = padded[i:i+8, j:j+8]
            padded[i:i+8, j:j+8] = _embed_bit_in_block(blk, Q, int(bits[bit_i]), a, b)
            bit_i += 1
        if bit_i >= len(bits):
            break

    if bit_i < len(bits):
        raise ValueError("Image too small for message at chosen embedding rate.")

    planes[channel] = Image.fromarray(padded[:h, :w].astype(np.uint8))
    stego_ycbcr     = Image.merge("YCbCr", tuple(planes))
    stego_ycbcr.save(save_path,
                     format="JPEG",
                     quality=quality,
                     subsampling=0) 


if __name__ == "__main__":
    Q_STD = np.array([
        [16,11,10,16,24,40,51,61],
        [12,12,14,19,26,58,60,55],
        [14,13,16,24,40,57,69,56],
        [14,17,22,29,51,87,80,62],
        [18,22,37,56,68,109,103,77],
        [24,35,55,64,81,104,113,92],
        [49,64,78,87,103,121,120,101],
        [72,92,95,98,112,100,103,99]
    ])

    embed_uid_single(
        img_path  = project_path("demo", "cat.jpg"),
        save_path = project_path("artifacts", "jpg", "cat_dct_y.jpg"), # cat_dct_y.jpg, cat_dct_cb.jpg, cat_dct_cr.jpg
        msg       = "uid:123456789",
        Q         = Q_STD,
        channel   = 0      # 0=Y, 1=Cb, 2=Cr
    )
