## Requirements
Python = 3.8.5
Pandas = 1.1.3
Numpy = 1.19.4
PIL = 8.1.2
Uproot = 3.10.12

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
--onlytagged - set to TRUE to only plot tagged branches

```

### Example
If you have a decay tree with untagged branches, and three seperate tagged ones, called 'tag1', 'tag2' and 'tag3':

To plot only untagged branches, include 'tag1', 'tag2' and 'tag3' in the --exclude argument.
To plot all branches, simply include 'tag1', 'tag2' and 'tag3' in the --tags argument.
To plot only the three tagged branches, include them in the --tags flag and also set --onlytagged to true.
To plot only the 'tag1' branch, include it in --tags argument and set --onlytagged to true.
To plot only the 'tag1' and untagged branches, include 'tag1' in --tags, and include 'tag2' and 'tag3' in --exclude.

Note: if --onlytagged is false (default), and there are tagged branches not specified in the --tags or --exclude arguments, the HoliTree plot will look bloody horrible.