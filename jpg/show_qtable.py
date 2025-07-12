from aftermark.utils.path import project_path
from PIL import Image

img = Image.open(project_path("demo", "cat.jpg"))
qtables = img.quantization
print(qtables)