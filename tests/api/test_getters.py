

def test_get_correlation():
   from monteprediction.api import get_correlation
   corr = get_correlation()
   assert len(corr.columns)==11
