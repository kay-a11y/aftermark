from aftermark.utils.path import project_path
from PIL import Image
import io

img = Image.open(project_path("demo", "cat.jpg"))
sizes = []

N = 100  # or any wild value you like
buf = io.BytesIO()
img.save(buf, format="PNG")
buf.seek(0)
sizes.append(('PNG', len(buf.getvalue()) / 1024))

for i in range(1, N+1):
    buf_jpg = io.BytesIO()
    Image.open(io.BytesIO(buf.getvalue())).save(buf_jpg, format="JPEG", quality=85)
    buf_jpg.seek(0)
    sizes.append(('JPG', len(buf_jpg.getvalue()) / 1024))

    buf_png = io.BytesIO()
    Image.open(io.BytesIO(buf_jpg.getvalue())).save(buf_png, format="PNG")
    buf_png.seek(0)
    sizes.append(('PNG', len(buf_png.getvalue()) / 1024))

    buf = buf_png 

with open(project_path("artifacts", "logs", f"gonewild_sizes_{N}.txt"), "w") as f:
    for i, (fmt, sz) in enumerate(sizes):
        f.write(f"Step {i}: {fmt} size = {sz:.1f} KB\n")
print(f"\nAll sizes written to gonewild_sizes_{N}.txt")
