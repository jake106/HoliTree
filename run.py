import numpy as np
import matplotlib.pyplot as plt
from singleplot import Histogram
import pandas as pd

test_df = pd.read_pickle('~/Documents/B0DDKana/DstDK_randompion/16/DstDK_randompion_tis_df.pkl')
test_M = test_df['B0_M']

v_type, particle, test_data = Histogram.get_properties(test_M)
print(v_type, particle)
histrange = Histogram.get_range(test_data)
ax = Histogram.plot(test_data, histrange)

plt.savefig('./testfig.jpeg')

