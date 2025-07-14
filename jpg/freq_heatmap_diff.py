from aftermark.utils.path import project_path
from PIL import Image
from scipy.fftpack import dct
import numpy as np
import matplotlib.pyplot as plt

img = Image.open(project_path("demo", "cat.jpg")).convert("YCbCr")
y_channel = np.array(img)[:, :, 0]

h, w = y_channel.shape
h_pad = (8 - h % 8) % 8
w_pad = (8 - w % 8) % 8
y_padded = np.pad(y_channel, ((0, h_pad), (0, w_pad)), mode='constant')

blocks = []
for i in range(0, y_padded.shape[0], 8):
    for j in range(0, y_padded.shape[1], 8):
        block = y_padded[i:i+8, j:j+8].astype(np.float32) - 128
        blocks.append(block)

Q_base = np.ones((8, 8)) * 16
Q_strong = np.ones((8, 8)) * 50
Q_weak = np.ones((8, 8)) * 5
matrices = {"Base Q": Q_base, "Strong Q (lossy)": Q_strong, "Weak Q (clear)": Q_weak}

def process_blocks(blocks, Q):
    result_blocks = []
    for block in blocks[:64]: 
        dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
        quantized = np.round(dct_block / Q)
        result_blocks.append(quantized)
    return result_blocks

BG = "#bac0adff"

fig, axs = plt.subplots(3, 8, figsize=(14, 8), facecolor=BG)

for row, (title, Q) in enumerate(matrices.items()):
    q_blocks = process_blocks(blocks, Q)
    for col in range(8):
        axs[row, col].matshow(q_blocks[col], cmap="seismic", vmin=-100, vmax=100)
        axs[row, col].set_title(f'{title}' if col == 0 else "")
        axs[row, col].axis("off")

plt.tight_layout()

plt.savefig(
    project_path("artifacts", "jpg", "freq_heatmaps_diff.png"),
    facecolor=BG,
    bbox_inches='tight',
    pad_inches=0.1,
    dpi=300,
)

# plt.show()
