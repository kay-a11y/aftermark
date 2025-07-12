from aftermark.utils.path import project_path
import matplotlib.pyplot as plt
import numpy as np

cat_qtable1 = [
    1, 1, 1, 2, 3, 4, 5, 6,
    1, 1, 1, 2, 3, 4, 5, 6,
    1, 1, 2, 3, 4, 5, 6, 7,
    2, 2, 3, 4, 5, 6, 7, 8,
    3, 3, 4, 5, 6, 7, 8, 9,
    4, 4, 5, 6, 7, 8, 9, 9,
    5, 5, 6, 7, 8, 9, 9, 9,
    6, 6, 7, 8, 9, 9, 9, 9
]

cat_qtable2 = [
    1, 1, 2, 4, 9, 9, 9, 9, 
    1, 2, 2, 6, 9, 9, 9, 9, 
    2, 2, 5, 9, 9, 9, 9, 9,  
    4, 6, 9, 9, 9, 9, 9, 9, 
    9, 9, 9, 9, 9, 9, 9, 9, 
    9, 9, 9, 9, 9, 9, 9, 9,  
    9, 9, 9, 9, 9, 9, 9, 9, 
    9, 9, 9, 9, 9, 9, 9, 9
]

mat1 = np.array(cat_qtable1).reshape((8, 8))
mat2 = np.array(cat_qtable2).reshape((8, 8))

BG = "#0b0f13"

fig, axes = plt.subplots(1, 2, figsize=(12, 5), facecolor=BG)

im1 = axes[0].imshow(mat1, cmap='viridis')
axes[0].set_title('QTable #0 (Luma)')
axes[0].axis('off')
fig.colorbar(im1, ax=axes[0], fraction=0.046, pad=0.04)

im2 = axes[1].imshow(mat2, cmap='viridis')
axes[1].set_title('QTable #1 (Chroma)')
axes[1].axis('off')
fig.colorbar(im2, ax=axes[1], fraction=0.046, pad=0.04)

for i in range(8):
    for j in range(8):
        axes[0].text(j, i, str(mat1[i, j]), ha='center', va='center', color='black', fontsize=8)
        axes[1].text(j, i, str(mat2[i, j]), ha='center', va='center', color='black', fontsize=8)

fig.suptitle('Quantization Matrices', color='w')
plt.tight_layout()

plt.savefig(
    project_path("artifacts", "jpg", "qtables.png"),
    facecolor=BG,
    bbox_inches='tight',
    pad_inches=0.1,
    dpi=300,
)

plt.show()
