import pandas as pd
import numpy as np

def merge_pkl(what_data, dftag=False):
    if dftag:
        end = 'df'
    else:
        end = 'weights'
    years = [16, 17, 18, 1112]
    df = pd.DataFrame({})
    for year in years:
        print(f'Merging {year}')
        tis_df = pd.read_pickle(f'./{year}/MC_phsp_tis_noddkveto_{end}.pkl')
        tos_df = pd.read_pickle(f'./{year}/MC_phsp_tos_noddkveto_{end}.pkl')
        df = df.append([tis_df, tos_df])
        print(len(df['B0_M']))
    df.to_pickle(f'./{what_data}_combined.pkl')



#merge_pkl('DstDK_randompion', True)

def tag(path, label):
    '''
    path1 must point to untagged file
    '''
    df = pd.read_pickle(path)
    print(f'Adding prefix {label}')
    dfn = df.add_prefix(f'{label}_')
    print('Saving')
    dfn.to_pickle('./data_vis_plot.pkl')

merge_pkl('noddkveto')
