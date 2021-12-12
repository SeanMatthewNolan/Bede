from pathlib import Path
from typing import Sequence, Container, Iterable, Any, Union, Optional

import click
from PyPDF2 import PdfFileMerger

from ..utils import flatten_to_list, make_ordinal
from ..utils.classes import GenericPath

TEMP_PREFIX = '__temp_'


def merge(files: Sequence[str], out_file: str, reorder: bool = False, append: bool = False):
    out_file = Path(out_file)
    out_file_exists = out_file.is_file()

    files = filter_files(files, ext='.pdf', exclude=out_file)
    if reorder:
        files = reorder_prompt(files, item_desc='file to merge')

    if len(files) == 0:
        click.echo('No PDF files specified. No operation will be performed.')
        return

    if append and out_file_exists:
        files = (out_file, *files)
        out_file = Path(*out_file.parts[:-1], TEMP_PREFIX + str(out_file.parts[-1]))

    merger = PdfFileMerger()
    for file in files:
        merger.append(str(file))

    with out_file.open('wb') as out:
        merger.write(out)

    merger.close()

    if append and out_file_exists:
        out_file.replace(Path(*out_file.parts[:-1], out_file.name[len(TEMP_PREFIX):]))
        click.echo(f'{len(files)} files merged and saved to {out_file}')
    else:
        click.echo(f'{len(files)} files merged and saved to {out_file}')


def filter_files(files: Sequence[GenericPath], ext: Optional[Union[GenericPath, Container[GenericPath]]] = None,
                 exclude: Optional[Sequence[GenericPath]] = None):
    if isinstance(ext, str) or not isinstance(ext, Container):
        ext = [ext]

    if isinstance(ext, str) or isinstance(ext, Iterable):
        exclude = [exclude]

    filtered_files = []
    for file in flatten_to_list(files):
        # Ensure all files are of type Pathlib.Path()
        file = Path(file)

        # Ensure file exists.
        if not file.is_file():
            continue

        # Remove files without specified extensions
        if file.suffix not in ext:
            continue

        # Remove excluded files
        file_excluded = False
        for excluded_item in exclude:
            if file.match(str(excluded_item)):
                file_excluded = True
                break
        if file_excluded:
            continue

        filtered_files.append(file)

    return filtered_files


def reorder_prompt(items: Sequence[Any], item_desc: str = 'file') -> list[Any]:
    items = [*items]
    reordered = []
    undo_idx_stack = []

    finish_str = 'Finish'
    undo_str = ''

    while items:
        if undo_idx_stack:
            options = [*items, undo_str, finish_str]
        else:
            options = [*items, finish_str]

        chosen_idx, chosen_item = choose_item(options, item_desc=f'{make_ordinal(len(reordered) + 1)} {item_desc}')

        if chosen_item is undo_str:
            items.insert(undo_idx_stack.pop(), reordered.pop())
            undo_str = f'Undo: {reordered[-1]}'
        elif chosen_item is finish_str:
            if click.confirm(f'Are you sure you want to finish?'):
                break
        else:
            reordered.append(items.pop(chosen_idx))
            undo_idx_stack.append(chosen_idx)
            undo_str = f'Undo: {reordered[-1]}'

    return reordered


def choose_item(items: Sequence[Any], item_desc: str = 'file') -> Any:
    prompt_str = f'Choose {item_desc}:\n'
    for idx, item in enumerate(items, start=1):
        prompt_str += f'    {idx}: {item}\n'

    chosen_idx = click.prompt(prompt_str, type=click.IntRange(min=1, max=len(items)), default=1) - 1
    click.clear()
    return chosen_idx, items[chosen_idx]
