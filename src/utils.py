import argparse
from pathlib import Path

from extension import FUNCTION_MAP


def create_parser():
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
    return parser