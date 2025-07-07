"""
Batch-nukes "snow" pattern watermarks.

USAGE
-----
python nuke.py IN_DIR  OUT_DIR              \
              [--crop PX]                  \
              [--header PX]

 • --crop   : hard-crop this many pixels off the top
              (useful if you never need the status-bar).
 • --header : apply a 3*3 median just to the first PX pixels
              (0 = skip).  Handy when the snow band is limited
              to the header area.
"""

import argparse, pathlib, random
import numpy as np
from PIL import Image, ImageFilter

def clean_image(path, crop_top=0, header_h=0):
    img = Image.open(path).convert("RGB")
    w, h = img.size

    if crop_top:
        img = img.crop((0, crop_top, w, h))

    new_w, new_h = int(img.width * 0.96), int(img.height * 0.96)
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    img = img.resize((w, h), Image.Resampling.LANCZOS)

    img = img.filter(ImageFilter.GaussianBlur(radius=1.3))

    arr = np.array(img, dtype=np.int16)
    noise = np.random.randint(-1, 2, arr.shape)   # -1, 0, or +1
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr, mode="RGB")

    jit_x, jit_y = 0.37, 0.19
    img = img.transform(
            img.size,
            Image.AFFINE,
            (1, 0, jit_x, 0, 1, jit_y),
            resample=Image.Resampling.BICUBIC)

    if header_h > 0:
        w, h = img.size
        header = img.crop((0, 0, w, min(header_h, h))) 
        header = header.filter(ImageFilter.MedianFilter(3))
        img.paste(header, (0, 0))

    return img

# =============== CLI =============== #

def main():
    ap = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("indir",  help="folder with raw screenshots")
    ap.add_argument("outdir", help="where cleaned files go")
    ap.add_argument("--crop", type=int, default=0,
                    help="pixels to crop off the very top")
    ap.add_argument("--header", type=int, default=0,
                    help="height (px) of header band to median-filter; 0 = skip")
    
    args = ap.parse_args()
    in_dir  = pathlib.Path(args.indir)
    out_dir = pathlib.Path(args.outdir); out_dir.mkdir(exist_ok=True)

    for p in in_dir.glob("*.[pjPJ][pnN]*"):   
        cleaned = clean_image(p, crop_top=args.crop, header_h=args.header)
        out_path = out_dir / f"{p.stem}_clean.jpg"
        cleaned.save(out_path, format="JPEG", quality=40, optimize=True, subsampling=2)
        print(f"✔ {out_path.name}")

if __name__ == "__main__":
    main()
