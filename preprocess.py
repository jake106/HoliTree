import numpy as np
import pandas as pd
from utils.process_data import convert_to_df, inv_mass


def select_branches(df, out_names, combinations, tagged_names, untagged_names, tags):
    '''
    '''
    final_branches = out_names + [f'{tag}{out}' for tag in tags for out in out_names]
    momenta = ['PX', 'PY', 'PZ', 'PE']
    for comb in combinations:
        for tag in tags:
            daughters = [f'{tag}{daughter}' for daughter in combinations[comb]]
            for mom in momenta:
                daughter_mom = [f'{daughter}_{mom}' for daughter in daughters]
                df[f'{tag}{comb}_{mom}'] = df[daughter_mom].sum(axis=1)
    print('combinations constructed')
    




df = convert_to_df('./DstDK_randompion_tis_df.pkl')
out_names = ['D0', 'D0bar', 'K', 'Pi']
combinations = {'D0': ['D0_Kplus', 'D0_piplus'], 
                'D0bar': ['D00_Kplus', 'D00_piplus']}
tagged_names = {'K': 'Kst_892_0_Kplus', 
                'Pi': 'Kst_892_0_piplus'}
untagged_names = {'K': 'K_Kst0', 
                  'Pi': 'Pi_Kst0',
                  'D0': 'D0', 
                  'D0bar': 'D0bar'}
tags = ['B0_OnlyD_', 'B0_BandDs_']

select_branches(df, out_names, combinations, tagged_names, untagged_names, tags)