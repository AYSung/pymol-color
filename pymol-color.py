import argparse
from pathlib import Path
import pandas as pd
import numpy as np


def make_into_pml_script(func):
    """Wraps a function that imports data into a Pandas Series with the residue
    number as the index and a corresponding categorical label and makes a PyMol
    coloring script out of the labels, residues, and colors.
    """
    def bin_residues(data, labels):
        """Return list of residues in each category joined with '+'"""
        def get_residues(data, label):
            residues = data[data.values == label].index.astype(str).tolist()
            return '+'.join(residues)
        return [get_residues(data, label) for label in labels]

    def make_commands(groupings):
        """Generate string of pymol commands from tuple of labels, residues, and colors"""
        commands = 'gray80\n'
        for label, residues, color in groupings:
            commands += f'select {label}, resi {residues}\n'
            commands += f'color {color}, {label}\n'
        commands += 'show surface\n'
        commands += 'set transparency, 0.2\n'
        commands += 'bg_color white\n'
        return commands
    
    def wrapper(file_path):
        data, labels, colors = func(file_path)
        residues = bin_residues(data, labels)
        pymol_commands = make_commands(zip(labels, residues, colors))

        script_path = file_path.with_name(f'{file_path.stem}-coloring-script.pml')
        with open(script_path, 'w') as f:
            f.write(pymol_commands)
    return wrapper


@make_into_pml_script
def moda(file_path):
    """Generates a pymol coloring script from a csv table of MODA scores"""
    labels = ['low', 'medium', 'high', 'very_high']
    colors = ['gray80', 'yelloworange', 'tv_orange', 'firebrick']

    data = pd.read_csv(
        file_path,
        usecols=['num', 'plainMODA'],
        index_col=['num']
    )
    medium, high, very_high = (50, 100, 1000)
    bins = pd.IntervalIndex.from_tuples([
        (0, medium),
        (medium, high),
        (high, very_high),
        (very_high, np.inf)
    ])
    data = pd.cut(data['plainMODA'], bins).map(dict(zip(bins, labels)))
    return data, labels, colors


@make_into_pml_script
def consurf(file_path):
    """Generates a pymol coloring script from a csv table of ConSurf scores"""
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
    return data, labels, colors


def main(args):
    make_script = eval(args.mode)
    for file_path in args.csv:
        make_script(file_path)


if __name__ == '__main__':
    MODES = ['moda','consurf',]

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
