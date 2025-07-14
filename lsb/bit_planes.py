from aftermark.utils.path import project_path
import cv2
import matplotlib.pyplot as plt

img = cv2.imread(project_path("demo", "demo2.jpg"), 0)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

fig, axs = plt.subplots(3, 8, figsize=(18, 6))
channels = ["Red", "Green", "Blue"]

for c in range(3):
    for b in range(8):
        plane = ((img[:, :, c] >> b) & 1) * 255
        axs[c, 7-b].imshow(plane, cmap='gray')
        axs[c, 7-b].set_title(f"{channels[c]}: Bit {7-b}")
        axs[c, 7-b].axis('off')

plt.tight_layout()
plt.savefig(project_path("artifacts", "lsb", "bitplanes_grid.png"), bbox_inches='tight', pad_inches=0.1, dpi=300)
plt.show()