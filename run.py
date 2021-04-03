import numpy as np
import matplotlib.pyplot as plt
from singleplot import Histogram
from process_data import convert_to_df
import pandas as pd
import argparse
import os
from PIL import Image


def multiplot(df, variables):
    accepted_cmaps = ['spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'copper']
    cmaps_to_plot = accepted_cmaps[:len(variables)]
    ax_array = np.empty_like(variables, dtype=object)
    for n, (var, cmap) in enumerate(zip(variables, cmaps_to_plot)):
        print(f'Plotting {var}')
        this_df = df.filter(regex=f'_{var}$')
        same_var_plot(this_df, var, cmap)
    print('Plotting done, beginning stich')
    temp_ims = os.listdir('./temp/')
    ims = [f'./temp/{x}' for x in temp_ims]
    plots = [Image.open(x) for x in ims]
    widths, heights = zip(*(i.size for i in plots))
    total_width = min(widths)
    total_height = sum(heights)
    final_im = Image.new('RGB', (total_width, total_height), color=(255,255,255))
    y_offset=0
    for plot in plots:
        width, height = plot.size
        if width > total_width:
            plot = plot.crop(((width-total_width), 0, width, height))
        final_im.paste(plot, (0, y_offset))
        y_offset += plot.size[1] + 5
    print('Done!')
    final_im.save('test.jpeg')



def same_var_plot(df, var_type, cmap):
    plot_len = len(df.columns)
    i = 0
    fig, ax = plt.subplots(nrows=2*plot_len, ncols=1, sharex=True, figsize=(24, plot_len))
    fig.suptitle(var_type, fontsize=16, y=0.504, x=0.08)
    for col in df.columns:
        this_df = df[col]
        hist = Histogram(this_df, cmap)
        hist.plot(ax=ax[i:i+2])
        i += 2
    ax[-1].tick_params(axis='x', labelsize=14)
    ax[-1].get_xaxis().set_visible(True)
    ax[-1].spines['bottom'].set_visible(True)
    fig.savefig(f'./temp/temp_{var_type}.jpeg', bbox_inches='tight')


test_df = convert_to_df('~/Documents/B0DDKana/DstDK_randompion/16/DstDK_randompion_tis_df.pkl')
multiplot(test_df, ['MM', 'PT'])


