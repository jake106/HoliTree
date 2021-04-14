import matplotlib.pyplot as plt
import numpy as np


def same_var_plot(df, var, unit, cmap):
    '''
    Function to plot a single variable of the HoliTree plot

    Inputs: df (DataFrame) - Dataframe of single variable to be plotted
            var (str)      - Name of variable for axis labelling
            unit (str)     - Unit of measurement var is in
            cmap (str)     - Name of colour map, taken from list in multiplot function

    Outputs: Saves temporary jpeg file to be used in multiplot function
    '''
    plot_len = len(df.columns)
    i = 0
    fig, ax = plt.subplots(nrows=2*plot_len, ncols=1, sharex=True, figsize=(24, plot_len))
    fig.suptitle(f'{var} / {unit}', fontsize=16, x=0.08, fontweight='bold',
                 y=0.54, rotation='vertical', verticalalignment='center')
    for col in df.columns:
        this_df = df[col]
        hist = Histogram(this_df, cmap)
        hist.plot(ax=ax[i:i+2])
        i += 2
    ax[-1].tick_params(axis='x', labelsize=14)
    ax[-1].get_xaxis().set_visible(True)
    ax[-1].spines['bottom'].set_visible(True)
    fig.savefig(f'./temp/temp_{var}.jpeg', bbox_inches='tight')


class Histogram:
    '''
    A single histogram for the HoliTree plot
    
    Initialisation requires only a pandas dataframe (single column),
    colourmap (str), and optional number of bins

    Call plot to get axes
    '''
    def __init__(self, df, cm='spring', bins=50):
        self.bins = bins
        self.df = df
        self.cm = cm
        self.v_type, self.particle, self.data = self.get_properties()
        self.hist_range = self.get_range()

    def get_properties(self):
        '''
        Function to get properties from the column of a pandas dataframe

        Inputs: self

        Outputs: v_type(str) - variable type
                 particle(str) - particle name
                 data(array) - array of the actual data to be plotted
        '''
        df_name = self.df.name.split('_')
        data = self.df.to_numpy()
        #if len(df_name) == 2:
         #   v_type = df_name[1]
          #  particle = df_name[0]
        #else:
        v_type = df_name[-1]
        particle = self.df.name[:-(len(v_type)+1)]

        return v_type, particle, data

    def get_range(self):
        '''
        Function to get range of data
        
        Inputs: self
        
        Outputs: hist_range(tuple) - min and max values of data histogram
        '''
        hist_min = np.min(self.data)
        hist_max = np.max(self.data)
        hist_range = (hist_min, hist_max)
        return hist_range

    def plot(self, ax):
        '''
        Function to produce a colour-mapped histogram

        Inputs: self
                ax(plt axes) - axis to append plot to

        Outputs: ax(axarr) - 2-sided axis array with histogram plotted on 
        '''
        cmap = plt.cm.get_cmap(self.cm)

        n, _, patches = ax[0].hist(self.data, self.bins, density=True, range=self.hist_range)
        _, _, patches2 = ax[1].hist(self.data, self.bins, density=True)
        ax[0].set_ylabel(self.particle, rotation=0)
        ax[0].yaxis.set_label_coords(-0.03, -0.05)
        col = (n - n.min()) / (n.max() - n.min())
        for c, p, p2 in zip(col, patches, patches2):
            plt.setp(p, 'facecolor', cmap(c))
            plt.setp(p2, 'facecolor', cmap(c))
        
        ax[1].invert_yaxis()
        plt.subplots_adjust(hspace=0)
        for a in ax:
            a.set_yticklabels([])
            a.set_yticks([])
            a.get_xaxis().set_visible(False)
            a.spines['right'].set_visible(False)
            a.spines['left'].set_visible(True)

        ax[0].spines['top'].set_visible(False)
        ax[1].spines['bottom'].set_visible(False)
        return ax

