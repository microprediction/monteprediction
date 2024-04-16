import numpy as np
import pytest
from monteprediction import KERNEL_RATE
from monteprediction.scoring import compute_score  

def test_compute_score():
    # Create a dummy 11-dimensional dataset with 5 samples
    np.random.seed(0)  # for reproducibility
    samples = np.random.rand(5, 11)
    z = np.random.rand(11)
    
    # Set the subsample weight and KERNEL_RATE manually for testing
    sub_weight = 0.5
    a = KERNEL_RATE
    
    # Expected values need to be calculated based on the implementation details
    # For now, we will check the execution and type of return
    result = compute_score(samples, z, sub_weight, a)
    
    # Check if the result is a float, as expected
    assert isinstance(result, float), "The function should return a float value representing the total score."
    


