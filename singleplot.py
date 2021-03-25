import matplotlib.pyplot as plt
import numpy as np

class Histogram:
    '''A single histogram for the HoliRoot'''
    def __init__(self, df, data, bins, cm, histrange):
        self.data = data
        self.bins = bins
        self.histrange = histrange
        self.cm = cm
        self.df = df

    def get_properties(df):
        '''
        Function to get properties from the column of a pandas dataframe

        Inputs: df(dataframe) - column of root dataframe to be plotted here

        Outputs: v_type(str) - variable type
                 particle(str) - particle name
                 data(array) - array of the actual data to be plotted
        '''
        df_name = df.name.split('_')
        data = df.to_numpy()
        if len(df_name) == 2:
            v_type = df_name[1]
            particle = df_name[0]
        else:
            v_type = df_name[-1]
            particle = df.name[:-(len(v_type)+1)]

        return v_type, particle, data

    def get_range(data):
        '''
        Function to get range of data
        
        Inputs: data(array) - data to be plotted in histogram
        
        Outputs: hist_range(tuple) - min and max values of data histogram
        '''
        hist_min = np.min(data)
        hist_max = np.max(data)
        hist_range = (hist_min, hist_max)
        return hist_range

    def plot(data, histrange, bins=50, cm='winter'):
        '''
        Function to produce a colour-mapped histogram

        Inputs: data(array) - data to be plotted in histogram
                histrange(tuple) - min and max vals of histogram, returned from get_range func
                bins(int) - Number of histogram bins
                cm(string) - name of colour map, choices to be outlined in main script

        Outputs: ax(axarr) - 2-sided axis array with histogram plotted on 
        '''
        cmap = plt.cm.get_cmap(cm)

        fig, ax = plt.subplots(ncols=1, nrows=2, figsize=(16, 4), sharex=True)
        n, _, patches = ax[0].hist(data, bins, density=True)
        _, _, patches2 = ax[1].hist(data, bins, density=True)
        col = (n - n.min()) / (n.max() - n.min())
        for c, p, p2 in zip(col, patches, patches2):
            plt.setp(p, 'facecolor', cmap(c))
            plt.setp(p2, 'facecolor', cmap(c))
        
        ax[1].invert_yaxis()
        plt.subplots_adjust(hspace=0)
        for a in ax:
            a.get_yaxis().set_visible(False)
            a.get_xaxis().set_visible(False)
            a.spines['right'].set_visible(False)
            a.spines['left'].set_visible(False)

        ax[0].spines['top'].set_visible(False)
        ax[1].spines['bottom'].set_visible(False)
        return ax

