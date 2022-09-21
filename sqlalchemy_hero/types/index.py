from dataclasses import dataclass
from typing import List


@dataclass
class HeroIndex:
    columns: List[str]
    name: str
    isUnique: bool
