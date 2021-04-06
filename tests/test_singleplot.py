import numpy as np
from plotting.singleplot import Histogram
from plotting.multiplot import separate_vars
import pytest
import pandas as pd

test_df = pd.read_pickle('~/Documents/B0DDKana/DstDK_randompion/16/DstDK_randompion_tis_df.pkl')
testdf1 = test_df['B0_M']
testdf2 = test_df['B0_OnlyD_nPV']
testdf3 = test_df['B0_OnlyB_Kst_892_0_PERR']

@pytest.mark.parametrize('data, expected', [
    (pd.Series(data=[1.0, 4.0, 6.0, 7.0], name='m'), (1.0, 7.0)),
    (pd.Series([-44.0, 999.0, 0.45], name='n'), (-44.0, 999.0))])
def test_range(data, expected):
    hist = Histogram(df=data)
    output = hist.get_range()
    assert output == expected

@pytest.mark.parametrize('testdf, expected', [
    (testdf1, ['B0', 'M']), (testdf2, ['B0_OnlyD', 'nPV']), (testdf3, ['B0_OnlyB_Kst_892_0', 'PERR'])])
def test_properties(testdf, expected):
    hist = Histogram(testdf)
    v_type, particle, data = hist.get_properties()
    assert [particle, v_type] == expected
