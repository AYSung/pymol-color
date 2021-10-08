import argparse
from pathlib import Path
import pandas as pd
import numpy as np


def import_moda(file_path):
    return pd.read_csv(
        file_path,
        usecols=['num', 'plainMODA'],
        index_col=['num'],
    )

def bin_moda(data):
    medium, high, very_high = (50, 100, 1000)  # set bin thresholds
    bins = pd.IntervalIndex.from_tuples(
        [(medium, high), (high, very_high), (very_high, np.inf)])
    bin_names = ['medium', 'high', 'very_high']
    bin_colors = ['yelloworange', 'tv_orange', 'firebrick']

    binned_data = pd.cut(data['plainMODA'], bins).map(
        dict(zip(bins, bin_names)))
    binned_residue_numbers = [get_residues(
        binned_data, bin_name) for bin_name in bin_names]
    return zip(bin_names, binned_residue_numbers, bin_colors)

def import_consurf(file_path):
    consurf_data = pd.read_csv(
        file_path,
        skiprows=4,
        usecols=['pos', 'ConSurf Grade'],
        index_col=['pos'],
    )
    consurf_data['ConSurf Grade'] = consurf_data['ConSurf Grade'].str.replace(
        '*', '', regex=False)
    return consurf_data

def bin_consurf(data):
    scores = [str(i) for i in range(1, 10)]
    residue_numbers = [get_residues(data, score) for score in scores]
    colors = ['teal', 'cyan', 'aquamarine', 'palecyan',
              'white', 'lightpink', 'pink', 'deepsalmon', 'raspberry']
    return zip(scores, residue_numbers, colors)


def get_residues(df, bin_name):
    filter = df.values == bin_name
    residue_numbers = df[filter].index.astype(str).tolist()
    return '+'.join(residue_numbers)


def generate_pymol_script(bins):
    default_color = 'gray80'

    output_string = f'{default_color}\n'
    for name, residue_numbers, color in bins:
        output_string += f'select {name}, resi {residue_numbers}\n'
        output_string += f'color {color}, {name}\n'
    output_string += 'show surface\n'
    output_string += 'set transparency, 0.2\n'
    output_string += 'bg_color white\n'

    return output_string


def main(args):
    import_data = IMPORT_FUNCTIONS[args.mode]
    bin_data = BIN_FUNCTIONS[args.mode]

    for file_path in args.csv:
        data = import_data(file_path)
        bins = bin_data(data)
        pymol_script = generate_pymol_script(bins)

        export_path = file_path.with_name(f'{file_path.stem}-{args.mode}-coloring-script').with_suffix('.pml')
        with open(export_path, 'w') as f:
            f.write(pymol_script)


if __name__ == '__main__':
    IMPORT_FUNCTIONS = {
        'moda': import_moda,
        'consurf': import_consurf,
    }
    BIN_FUNCTIONS = {
        'moda': bin_moda,
        'consurf': bin_consurf,
    }

    parser = argparse.ArgumentParser(
        prog='PyMol color', description='Generate pymol script to color residues based on csv score tables from various bioinformatic servers (e.g. ConSurf, MODA)')
    parser.add_argument('mode',
                        metavar='mode',
                        type=str,
                        choices=IMPORT_FUNCTIONS.keys(),
                        help='type of analysis (e.g. moda, consurf)',
                        )
    parser.add_argument('csv',
                        metavar='csv',
                        nargs='+',
                        type=Path,
                        help='csv file with residue scores',
                        )
    args = parser.parse_args()
    main(args)
