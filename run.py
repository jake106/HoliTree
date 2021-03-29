import numpy as np
import matplotlib.pyplot as plt
from singleplot import Histogram
import pandas as pd


def multiplot(df, variables):
    accepted_cmaps = ['spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'copper']
    cmaps_to_plot = accepted_cmaps[:len(variables)]
    for var, cmap in zip(variables, cmaps_to_plot):
        this_df = df.filter(regex=f'_{var}$')
        same_var_plot(this_df, var, cmap)



def same_var_plot(df, var_type, cmap):
    plot_len = len(df.columns)
    i = 0
    fig, ax = plt.subplots(nrows=2*plot_len, ncols=1, sharex=True, figsize=(24, 2*plot_len))
    fig.suptitle(var_type, fontsize=16, y=0.504, x=0.08)
    for col in df.columns:
        this_df = df[col]
        hist = Histogram(this_df, cmap)
        hist.plot(ax=ax[i:i+2])
        i += 2
    ax[-1].get_xaxis().set_visible(True)
    ax[-1].spines['bottom'].set_visible(True)
    fig.savefig(f'./testfig_{var_type}.jpeg', bbox_inches='tight')


test_df = pd.read_pickle('~/Documents/B0DDKana/DstDK_randompion/16/DstDK_randompion_tis_df.pkl')

multiplot(test_df, ['M', 'PT'])
#hist = Histogram(test_M)
#ax = hist.plot()

#plt.savefig('./testfig2.jpeg')

