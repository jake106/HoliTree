# Requirements and features

## Requirements
Python = 3.8.5
Pandas = 1.1.3
Numpy = 1.19.4
PIL = 8.1.2
Uproot = 3.10.12

## Features to be added
- default units for variables
- Expanded testing and continuous integration
- allow multiple cuts with single tag
- make command line output more coherent
- compile all preporcessing scripts in single useful package

# Example plot

![Example](https://github.com/jake106/HoliTree/blob/main/HoliTree_M_DDKcut_M.pdf)

# Usage

## Preprocessing data
```bash
usage: python preprocess.py -path -untagged_names --tagged_names --tags --combinations --additional_vars

Trims down dataframe to be plotted for faster plotting. Also contains a number of helpers to add mass combinations ect.

Positional arguments:
-path - path to file to be preprocessed
-untagged_names - dictionary with keys corresponding to desired plotting names, and items corresponding to names of untagged particles in dataframe

Optional arguments:
--tagged_names - same as untagged names, for when tagged branches name particles differently  
--tags - list of names of any tags
--combinations - dictionary with keys being the names of composite particles, items are names of particles in original tuple that compose these particles
--additional_vars - any non-kinematic variables to be added (not Px, Py, Pz, E, M)
```

## Running HoliTree
```bash
usage: python run.py -vars -path --tags --exclude --onlytagged

Runs the HoliTree tool, saving the output as a jpeg/pdf in the current folder.

Positional Arguments:
-path - path to file to be plotted
-vars - variables to be plotted

Optional Arguments:
--tags - specify any tagged branches to be plotted
--exclude - specify any tagged branches to not be plotted
--onlytagged - set to TRUE to only plot tagged branches that are included in --tags
--cuts - define dictionary of cuts to be applied and plotted, fomat defined below

```

### Cutting format
Any number of cuts must be defined as a dictionary in the form:

{'cut1name':{'type':'veto, min or max', 'var':'variable to be cut on', 'region (if veto), value (if min or max)':min/max value, or 2 comma-separated values if veto},cut2name:{...}}

### Example
If you have a decay tree with untagged branches, and three seperate tagged ones, called 'tag1', 'tag2' and 'tag3':

To plot only untagged branches, include 'tag1', 'tag2' and 'tag3' in the --exclude argument.  

To plot all branches, simply include 'tag1', 'tag2' and 'tag3' in the --tags argument.  

To plot only the three tagged branches, include them in the --tags flag and also set --onlytagged to true.  

To plot only the 'tag1' branch, include it in --tags argument and set --onlytagged to true.  

To plot only the 'tag1' and untagged branches, include 'tag1' in --tags, and include 'tag2' and 'tag3' in --exclude.  

Note: if --onlytagged is false (default), and there are tagged branches not specified in the --tags or --exclude arguments, the HoliTree plot will look bloody horrible.
