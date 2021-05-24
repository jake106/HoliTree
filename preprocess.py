import numpy as np
import pandas as pd
from utils.process_data import convert_to_df, inv_mass
import itertools
import argparse


def make_kinematic_comb(df, combinations, tags=False):
    '''
    Function to add branches with kinematics of composite particles to dataframe

    Input:
    df (DataFrame)      - pandas dataframe to add composites to 
    combinations (dict) - dictionary with composite particle names as keys (must be output
                          branch names). Entries correspond to branch names of daughter 
                          particles
    tags (list)         - list of names of tagged branches (default=False (no tags))

    Output:
    df (DataFrame)      - pandas dataframe with added composites 
    '''
    # Construct composites
    momenta = ['PX', 'PY', 'PZ', 'PE']
    # Tagged composites
    for comb in combinations:
        if tags:
            for tag in tags:
                daughters = [f'{tag}_{daughter}' for daughter in combinations[comb]]
                for mom in momenta:
                    daughter_mom = [f'{daughter}_{mom}' for daughter in daughters]
                    df[f'{tag}_{comb}_{mom}'] = df[daughter_mom].sum(axis=1)
        else:
            for mom in momenta:
                daughter_mom = [f'{daughter}_{mom}' for daughter in combinations[comb]]
                df[f'{comb}_{mom}'] = df[daughter_mom].sum(axis=1)
    print('Composite particles constructed')
    return df


def trim_down(df, untagged_names, tagged_names, tags ,combinations, additional_vars):
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
    if tags:
        if not tagged_names:
            print('No tagged names provided, assuming these are the same as untagged names.')
            tagged_names = untagged_names
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
    Function to add mass combinations to tuple

    Inputs:
    df (DataFrame)        - dataframe to add mass combinations to
    particle_names (list) - list of plotting names for particles from
                            untagged branches dictionary
    tags (list)           - list of tagged branches

    Outputs:
    df (DataFrame)        - dataframe with added mass combs
    '''
    # Construct branches
    branches = []
    # add non-combined mass branches
    for m in particle_names:
        df[f'{m}_M'] = inv_mass(df, [m])
    if tags:
        for const in tags:
            for m in particle_names:
                df[f'{const}_{m}_M'] = inv_mass(df, [m])
    for i in range(2, len(particle_names)):
        branches += list(itertools.combinations(particle_names, i))
    # Add masses for these branches to df
    for branch in branches:
        n = ''.join(branch)
        df[f'{n}_M'] = inv_mass(df, list(branch))
        if tags:
            for const in tags:
                const_branch = [f'{const}_' + x for x in list(branch)]
                df[f'{const}_{n}_M'] = inv_mass(df, list(const_branch))
    print('Mass combinations added:' + '\n')
    for branch in branches:
        print(''.join(branch))
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
    parser.add_argument('--tagged_names', action='store_true',
                        help='Names of output branches and tuple branches for untagged particles')
    parser.add_argument('--tags', action='store_true',
                        help='Names of tags used for pre-tagged branches')
    parser.add_argument('--composites', action='store_true',
                         help='Dict describing composite particles')
    parser.add_argument('--additional_vars', action='store_true',
                        help='Define list of additional non-kinematic variables to plot')
    args = parser.parse_args()

    path = args.path
    untagged_names = args.untagged_names
    tagged_names = args.tagged_names
    combinations = args.composites
    tags = args.tags
    additional_vars = args.additional_vars

    df = convert_to_df(path)
    dfn = trim_down(df, untagged_names, tagged_names, tags, combinations, additional_vars)
    # * in list allows itertools to make combinations from dictionary keys
    dfm = add_mass_comb(dfn, [*untagged_names], tags)
    dfm.to_pickle('./processed_data/MC_noddkveto.pkl')
