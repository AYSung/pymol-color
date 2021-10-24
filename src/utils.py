import argparse
import numpy as np
import pandas as pd

from pathlib import Path


def import_moda(path: Path) -> pd.DataFrame:
    """Generates a pymol coloring script from a csv table of MODA scores"""
    file_format = {'usecols': ['num','plainMODA']}
    
    labels = ['low', 'medium', 'high', 'very_high']
    colors = ['gray80', 'yelloworange', 'tv_orange', 'firebrick']

    bins = [0, 50, 100, 1000, np.inf]
    return (pd.read_csv(path, **file_format)
            .rename(columns={'num': 'residue', 
                             'plainMODA': 'label'})
            .assign(label=lambda x: pd.cut(x.label, bins=bins, labels=labels, include_lowest=True),
                    color=lambda x: x.label.map(dict(zip(labels, colors)))))

def import_consurf(path: Path) -> pd.DataFrame:
    """Generates a pymol coloring script from a csv table of ConSurf scores"""
    file_format = {'skiprows': 4, 'usecols': ['pos', 'ConSurf Grade']}

    labels = [str(i) for i in range(1, 10)]
    colors = ['teal', 'cyan', 'aquamarine', 'palecyan',
              'white', 'lightpink', 'pink', 'deepsalmon', 'raspberry']

    return (pd.read_csv(path, **file_format)
            .rename(columns={'pos':'residue', 
                             'ConSurf Grade': 'label'})
            .assign(label=lambda x: x.label.str.replace('*', '', regex=False),
                    color=lambda x: x.label.map(dict(zip(labels, colors)))))

def import_gnomad(path: Path) -> pd.DataFrame:
    """Generates a pymol coloring script from a gnomAD variant table.
    Residues with multiple types of annotations will be colored based
    on the most severe annotation (pathogenic > likely_pathogenic > 
    uncertain_significance > likely_benign > benign > no annotation)
    """
    file_format = {'usecols': ['Protein Consequence', 'VEP Annotation', 'ClinVar Clinical Significance']}

    labels = ['pathogenic', 'likely_pathogenic', 'uncertain_significance', 'likely_benign', 'benign', 'no_annotation']
    colors = ['firebrick', 'salmon', 'paleyellow', 'lightblue', 'skyblue', 'gray60']

    return (pd.read_csv(path, **file_format)
            .rename(columns={'Protein Consequence': 'residue',
                             'VEP Annotation': 'type',
                             'ClinVar Clinical Significance': 'label'})
            .loc[lambda x: x.type == 'missense_variant']
            .drop(columns='type')
            .assign(residue=lambda x: x.residue.str.extract(r'(\d+)'),
                    label=lambda x: x.label.str.lower().str.replace(' ','_')
                                     .str.replace(r'\w+/','', regex=True)
                                     .fillna('no_annotation')
                                     .astype('category')
                                     .cat.set_categories(labels, ordered=True),
                    color=lambda x: x.label.map(dict(zip(labels, colors))).astype('category'))
            .sort_values(by='label')
            .drop_duplicates(subset='residue')
        )

def import_custom(path: Path) -> pd.DataFrame:
    """Generates a pymol coloring script from a csv table of custom annotations and colors"""
    file_format = {'usecols': ['residue', 'label', 'color']}

    return pd.read_csv(path, **file_format)


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



FUNCTION_MAP = {
    'moda': import_moda,
    'consurf': import_consurf,
    'gnomad': import_gnomad,
    'custom': import_custom,
}