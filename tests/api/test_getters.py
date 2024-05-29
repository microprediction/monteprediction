

def test_get_correlation():
   from monteprediction import get_correlation
   corr = get_correlation()
   assert len(corr.columns)==11
