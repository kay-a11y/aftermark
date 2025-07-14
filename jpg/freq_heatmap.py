from aftermark.utils.path import project_path
from PIL import Image
from scipy.fftpack import dct
import matplotlib.pyplot as plt
import numpy as np

img = Image.open(project_path("demo", "cat.jpg")).convert("YCbCr")
y_channel = np.array(img)[:, :, 0]

h, w = y_channel.shape
h_pad = (8 - h % 8) % 8
w_pad = (8 - w % 8) % 8
y_padded = np.pad(y_channel, ((0, h_pad), (0, w_pad)), mode='constant')

Q = np.array([
    [16,11,10,16,24,40,51,61],
    [12,12,14,19,26,58,60,55],
    [14,13,16,24,40,57,69,56],
    [14,17,22,29,51,87,80,62],
    [18,22,37,56,68,109,103,77],
    [24,35,55,64,81,104,113,92],
    [49,64,78,87,103,121,120,101],
    [72,92,95,98,112,100,103,99]
])

def block_process(channel, Q):
    h, w = channel.shape
    blocks = []

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            block = channel[i:i+8, j:j+8].astype(np.float32) - 128
            dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
            quantized = np.round(dct_block / Q)
            blocks.append(quantized)

    return blocks

blocks = block_process(y_padded, Q)

BG = "#bac0adff"

fig, axs = plt.subplots(8, 8, figsize=(10, 10), facecolor=BG)

for idx, ax in enumerate(axs.flat):
    ax.matshow(blocks[idx], cmap="seismic", vmin=-100, vmax=100)
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.set_title(f'B{idx}', fontsize=8)

plt.suptitle("DCT Coefficients (Quantized) - Y Channel", fontsize=14)
plt.tight_layout()

plt.savefig(
    project_path("artifacts", "jpg", "freq_heatmaps.png"),
    facecolor=BG,
    bbox_inches='tight',
    pad_inches=0.1,
    dpi=300,
)

# plt.show()
