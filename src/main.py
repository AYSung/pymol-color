from pathlib import Path
import os
from typing import Tuple

import pandas as pd

from src.utils import FUNCTION_MAP, create_parser


def bin_residues(data: pd.DataFrame) -> Tuple[str, str, str]:
    """Groups residues with the same label into a single string joined
    by the '+' character. Returns a tuple of (label, color, residue #s)
    """
    return (data
            .astype({'residue':str})
            .groupby(['label','color'], observed=True, sort=False).agg('+'.join)
            .sort_index(level='label')
            .pipe(lambda x: print(x) or x)
            .to_records()
            )
  
def make_script(path: Path, import_data: function) -> None:
    groupings = (import_data(path).pipe(bin_residues))
    output_path = path.with_name(f'{path.stem}-coloring-script.pml')
    output_directory = path.parent/'results'
    if not output_directory.exists():
        os.mkdir(output_directory)

    # Change Parameters
    default_color = 'gray80'
    surface_transparency = 0.2
    #
    
    # TODO: add support for specifying chain letter

    with open(output_directory/output_path, 'w') as f:
        f.write(f'color {default_color}\n')
        for label, color, residues in groupings:
            f.write(f'select {label}, resi {residues}\n')
            f.write(f'color {color}, {label}\n')
        f.write('show surface\n')
        f.write(f'set transparency, {surface_transparency:.1f}\n')
        f.write('bg_color white')



            

def main(args):
    import_func = FUNCTION_MAP[args.mode]
    for path in args.csv:
        make_script(path, import_func)


if __name__ == '__main__':
    parser = create_parser()
    main(parser.parse_args())
