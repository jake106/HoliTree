from processing.process_data import convert_to_df, extract_constraints
from plotting.multiplot import multiplot
import argparse


def run(path, variables, contraints):
    '''
    Function to run HoliTree tool

    Inputs: path (str)         - path to file to be plotted
            variables (list)   - list of variables (str) to plot, separated from unit
                                 by '*'
            constraints (list) - names of pre-applied constraints in tree

    Outputs: Saves HoliTree plot
    '''
    if constraints:
        variables = extract_constraints(variables, constraints)
    df = convert_to_df(path)
    multiplot(df, variables)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run HoliTree plotting and save plot to pdf" +
                                     "from inside HoliTree folder.")
    parser.add_argument('path', type=str, nargs='?', default='./DstDK_randompion_tis_df.pkl', 
                        help='Path to file to be plotted (.root or .pkl)')
    parser.add_argument('variables', type=list, nargs='?', default=['M*MeV', 'PT*MeV'],
                        help='Variables to be plotted, in form [var1*unit1, var2*unit2, ...]')
    parser.add_argument('--constraints', action='store_true', 
                        help='Names of any constraints pre-applied to dataset')
    args = parser.parse_args()

    print('Args: ', args)
    path = args.path
    variables = args.variables
    constraints = args.constraints
    
    constraints = ['OnlyD', 'BandDs']
    run(path, variables, constraints)


