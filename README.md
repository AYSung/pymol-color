# pymol-color
Command line utility to generate pymol script for coloring structures based on csv score tables from various bioinformatic servers (e.g. ConSurf, MODA)

## Generating coloring script for pymol
Open terminal and navigate to script directory. Run script with the follow command

`python3 pymol-color.py [ moda | consurf ] files*`

where the first positional argument is for what type of scores are being mapped and the second positional argument is a file (or multiple files) on which to perform the analysis. A separate coloring script will be generated for each input file.

To color the PyMOL structure, move coloring script to same directory as the PDB file. Open the PDB file in PyMOL and run the command:

`@<file_name>-coloring-script.pml`

## Getting ConSurf scores
1. Go to https://consurf.tau.ac.il/ to get ConSurf scores for protein of interest
2. Download results in CSV table

## Getting MODA scores

1. Go to http://molsoft.com/~eugene/moda/modamain.cgi
2. Upload PDB file or enter PDB code, then click 'Predict'
3. Download the results as a CSV table