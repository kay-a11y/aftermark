from aftermark.utils.path import project_path
import matplotlib.pyplot as plt

BG = "#6a6d65ff"
plt.style.use('dark_background')

maps = sorted(m for m in plt.colormaps() if not m.endswith("_r"))
fig, axs = plt.subplots(len(maps)//4, 4, figsize=(12, 30), facecolor=BG)
for ax, cmap in zip(axs.ravel(), maps):
    gradient = [list(range(256))]
    ax.imshow(gradient, aspect='auto', cmap=cmap)
    ax.set_title(cmap, fontsize=8, pad=8, color='white')
    ax.axis('off')

plt.tight_layout()
plt.subplots_adjust(top=0.97, hspace=1)

plt.savefig(
    project_path("artifacts", "jpg", "theme.png"),
    facecolor=BG,
    bbox_inches='tight',
    pad_inches=0.1,
    dpi=300,
)

# plt.show()