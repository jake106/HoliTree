import pandas as pd
import uproot
import numpy as np

df = pd.DataFrame({'foo': range(5), 'bar':range(5, 10)})

root_file = uproot.recreate('./root_file.root', compression=uproot.ZLIB(4))
branches = {'foo': np.int, 'bar': np.int}
root_file['DecayTree'] = uproot.newtree(branches, title='DecayTree')
root_file['DecayTree'].extend(df.to_dict('list'))

pkl_file = df.to_pickle('./pkl_file.pkl')
