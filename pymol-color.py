import argparse
from pathlib import Path
import pandas as pd
import numpy as np


def import_moda(path):
    """Generates a pymol coloring script from a csv table of MODA scores"""
    file_format = {'usecols': ['num','plainMODA']}
    
    labels = ['low', 'medium', 'high', 'very_high']
    colors = ['gray80', 'yelloworange', 'tv_orange', 'firebrick']

    bins = [0, 50, 100, 1000, np.inf]
    return (pd.read_csv(path, **file_format)
            .rename(columns={'num': 'residue', 'plainMODA': 'label'})
            .assign(label=lambda x: pd.cut(x.label, bins=bins, labels=labels, include_lowest=True),
                    color=lambda x: x.label.map(dict(zip(labels, colors))))
            )

def import_consurf(path):
    """Generates a pymol coloring script from a csv table of ConSurf scores"""
    file_format = {'skiprows': 4, 'usecols': ['pos', 'ConSurf Grade']}

    labels = [str(i) for i in range(1, 10)]
    colors = ['teal', 'cyan', 'aquamarine', 'palecyan',
              'white', 'lightpink', 'pink', 'deepsalmon', 'raspberry']

    return (pd.read_csv(path, **file_format)
            .rename(columns={'pos':'residue', 'ConSurf Grade': 'label'})
            .assign(label=lambda x: x.label.str.replace('*', '', regex=False),
                    color=lambda x: x.label.map(dict(zip(labels, colors))))
            )

def import_custom(path):
    """Generates a pymol coloring script from a csv table of custom annotations and colors"""
    file_format = {'usecols': ['residue', 'label', 'color']}

    return pd.read_csv(path, **file_format)


def make_script(path, import_data):
    groupings = (import_data(path).pipe(bin_residues))
    output_path = path.with_name(f'{path.stem}-coloring-script.pml')

    with open(output_path, 'w') as f:
        f.write('color gray80\n')
        for label, color, residues in groupings:
            f.write(f'select {label}, resi {residues}\n')
            f.write(f'color {color}, {label}\n')
        f.write('show surface\n')
        f.write('set transparency, 0.2\n')
        f.write('bg_color white')


def bin_residues(data):
    '''Groups residues with the same label into a single string joined
    by the '+' character. Returns a tuple of (label, color, residue #s)
    '''
    return (data
            .astype(str)
            .groupby(['label','color']).residue.apply('+'.join)
            .reset_index()
            .to_records(index=False)
            )
            

def main(args):
    import_data = FUNCTION_MAP[args.mode]
    for path in args.csv:
        make_script(path, import_data)


if __name__ == '__main__':
    FUNCTION_MAP = {
        'moda': import_moda,
        'consurf': import_consurf,
        'custom': import_custom
    }

    parser = argparse.ArgumentParser(
        prog='PyMol color',
        description='Generate pymol coloring script based on csv score tables')
    parser.add_argument(
        'mode',
        metavar='mode',
        type=str,
        choices=FUNCTION_MAP.keys(),
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
