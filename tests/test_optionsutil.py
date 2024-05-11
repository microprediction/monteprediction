
from monteprediction.optionsutil import get_weekly_options, get_weekly_implied

def test_weekly_options():
    df = get_weekly_options()
    assert(len(df.index)>5)


def test_weekly_implied():
    d = get_weekly_implied()
    assert 'XLB' in d


