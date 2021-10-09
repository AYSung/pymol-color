import argparse
from pathlib import Path
import pandas as pd
import numpy as np
from collections import namedtuple
from abc import ABC, abstractclassmethod


Groups = namedtuple('Groups', ['label', 'residues', 'color'])


class PyMOL_Script_Maker(ABC):
    labels, colors = None, None

    @abstractclassmethod
    def import_data(cls, file_path): pass

    @classmethod
    def bin_residues(cls, data):
        def get_residues(data, label):
            filter = data.values == label
            residues = data[filter].index.astype(str).tolist()
            return '+'.join(residues)

        residues = [get_residues(data, label) for label in cls.labels]
        return [Groups(*tup) for tup in zip(cls.labels, residues, cls.colors)]

    @classmethod
    def make_commands(cls, groupings):
        default_color = 'gray80'

        pymol_commands = f'{default_color}\n'
        for label, residues, color in groupings:
            pymol_commands += f'select {label}, resi {residues}\n'
            pymol_commands += f'color {color}, {label}\n'
        pymol_commands += 'show surface\n'
        pymol_commands += 'set transparency, 0.2\n'
        pymol_commands += 'bg_color white\n'
        return pymol_commands

    @classmethod
    def make_script(cls, file_path):
        data = cls.import_data(file_path)
        groupings = cls.bin_residues(data)
        pymol_commands = cls.make_commands(groupings)

        script_path = file_path.with_name(f'{file_path.stem}-coloring-script.pml')
        with open(script_path, 'w') as f:
            f.write(pymol_commands)


class MODA(PyMOL_Script_Maker):
    labels = ['low', 'medium', 'high', 'very_high']
    colors = ['gray80', 'yelloworange', 'tv_orange', 'firebrick']

    @classmethod
    def import_data(cls, file_path):
        data = pd.read_csv(
            file_path,
            usecols=['num', 'plainMODA'],
            index_col=['num']
        )
        medium, high, very_high = (50, 100, 1000)  # set bin thresholds
        bins = pd.IntervalIndex.from_tuples([
            (0, medium),
            (medium, high),
            (high, very_high),
            (very_high, np.inf)
        ])
        return pd.cut(data['plainMODA'], bins).map(dict(zip(bins, cls.labels)))


class ConSurf(PyMOL_Script_Maker):
    labels = [str(i) for i in range(1, 10)]
    colors = ['teal', 'cyan', 'aquamarine', 'palecyan',
              'white', 'lightpink', 'pink', 'deepsalmon', 'raspberry']

    @classmethod
    def import_data(cls, file_path):
        data = pd.read_csv(
            file_path,
            skiprows=4,
            usecols=['pos', 'ConSurf Grade'],
            index_col=['pos'],
        )
        data['ConSurf Grade'] = data['ConSurf Grade'].str.replace('*', '', regex=False)
        return data


def main(args):
    mode = MODES[args.mode]
    for file_path in args.csv:
        mode.make_script(file_path)


MODES = {
    'moda': MODA,
    'consurf': ConSurf
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='PyMol color',
        description='Generate pymol coloring script based on csv score tables')
    parser.add_argument(
        'mode',
        metavar='mode',
        type=str,
        choices=MODES.keys(),
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
