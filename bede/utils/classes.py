from typing import Optional, Union
from pathlib import Path
from dataclasses import dataclass

GenericPath = Union[Path, str]


@dataclass
class Date:
    year: int
    month: Optional[int]
    day: Optional[int]

    def __repr__(self):
        return f'{self.month}/{self.day}/{self.year}'
