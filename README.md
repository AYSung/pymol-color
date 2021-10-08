# pymol-color
generate script for coloring pymol structures based on csv score tables from various bioinformatic servers (e.g. ConSurf, MODA)



## Color by MODA score

1. Go to http://molsoft.com/~eugene/moda/modamain.cgi
2. Upload PDB file or enter PDB code, then click 'Predict'
3. Download the results as a CSV table
4. Open terminal and navigate to the script directory
5. Use the command `python3 moda-color.py ./sample_moda.csv`, replacing `./sample_moda.csv` with the path to your MODA csv file.
    * Also supports multiple input files e.g. `python3 moda-color.py ./sample_moda_1.csv ./sample_moda_2.csv ./*_moda.csv`
6. There should now be a new file in same directory as the MODA csv with the suffix `-moda-coloring-script.py`
7. Cut and paste the coloring script into the same directory as the PDB file
8. Open the PDB file in PyMOL and run the command `@<prefix>-moda-coloring-script.py`