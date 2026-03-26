from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional


@dataclass
class SortState:
    columns: List[str]
    index: int = 0
    direction: str = "asc"  # 'asc' or 'dsc'

    def current(self) -> str:
        return self.columns[self.index]

    def cycle(self) -> None:
        self.index = (self.index + 1) % len(self.columns)

    def toggle_direction(self) -> None:
        self.direction = "dsc" if self.direction == "asc" else "asc"

    def is_filesystem(self) -> bool:
        return self.current() == "filesystem"

    def sort_key_fn(self, column: str, mapping: dict[str, Callable]) -> Optional[Callable]:
        """Return a key function for the given column using mapping.

        mapping maps column name -> key function that accepts an item and returns a sort key.
        If column is 'filesystem' return None to indicate natural ordering.
        """
        if column == "filesystem":
            return None
        return mapping.get(column)
