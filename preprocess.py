import numpy as np
import pandas as pd
from utils.process_data import convert_to_df, inv_mass
import itertools
import argparse


def make_kinematic_comb(df, combinations, tags):
    '''
    Function to add branches with kinematics of composite particles to dataframe

    Input:
    df (DataFrame)      - pandas dataframe to add composites to 
    combinations (dict) - dictionary with composite particle names as keys (must be output
                          branch names). Entries correspond to branch names of daughter 
                          particles
    tags (list)         - list of names of tagged branches (untagged branches assumed to already
                          have composites)

    Output:
    df (DataFrame)      - pandas dataframe with added composites 
    '''
    # Construct composites
    momenta = ['PX', 'PY', 'PZ', 'PE']
    # Tagged composites
    for comb in combinations:
        for tag in tags:
            daughters = [f'{tag}_{daughter}' for daughter in combinations[comb]]
            for mom in momenta:
                daughter_mom = [f'{daughter}_{mom}' for daughter in daughters]
                df[f'{tag}_{comb}_{mom}'] = df[daughter_mom].sum(axis=1)
    print('Composite particles constructed')
    return df


def trim_down(df, tags, untagged_names, tagged_names, combinations=False, additional_vars=False):
    '''
    Function to trim down data to only relevant branches

    Inputs:
    df (DataFrame)         - pandas dataframe to trim down
    tags (list)            - list of names of tagged branches
    untagged_names (dict)  - dictionary with keys as desired particle names, entries are names
                             of particles currently untagged 
    tagged_names (dict)    - dictionary with keys as desired particle names, entries are names
                             of particles currently tagged 
    combinations (dict)    - dictionary with composite particle names as keys (must be output
                             branch names). Entries correspond to branch names of daughter 
                             particles
    additional_vars (list) - list of non-kinematic varibles to keep in data

    Outputs:
    df_out (DataFrame)     - Pandas dataframe of new values, trimmed down with correct names 
    '''
    momenta = ['PX', 'PY', 'PZ', 'PE']
    # Trim down dataframe
    if combinations:
        df = make_kinematic_comb(df, combinations, tags)
    df_out = pd.DataFrame({})
    # Deal with untagged branches
    for nm in untagged_names:
        for mom in momenta:
            df_out[f'{nm}_{mom}'] = df[f'{untagged_names[nm]}_{mom}']
        if additional_vars:
            for variable in additional_vars:
                df_out[f'{nm}_{variable}'] = df[f'{untagged_names[nm]}_{variable}']
    # Deal with tagged branches
    for nm in tagged_names:
        for tag in tags:
            for mom in momenta:
                df_out[f'{tag}_{nm}_{mom}'] = df[f'{tag}_{tagged_names[nm]}_{mom}']
            if additional_vars:
                for variable in additional_vars:
                    df_out[f'{tag}_{nm}_{variable}'] = df[f'{tag}_{tagged_names[nm]}_{variable}']
    print('dataset trimmed')
    return df_out


def add_mass_comb(df, particle_names, tags):
    '''
    '''
    # Construct branches
    branches = []
    for i in range(2, len(particle_names)):
        branches += list(itertools.combinations(particle_names, i))
    # Add masses for these branches to df
    for branch in branches:
        n = ''.join(branch)
        df[f'{n}_M'] = inv_mass(df, list(branch))
        for const in tags:
            const_branch = [f'{const}_' + x for x in list(branch)]
            df[f'{const}_{n}_M'] = inv_mass(df, list(const_branch))
    print('Mass combinations added')
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Preprocess data tuples for use in HoliTree plot")
    parser.add_argument('-path', nargs='?', default='./DstDK_randompion_tis_df.pkl', 
                        help='Path to file to be plotted (.root or .pkl)')
    parser.add_argument('-untagged_names', default={'K': 'K_Kst0', 
                        'Pi': 'Pi_Kst0',
                        'D0': 'D0', 
                        'D0bar': 'D0bar'},
                        help='Names of output branches and tuple branches for untagged particles')
    parser.add_argument('-tagged_names', default={'K': 'Kst_892_0_Kplus', 
                        'Pi': 'Kst_892_0_piplus',
                        'D0' : 'D0',
                        'D0bar':'D0bar'},
                        help='Names of output branches and tuple branches for untagged particles')
    parser.add_argument('-tags', default=['B0_OnlyD', 'B0_BandDs'],
                        help='Names of tags used for tagged branches')
    parser.add_argument('-combinations', default={'D0': ['D0_Kplus', 'D0_piplus'], 
                        'D0bar': ['D00_Kplus', 'D00_piplus']},
                         help='Dict describing composite particles')
    args = parser.parse_args()

    path = args.path
    untagged_names = args.untagged_names
    tagged_names = args.tagged_names
    combinations = args.combinations
    tags = args.tags

    df = convert_to_df(path)
    dfn = trim_down(df, tags, untagged_names, tagged_names, combinations)
    dfm = add_mass_comb(dfn, [*tagged_names], tags)
    dfm.to_pickle('./processed_data/example.pkl')
