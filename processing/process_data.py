import pandas as pd
import numpy as np
import uproot
import sys


def convert_to_df(path, tree_name='DecayTree'):
    '''
    Convert both root files and pickled files to the correct form

    Inputs:
    path (str)      - Path to root or pkl file, including file name
    tree_name (str) - Name of tree name in root file, defaults to DecayTree

    Outputs:
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


def extract_constraints(variables, constraints):
    '''
    Function to convert variables and constraint lists into usable form

    Inputs:
    variables (list)   - list of variables passed by user
    constraints (list) - list of constraints passed by user

    Outputs:
    new_vars (list)    - list of variables and constraints to be plotted
                         (will contain some that may not be in the data)
    '''
    new_vars = variables.copy()
    for variable in variables:
        for constraint in constraints:
            new_vars.append(constraint + f'#{variable}')
    return new_vars
    

def exclude_constraints(df, exclude):
    '''
    Function to remove un-needed branches from dataframe, to declutter plot 
    and speed up plotting

    Inputs:
    df (DataFrame) - Dataframe to be plotted
    exclude (list) - List of constraints or branch tags to exclude from plot

    Outputs:
    df (DataFrame) - Trimmed down dataframe, no longer containing unrequired branches   
    '''
    print(f'Excluding the tags: {exclude}')
    for tag in exclude:
        df = df.filter(regex=f'^((?!_{tag}_).)*$')
    return df


def get_masscomb():
    '''
    Function to obtain mass combinations for multiple particles
    '''
    pass