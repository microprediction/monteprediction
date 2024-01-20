from monteprediction import KERNEL_RATE
import numpy as np


def compute_score(samples, z, a=KERNEL_RATE):
    distances = np.linalg.norm(samples - z, axis=1)
    return np.sum(np.exp(-a * distances))