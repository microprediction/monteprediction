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
    


def test_compute_score_with_known_values():
    # Controlled small dataset and known z for exact calculation verification
    samples = np.array([[0, 0], [3, 4]])  # 2 samples in 2D for simplicity in manual calculation
    z = np.array([0, 0])
    sub_weight = 0.5
    a = 1.0  # Simplified rate for easier calculation

    # Manually compute expected scores
    # Distance from [0,0] to [0,0] is 0, exp(-1*0) = 1
    # Distance from [0,0] to [3,4] is 5, exp(-1*5) = approx 0.0067
    expected_scores = np.array([1, np.exp(-5)])
    expected_weighted_average = sub_weight * np.average(expected_scores)
    expected_full_score = np.exp(-0) + np.exp(-5)  # Simplified to 1D case for both points
    expected_total = expected_weighted_average + expected_full_score

    # Actual test execution
    result = compute_score(samples, z, sub_weight, a)

    # Check against the expected total score
    np.testing.assert_almost_equal(result, expected_total, decimal=5,err_msg="The computed total score does not match the expected value.")



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
