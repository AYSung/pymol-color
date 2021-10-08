import argparse
from pathlib import Path
import pandas as pd
import numpy as np


def get_bins(MODA_df):
    medium, high, very_high = (50, 100, 1000)  # set bin thresholds
    bins = pd.IntervalIndex.from_tuples(
        [(medium, high), (high, very_high), (very_high, np.inf)])
    bin_names = ['medium', 'high', 'very_high']
    bin_colors = ['yelloworange', 'tv_orange', 'firebrick']

    binned_data = pd.cut(MODA_df['plainMODA'], bins).map(
        dict(zip(bins, bin_names)))
    binned_residue_numbers = [get_residues(
        binned_data, bin_name) for bin_name in bin_names]
    return zip(bin_names, binned_residue_numbers, bin_colors)


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


def import_data(file_path):
    return pd.read_csv(
        file_path,
        usecols=['num', 'plainMODA'],
        index_col=['num'],
    )


def main(file_path):
    data = import_data(file_path)
    pymol_script = generate_pymol_script(get_bins(data))

    with open(file_path.with_name(f'{file_path.stem}-moda-coloring-script').with_suffix('.py'), 'w') as f:
        f.write(pymol_script)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='MODA color', description='Generate pymol script to color residues based on MODA score')
    parser.add_argument('csv',
                        metavar='moda.csv',
                        nargs='+',
                        type=Path,
                        help='csv file with MODA scores',
                        )
    args = parser.parse_args()
    for file_path in args.csv:
        main(file_path)
