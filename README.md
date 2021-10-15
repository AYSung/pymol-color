# pymol-color
Command line utility to generate pymol script for coloring structures based on csv score tables from various bioinformatic servers (e.g. ConSurf, MODA)

## Generating coloring script for pymol
Open terminal and navigate to script directory. Run script with the follow command

`python3 main.py [ moda | consurf | gnomad | custom ] files*`

where the first positional argument is for what type of scores are being mapped and the second positional argument is a file (or multiple files) on which to perform the analysis. A separate coloring script will be generated in a `results` folder for each input file.

To color the PyMOL structure, move coloring script to same directory as the PDB file. Open the PDB file in PyMOL and run the command:

`@<file_name>-coloring-script.pml`

Running the script will color the pymol structure as well as generate selection groups for each group of color.

## Getting ConSurf scores
1. Go to https://consurf.tau.ac.il/ to get ConSurf scores for protein of interest
2. Download results in CSV table

## Getting MODA scores
1. Go to http://molsoft.com/~eugene/moda/modamain.cgi
2. Upload PDB file or enter PDB code, then click 'Predict'
3. Download the results as a CSV table

## Getting gnomAD annotations
1. Go to https://gnomad.broadinstitute.org/ and find gene of interest
2. Scroll down to 'gnomAD variants' section
3. Click 'Export variants to CSV' (script will automatically filter for missense mutations)

## Using a custom annotation
1. Create a csv file with the following headers:
    1. `residue` - the number of the residue to be annotated, only one residue number per line
    2. `label` - label for PyMOL group
    3. `color` - color for PyMOL group
**See sample-custom.csv for an example