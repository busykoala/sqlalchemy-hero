from dataclasses import dataclass

from sqlalchemy_hero.types.metadata import HeroMetadata
from sqlalchemy_hero.types.spec import HeroSpec


@dataclass
class HeroFile:
    apiVersion: str
    kind: str
    metadata: HeroMetadata
    spec: HeroSpec
