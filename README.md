# pymol-color
Command line utility to generate pymol script for coloring structures based on csv score tables from various bioinformatic servers (e.g. ConSurf, MODA)

## Run as PyMOL extension
Boot up PyMOL and enter the following in the command line `run <path-to-pymol-color>/src/extension.py`, replacing the contents in the angle brackets with the path to the pymol-color folder. Depending on how PyMOL is set up on your machine, it might raise a `ImportError: No module named pandas` error message. If this happens, you can either:
1. In the PyMOL command line, run `pip install pandas` (you might need to do this each time you open PyMOL)
2. Open a terminal/command prompt and run the following command `pip install --target=<path to PyMOL install>/pkgs pandas`

Once `run extension.py` succeeds, you will be able to color any object opened in that PyMOL instance with the command `color_by_score analysis-type, path-to-csv-file`, where:
* analysis-type is either moda, consurf, gnomad, or custom
* path-to-csv-file is the relative path to the csv file containing the per-residue scores

You can also supply several optional keyworded arguments of the form `keyword=value` separated by commas. The keywords are as follows:
* object : string, the name of the PyMOL object to be colored (defaults to all objects)
* segment : string, the segment of the PyMOL object to be colored (defaults to all segments)
* chain : string, the chain of the PyMOL object to be colored (defaults to all chains)
* default_color : string, color of residues that are not found in the csv score file (defaults to gray80)
* bg_color : string, background color of PyMOL (defaults to black)
* surface : boolean, whether to display the surface of the protein after the script is done coloring (defaults to False)
* surface_transparency : float value between 0 and 1. set transparency value of the surface (defaults to 0.2)

The extension will also create selection groups for each color.

## Generating coloring script for pymol using the command line interface (CLI)
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