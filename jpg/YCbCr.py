from aftermark.utils.path import project_path
from PIL import Image, ImageFilter

# === show Y / cb / cr ===
img = Image.open(project_path("demo", "cat.jpg"))
channels = img.convert("YCbCr").split()
names = ["y", "cb", "cr"]

for c, name in zip(channels, names):
    c.save(project_path("artifacts", "jpg", f"cat_{name}.png"))

# === Blur Y / Blur cb / Blur cr -> merge ===
y, cb, cr = channels

blurred_y = y.filter(ImageFilter.GaussianBlur(radius=3))
img = Image.merge("YCbCr", (blurred_y, cb, cr))

blurred_cb = cb.filter(ImageFilter.GaussianBlur(radius=3))
blurred_cr = cr.filter(ImageFilter.GaussianBlur(radius=3))
img = Image.merge("YCbCr", (y, blurred_cb, blurred_cr))
img.convert("RGB").show()

for i, name in enumerate(names):
    blurred = channels[i].filter(ImageFilter.GaussianBlur(radius=3))
    merged = list(channels)
    merged[i] = blurred
    img_blur = Image.merge("YCbCr", merged)
    img_rgb = img_blur.convert("RGB")
    img_rgb.save(project_path("artifacts", "jpg", f"cat_blur_{name}.png"))

