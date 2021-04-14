from processing.process_data import convert_to_df, extract_constraints, exclude_constraints
from plotting.multiplot import multiplot
import argparse


def run(path, variables, contraints, exclude, onlyconst):
    '''
    Function to run HoliTree tool

    Inputs: path (str)         - path to file to be plotted
            variables (list)   - list of variables (str) to plot, separated from unit
                                 by '*'
            constraints (list) - names of pre-applied constraints in tree
            exclude (list)     - names of any branch tags to be excluded fromt the plot 
            onlyconst (bool)   - flag to switch off automatic plotting of un-tagged branches
                                 not in "exclude"

    Outputs: Saves HoliTree plot
    '''
    if onlyconst:
        print('Automatic plotting of untagged variables turned OFF')
    else:
        print('Automatic plotting of untagged variables tuned ON')
    if constraints:
        variables = extract_constraints(variables, constraints)
    df = convert_to_df(path)
    if exclude:
        df = exclude_constraints(df, exclude)
    multiplot(df, variables, onlyconst)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run HoliTree plotting and save plot to pdf" +
                                     "from inside HoliTree folder.")
    parser.add_argument('-vars', nargs='+', default=['M*MeV', 'PT*MeV'],
                        help='Variables to be plotted, in form [var1*unit1, var2*unit2, ...]')
    parser.add_argument('-path', nargs='?', default='./DstDK_randompion_tis_df.pkl', 
                        help='Path to file to be plotted (.root or .pkl)')
    parser.add_argument('--tags', nargs='+', default=['OnlyD', 'BandDs', 'OnlyB'], 
                        help='List of names of any tagged constraints pre-applied to dataset')
    parser.add_argument('--exclude', nargs='+', default=['DTF', 'KasP', 'KasPi', 'PiasK', 'PiasP'],
                        help='List of names of any constraints to be excluded from the plot')
    parser.add_argument('--onlytagged', action='store_true',
                        help='Flag to ONLY display tagged branches, and no un-tagged ones')
    args = parser.parse_args()

    print('Args: ', args)
    variables = args.vars
    path = args.path
    tags = args.tags
    exclude = args.exclude
    onlytagged = args.onlytagged

    run(path, variables, tags, exclude, onlytagged)


