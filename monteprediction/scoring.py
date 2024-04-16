
from monteprediction import KERNEL_RATE
import numpy as np


def compute_score(samples, z, sub_weight=0.5, a=KERNEL_RATE):

    def _compute_score(subsamples, subset_z, a=KERNEL_RATE):
        distances = np.linalg.norm(subsamples - subset_z, axis=1)
        return np.sum(np.exp(-a * distances))
    
    num_dimensions = samples.shape[1]
    scores = []
    
    # Compute scores for each 10-dimensional subset by excluding one dimension
    for i in range(num_dimensions):
        # Create a subset by excluding the i-th dimension
        subset_samples = np.delete(samples, i, axis=1)
        subset_z = np.delete(z, i)
        score = _compute_score(subset_samples, subset_z, a)
        scores.append(score)
    
    # Weighted average of the scores from the 10-dimensional subsets
    weighted_average = sub_weight*np.average(scores)
    
    # Score from the full 11-dimensional set
    score_11d = _compute_score(samples, z, a)
    
    # Total score: weighted average of 10D scores + score from 11D
    total_score = weighted_average + score_11d
    return total_score
