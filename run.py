from utils.process_data import *
from utils.multiplot import multiplot
import argparse


def run(path, variables, tags, exclude, onlyconst, cuts):
    '''
    Function to run HoliTree tool

    Inputs: 
    path (str)         - path to file to be plotted
    variables (list)   - list of variables (str) to plot, separated from unit
                         by '*'
    tags (list)        - names of pre-applied constraints in tree
    exclude (list)     - names of any branch tags to be excluded fromt the plot 
    onlyconst (bool)   - flag to switch off automatic plotting of un-tagged branches
                         not in "exclude"
    cuts (dict)        - dictionary of cuts to be applied at new plots made for 
                         (format described in the process_data function "assess_cuts")
            
    Outputs:
    Saves HoliTree plot
    '''
    if onlyconst:
        print('Automatic plotting of untagged variables turned OFF')
    else:
        print('Automatic plotting of untagged variables tuned ON')
    df = convert_to_df(path)
    if exclude:
        df = exclude_constraints(df, exclude)
    if cuts:
        assess_cuts(cuts)
        print('All cuts good')
        df, tags = apply_cuts(df, cuts, tags)
    if tags or cuts:
        variables = extract_constraints(variables, tags)

    multiplot(df, variables, onlyconst)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run HoliTree plotting and save plot to pdf" +
                                     "from inside HoliTree folder.")
    parser.add_argument('-vars', nargs='+', default=['M*MeV'],
                        help='Variables to be plotted, in form [var1*unit1, var2*unit2, ...]')
    parser.add_argument('-path', nargs='?', default='./processed_data/example.pkl', 
                        help='Path to file to be plotted (.root or .pkl)')
    parser.add_argument('--tags', nargs='+', default=False, 
                        help='List of names of any tagged constraints pre-applied to dataset')
    parser.add_argument('--exclude', nargs='+', default=False,
                        help='List of names of any constraints to be excluded from the plot')
    parser.add_argument('--onlytagged', action='store_true',
                        help='Flag to ONLY display tagged branches, and no un-tagged ones')
    parser.add_argument('--cuts', default=False,
                        help='Define any cuts here as dictionary')
    args = parser.parse_args()

    print('Args: ', args)
    variables = args.vars
    path = args.path
    tags = args.tags
    exclude = args.exclude
    onlytagged = args.onlytagged
    cuts = args.cuts

    #tags = ['B0_OnlyD', 'B0_BandDs']
    exclude = ['DTF', 'KasP', 'KasPi', 'PiasK', 'PiasP', 'B0_OnlyD', 'B0_BandDs']
    cuts = {'DDKcut': {'type':'veto','var':'KD0D0bar_M', 'region':'5050,5200'}}

    #        'testmin': {'type':'min', 'var':'D0D0bar_M', 'value':'200'}}

    run(path, variables, tags, exclude, onlytagged, cuts)
