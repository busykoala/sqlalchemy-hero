from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import Optional


@dataclass
class HeroColumn:
    name: str
    type: str
    constraints: Optional[Dict[str, bool]] = field(default_factory=dict)
    attributes: Optional[Dict[str, bool]] = field(default_factory=dict)
