
from monteprediction import KERNEL_RATE
import numpy as np


def compute_score(full_samples, z_full, weights, a=KERNEL_RATE):

    def _compute_score(samples, z, a=KERNEL_RATE):
        distances = np.linalg.norm(samples - z, axis=1)
        return np.sum(np.exp(-a * distances))
    
    num_dimensions = full_samples.shape[1]
    scores = []
    
    # Compute scores for each 10-dimensional subset by excluding one dimension
    for i in range(num_dimensions):
        # Create a subset by excluding the i-th dimension
        subset_samples = np.delete(full_samples, i, axis=1)
        subset_z = np.delete(z_full, i)
        score = _compute_score(subset_samples, subset_z, a)
        scores.append(score)
    
    # Weighted average of the scores from the 10-dimensional subsets
    weighted_average = np.average(scores, weights=weights)
    
    # Score from the full 11-dimensional set
    score_11d = compute_score(full_samples, z_full, a)
    
    # Total score: weighted average of 10D scores + score from 11D
    total_score = weighted_average + score_11d
    return total_score
