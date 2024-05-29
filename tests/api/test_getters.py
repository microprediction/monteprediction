

def test_get_correlation():
   from monteprediction.api import get_correlation
   corr = get_correlation(expiry='2024-05-13')
   assert len(corr.columns)==11
