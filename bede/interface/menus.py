from typing import Iterable, Optional

import click


def make_menu(items: Iterable[str], title: Optional[str] = None) -> str:
    if title is not None:
        menu_str = f'{title}:\n'
    else:
        menu_str = 'Choose Option:'

    for idx, item in enumerate(items):
        menu_str += f'{idx + 1} - {item}\n'

    return menu_str


def prompt_menu(items: Iterable[str], title: Optional[str] = None, **kwargs):
    return click.prompt(make_menu(items, title=title), type=click.IntRange(min=1, max=len(items)), **kwargs)


def main_menu():
    # TODO Make title persistent
    click.echo(f'The Venerable Bede')
    task = prompt_menu(['Search Document (Default)', 'Register Document', 'Validate Library'],
                       title='Choose Task', default=1)
    click.echo(task)
