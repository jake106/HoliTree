import pandas as pd
import numpy as np
import os
from PIL import Image
from utils.singleplot import Histogram, same_var_plot


def separate_vars(variable, df, constraint_list):
    '''
    Function to extract desired data from dataframe, and return axis labels

    Inputs: variable (str)         - name of variable to be plotted
            df (DataFrame)         - data to be plotted
            constraint_list (list) - list of constraints to not plot multiple times
    
    Outputs: this_df (DataFrame)   - Trimmed dataframe containing only what needs to be plotted
             var (str)             - Variable name without any constraint label
             unit (str)            - Unit of measurement for x axis
    '''
    var, unit = variable.split('*')
    if '#' in var:
        constraint, var2 = var.split('#')
        this_df = df.filter(regex=f'{constraint}(.*)_{var2}$')
        if len(this_df.columns) == 0:
            return 'noconst', 'noconst', unit
        print(f'Constraint {constraint} found in {var2}, plotting seperately')
        var = f'{constraint}_{var2}'
        this_df.columns = this_df.columns.str.replace(f'{constraint}_', '')
    else:
        print(f'Plotting {var} in {unit}')
        this_df = df.filter(regex=f'_{var}$')
    for constraint in constraint_list:
        this_df = this_df.filter(regex=f'^((?!{constraint}).)*$')
    return this_df, var, unit



def multiplot(df, variables, onlyconst):
    '''
    Function to manage plotting of multiple variables

    Inputs: df (DataFrame)     - Dataframe of file to be plotted
            variables (list)   - list of variables (str) to plot, separated from unit
                                 by '*' 
            onlyconst (bool)   - flag to switch off automatic plotting of un-tagged branches
                                 not in "exclude"

    Outputs: Saves HoliTree plot as jpeg file

    '''
    fname = 'HoliTree'
    constraint_list = [variable.split('#')[0] for variable in variables if '#' in variable]

    # Add function to recursively update cmaps
    accepted_cmaps = ['spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'copper']
    cmaps_to_plot = accepted_cmaps[:len(variables)]
    
    prev_var = ''
    i=0
    for var in variables:
        if onlyconst and (not '#' in var):
            continue
        this_df, var, unit = separate_vars(var, df, constraint_list)
        if var == 'noconst':
            continue
        fname += f'_{var}'
        if i == len(accepted_cmaps):
            i = 0
        cmap = accepted_cmaps[i]
        i += 1
        if var.split('_')[-1] == prev_var.split('_')[-1]:
            ax = axn
            axn = same_var_plot(this_df, var, unit, cmap, ax)
        else:
            axn = same_var_plot(this_df, var, unit, cmap, False)
        prev_var = var
    print('Plotting done, beginning stich.')
    temp_ims = sorted(os.listdir('./temp/'))
    ims = [f'./temp/{x}' for x in temp_ims]
    plots = [Image.open(x) for x in ims]
    widths, heights = zip(*(i.size for i in plots))
    total_width = min(widths)
    total_height = sum(heights)+25
    final_im = Image.new('RGB', (total_width, total_height), color=(255,255,255))
    y_offset=5
    for plot in plots:
        width, height = plot.size
        if width > total_width:
            plot = plot.crop(((width-total_width), 0, width, height))
        final_im.paste(plot, (0, y_offset))
        y_offset += plot.size[1] + 5
    print('Stitching complete, saving and clearing temp files')
    final_im.save(f'{fname}.pdf')
    for x in temp_ims:
        os.remove(f'./temp/{x}')
    print(f'Complete, output saved as: {fname}.pdf')

