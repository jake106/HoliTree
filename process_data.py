import pandas as pd
import numpy as np
import uproot
import sys


def convert_to_df(path, tree_name='DecayTree'):
    '''
    Convert both root files and pickled files to the correct form

    Inputs:
    path (str)      - Path to root or pkl file, including file name
    tree_name (str) - Name of tree name in root file, defults to DecayTree

    Returns:
    df (dataframe)  - File from "path" input in pandas DataFrame form
    '''
    if path[-4:] == 'root':
        print('Converting root file to DataFrame')
        tree = uproot.open(path)[tree_name]
        df = tree.pandas.df()
    elif path[-3:] == 'pkl':
        print('Converting pkl file to DataFrame')
        df = pd.read_pickle(path)
    else:
        print('No valid file found, check path and file name')
        sys.exit()
    return df



#convert_to_df('mfgsafasfwefem.root')
