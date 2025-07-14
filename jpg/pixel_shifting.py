import numpy as np

block = np.array([[100, 120], [130, 140]])
print("Original block:\n", block)

shifted = block.astype(np.float32) - 128
print("Shifted block:\n", shifted)
