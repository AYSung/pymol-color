import argparse
from pathlib import Path
import pandas as pd
import numpy as np
from collections import namedtuple


Groups = namedtuple('Groups', ['label', 'residues', 'color'])


# wraps grouping function (e.g. moda, consurf) to make it write the script
def make_pymol_commands(func):
    def wrapper(file_path):
        groupings = func(file_path)

        default_color = 'gray80'

        pymol_commands = f'{default_color}\n'
        for label, residues, color in groupings:
            pymol_commands += f'select {label}, resi {residues}\n'
            pymol_commands += f'color {color}, {label}\n'
        pymol_commands += 'show surface\n'
        pymol_commands += 'set transparency, 0.2\n'
        pymol_commands += 'bg_color white\n'
        
        script_path = file_path.with_name(f'{file_path.stem}-coloring-script.pml')
        
        with open(script_path, 'w') as f:
            f.write(pymol_commands)
    return wrapper


@make_pymol_commands
def moda(file_path):
    labels = ['low', 'medium', 'high', 'very_high']
    colors = ['gray80','yelloworange', 'tv_orange', 'firebrick']

    data = pd.read_csv(
        file_path,
        usecols=['num', 'plainMODA'],
        index_col=['num'],
    )
    medium, high, very_high = (50, 100, 1000)  # set bin thresholds
    bins = pd.IntervalIndex.from_tuples([
        (0, medium),
        (medium, high),
        (high, very_high),
        (very_high, np.inf)
        ])
    data = pd.cut(data['plainMODA'], bins).map(dict(zip(bins, labels)))
    return group_by_category(data, labels, colors)


@make_pymol_commands
def consurf(file_path):
    labels = [str(i) for i in range(1, 10)]
    colors = ['teal', 'cyan', 'aquamarine', 'palecyan',
              'white', 'lightpink', 'pink', 'deepsalmon', 'raspberry']

    data = pd.read_csv(
        file_path,
        skiprows=4,
        usecols=['pos', 'ConSurf Grade'],
        index_col=['pos'],
    )
    data['ConSurf Grade'] = data['ConSurf Grade'].str.replace('*', '', regex=False)
    return group_by_category(data, labels, colors)


def group_by_category(data, labels, colors):
    def get_residues(data, label):
        filter = data.values == label
        residues = data[filter].index.astype(str).tolist()
        return '+'.join(residues)

    residues = [get_residues(data, label) for label in labels]
    return [Groups(*tup) for tup in zip(labels, residues, colors)]


def main(args):
    make_script = eval(args.mode)
    for file_path in args.csv:
        make_script(file_path)


if __name__ == '__main__':
    MODES = ['moda', 'consurf']

    parser = argparse.ArgumentParser(
        prog='PyMol color', 
        description='Generate pymol coloring script based on csv score tables')
    parser.add_argument(
        'mode',
        metavar='mode',
        type=str,
        choices=MODES,
        help='type of analysis (e.g. moda, consurf)',
        )
    parser.add_argument(
        'csv',
        metavar='csv',
        nargs='+',
        type=Path,
        help='csv file with residue scores',
        )
    args = parser.parse_args()
    main(args)
