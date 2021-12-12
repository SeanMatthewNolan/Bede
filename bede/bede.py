import os
from typing import Iterable

import click
import console

from .interface.cli.pages import main_menu
from .tagging import Library
from .pdf import merge

TEMP_PREFIX = '__temp_'


def shell():
    library = Library()


@click.command()
def cli():
    main_menu()

    # from console import fg, fx, defx
    # from console.screen import Screen
    # from console.utils import wait_key, set_title
    # from console.constants import ESC
    #
    # exit_keys = (ESC, 'q', 'Q')
    #
    # with Screen() as screen:
    #
    #     set_title('The Venerable Bede')
    #     with screen.location(5, 4):
    #         print(
    #                 fg.lightgreen('** Hi from a '
    #                               f'{fx.i}fullscreen{defx.i} app! **'),
    #                 screen.move_x(5),  # back up, then down
    #                 screen.move_down(5),
    #                 fg.yellow(f'(Hit the {fx.reverse("ESC")} key to exit): '),
    #                 end='', flush=True,  # optional
    #         )
    #
    #     with screen.hidden_cursor():
    #         wait_key(exit_keys)


def gui():
    print('Bede GUI not yet implemented')


def web():
    print('Bede web not yet implemented')


@click.command()
@click.option('-n', '--name', default='merged.pdf')
@click.option('-r', '--reorder/--no-reorder', default=False)
@click.option('-a', '--append/--no-append', default=False)
@click.argument('files', nargs=-1)
def pdf_merge(files: Iterable[str], name: str, reorder: bool = False, append: bool = False):
    merge(files, name, reorder=reorder, append=append)


if __name__ == '__main__':
    cli()
