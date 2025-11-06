# AST node classes for the Flow programming language.

from dataclasses import dataclass, field
from typing import List

@dataclass
class Load:
    path: str
    alias: str

@dataclass
class Pipeline:
    name: str
    steps: list
    base_alias: str = None
    depends_on: str = None 

@dataclass
class Filter:
    expr: str

@dataclass
class Sum:
    column: str
    alias: str

@dataclass
class GroupBy:
    column: str

@dataclass
class Average:
    column: str
    alias: str

@dataclass
class DropDuplicates:
    column: str

@dataclass
class SortBy:
    column: str
    ascending: bool

@dataclass
class Emit:
    path: str

@dataclass
class Ensure:
    condition: str

@dataclass
class Join:
    other_alias: str
    on: str

@dataclass
class Rename:
    old_name: str
    new_name: str

@dataclass
class Select:
    columns: List[str]