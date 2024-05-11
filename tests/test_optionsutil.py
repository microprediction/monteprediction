
from monteprediction.optionsutil import get_weekly_options

def test_weekly_options():
    df = get_weekly_options()
    assert(len(df.index)>5)
