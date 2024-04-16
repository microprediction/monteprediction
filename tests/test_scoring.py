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
    


def test_empty_samples():
    # Empty dataset should handle gracefully or raise a meaningful error
    samples = np.array([]).reshape(0, 11)  # No samples, 11 features
    z = np.zeros(11)
    sub_weight = 0.5
    a = 1.0

    with pytest.raises(ValueError):
        compute_score(samples, z, sub_weight, a)

def test_invalid_weights():
    # Invalid sub_weight should raise an error or produce a predictable result
    samples = np.random.rand(5, 11)
    z = np.random.rand(11)
    sub_weight = -1  # Negative weight, which is not sensible
    a = 1.0

    with pytest.raises(ValueError):
        compute_score(samples, z, sub_weight, a)
