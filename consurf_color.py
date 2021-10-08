import argparse
from pathlib import Path
import pandas as pd


def get_bins(data):
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


def import_data(file_path):
    consurf_data = pd.read_csv(
        file_path,
        skiprows=4,
        usecols=['pos', 'ConSurf Grade'],
        index_col=['pos'],
    )
    consurf_data['ConSurf Grade'] = consurf_data['ConSurf Grade'].str.replace(
        '*', '', regex=False)
    return consurf_data


def main(file_path):
    data = import_data(file_path)
    pymol_script = generate_pymol_script(get_bins(data))
    with open(file_path.with_name(f'{file_path.stem}-consurf-coloring-script').with_suffix('.py'), 'w') as f:
        f.write(pymol_script)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='ConSurf color', description='Generate pymol script to color residues based on consurf score')
    parser.add_argument('csv',
                        metavar='moda.csv',
                        nargs='+',
                        type=Path,
                        help='csv file with MODA scores',
                        )
    args = parser.parse_args()
    for file_path in args.csv:
        main(file_path)
