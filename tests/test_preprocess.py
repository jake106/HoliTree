import pytest
from preprocess import make_kinematic_comb
import pandas as pd 

@pytest.mark.parametrize('df, out_names, combinations, tags, expected',
[
    (pd.DataFrame({'_foo_': range(5), '_bar_':range(5, 10)}), ['bar'], pd.DataFrame({'_foo_': range(5)}), 
    , ['D0', 'foo', 'bar'], {'D0': ['foo', 'bar']}, )
])
def test_make_comb(df, out_names, combinations, tags, expected):
    output = make_kinematic_comb(df, out_names, combinations, tags)
    assert output == expected