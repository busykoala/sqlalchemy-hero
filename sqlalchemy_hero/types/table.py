from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Optional

from sqlalchemy_hero.types.column import HeroColumn
from sqlalchemy_hero.types.index import HeroIndex


@dataclass
class HeroTable:
    # name: str
    primaryKey: List[str]
    columns: List[HeroColumn]
    indexes: Optional[List[HeroIndex]] = field(default_factory=list)
