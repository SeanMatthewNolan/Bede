from typing import Union, Optional, Iterable
from pathlib import Path

RawPath = Union[str, Path]


def check_extension(file: Path, extension: Union[str, Iterable[str]]):
    # TODO Consider making work with multiple suffixes like .tar.gz
    if isinstance(extension, str):
        return file.suffix == extension
    elif isinstance(extension, Iterable):
        return file.suffix in extension
    else:
        raise TypeError('Specified extension should be string or list of strings.')


def list_files_in_folder(folder: Path, max_depth: int = 10) -> list[Path]:
    files = []
    for item in folder.iterdir():
        if item.is_dir():
            if max_depth > 0:
                files += list_files_in_folder(item, max_depth=max_depth-1)
            else:
                print('Max recursion depth reached')
        elif item.is_file():
            files.append(item)

    return files


def get_abs_and_rel_paths(path: RawPath) -> (Path, Path):
    path = Path(path)
    if path.is_absolute():
        abs_path = path
        rel_path = path.relative_to(Path.cwd())
    else:
        abs_path = Path.cwd() / path
        rel_path = path

    return abs_path, rel_path


class Library:
    def __init__(self, root_path: RawPath = '.'):
        root_path = Path(root_path)
        if not root_path.exists() or not root_path.is_dir():
            raise RuntimeError('Library must point to directory.')

        self.abs_path, self.rel_path = get_abs_and_rel_paths(root_path)

        self.documents: list[Document] = []
        self.tags: list[Tag] = []

    def __repr__(self):
        return f'Library<{self.abs_path.name}>'

    def get_document_paths(self, absolute: bool = False) -> list[Path]:
        if absolute:
            return [doc.abs_path for doc in self.documents if doc.abs_path is not None]
        else:
            return [doc.rel_path for doc in self.documents if doc.rel_path is not None]

    def add_document(self, file_path: RawPath):
        file_path = Path(file_path)
        if file_path in self.get_document_paths(absolute=file_path.is_absolute()):
            print(f'"{file_path.name}" already in library.')
        elif file_path.exists():
            doc = Document(file_path)
            self.documents.append(doc)
        else:
            print(f'"{file_path.name}" does not exist.')

    def add_documents(self, *file_paths: Iterable[RawPath]):
        for file_path in file_paths:
            self.add_document(file_path)

    def list_files_in_folder(self):
        return list_files_in_folder(self.abs_path)

    def save(self):
        pass


class Document:
    def __init__(self, file_path: Optional[RawPath] = None):
        if file_path is not None:
            self.abs_path, self.rel_path = get_abs_and_rel_paths(file_path)
        else:
            self.abs_path, self.rel_path = None, None

        self.tags: set = set()

        self.title: Optional[str] = None
        self.author: Optional[str] = None
        self.year: Optional[str] = None

    def add_tag(self, tag):
        pass

    def __repr__(self):
        if self.title is not None:
            name = self.title

            if self.author is not None:
                name = f'{self.author} - {name}'

            if self.year is not None:
                name = f'{name} ({self.year})'

        elif self.rel_path is not None:
            name = self.rel_path.name

        else:
            name = f'Document<{id(self)}>'

        return name


class Tag:
    def __init__(self, name: str):
        self.name: str = name

        self.tagged_docs: set[Document] = set()

        self.supertags: set[Tag] = set()
        self.subtags: set[Tag] = set()

    def __repr__(self):
        return self.name


if __name__ == '__main__':
    import os

    test_library_path = Path('../../test_library')
    os.chdir(test_library_path)

    files = [*Path('').iterdir()]

    library = Library()
    library.add_documents(*files)

    doc = library.documents[0]
    doc.title = 'Solving Mixed State Control Constraint Problems'
    doc.author = 'Kshitij Mall'
    doc.year = '2020'



