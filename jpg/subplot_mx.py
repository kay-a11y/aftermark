import matplotlib.pyplot as plt
import numpy as np

fig, axs = plt.subplots(2, 2, figsize=(8, 8))
for i in range(2):
    for j in range(2):
        axs[i, j].imshow(np.random.rand(8, 8), cmap="gray")
        axs[i, j].set_title(f"Plot {i},{j}")
plt.tight_layout()
plt.show()
