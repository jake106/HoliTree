import pandas as pd
import numpy as np
import uproot
import sys
import re
from utils.multiplot import separate_vars


def assess_cuts(cuts):
    '''
    Ensures cuts are provided in correct format

    Inputs:
    cuts (dict) - dictionary defining any cuts to be placed on data
    '''
    for cut in cuts:
        print(f'Assessing {cut}')
        cut_dict = cuts[cut]
        assert 'type' in cut_dict.keys(), ('Type of cut must be defined')
        assert 'var' in cut_dict.keys(), ('What variable are we cuttting on?')
        if cut_dict['type'] == 'veto':
            assert len(cut_dict['region'].split(',')) == 2, ('region must have 2 values')
        elif cut_dict['type'] == 'min' or 'max':
            assert 'value' in cut_dict.keys(), ('Must define minimum/maximum value')


def apply_cuts(df, cuts, tags):
    '''
    Applies cuts to branches and creates a new 
    tag for cut-tagged variables

    Inputs:
    df (DataFrame) - dataframe to apply cuts to
    cuts (dict)    - dictionary defining cuts
    tags (list)    - list of tags

    Outputs:
    dfn (DataFrame) - Dataframe with added tags including cuts
    new_tags (list) - list of new tags for cut branches
    '''
    dfn = df.copy()
    for cut in cuts:
        df_cut = df.copy()
        print(f'Applying {cut}')
        cut_dict = cuts[cut]
        # Handle vetos
        if cut_dict['type'] == 'veto':
            lower, upper = cut_dict['region'].split(',')
            veto_var = cut_dict['var']
            veto = np.all([float(lower) < df_cut[veto_var], df_cut[veto_var] < float(upper)], axis=0)
            df_cut = df_cut[~veto]
        # Handle min cuts
        elif cut_dict['type'] == 'min':
            lower = cut_dict['value']
            min_var = cut_dict['var']
            df_cut = df_cut[float(lower) < df_cut[min_var]]
        # Handle max cuts
        elif cut_dict['type'] == 'max':
            upper = cut_dict['value']
            max_var = cut_dict['var']
            df_cut = df_cut[df_cut[max_var] < float(upper)]
        # Add to df and tags
        if len(df_cut) == 0:
            print(f'No events left after {cut}')
            continue
        df_cut = df_cut.add_prefix(f'{cut}_')
        dfn = dfn.append(df_cut, ignore_index=True)
    new_tags = [*cuts]
    if tags:
        for tag in tags:
            cut_tags = [f'{cut}_{tag}' for cut in cuts]
            new_tags += [tag] + cut_tags
    print('Constructed cuts')
    return dfn, new_tags


def inv_mass(data, particles, energy_label = None):
    '''
    Calculates invariant mass of particle

    Inputs:
    data (DataFrame) - dataframe containing particle data
    particles (list) - list of particles to construct mass for

    Outputs:
    mass (array)     - result of invariant mass calculation
    '''
    if energy_label is not None:
        en = energy_label
    else:
        en = 'PE'
    mat = np.zeros([len(data.index), 4])
    for particle in particles:
        mat += np.array(data[['{}_{}'.format(particle, en), '{}_PX'.format(particle), '{}_PY'.format(particle), '{}_PZ'.format(particle)]])

    mm = mat[:, 0]**2 - (mat[:, 1:]**2).sum(axis = 1)
    return np.sqrt(mm)


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
    new_vars = []
    for variable in variables:
        new_vars.append(variable)
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
